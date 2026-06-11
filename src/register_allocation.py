from itertools import count
from functools import reduce
from collections import deque

from register import *
from label import Label
from identifier import Id
import ast_9_sel as src
import ast_10_mem as tgt
from util.undirected_graph import UndirectedGraph
from util.priority_queue import PriorityQueue
from util.immutable_list import ilist
from util.directed_graph import DirectedGraph

from dataclasses import dataclass

# API

@dataclass
class RegAllocOutput:
    env: dict[Id, Register | tgt.Offset]
    offset_sp: int
    callee_saved: set[Register]

def allocate_registers(p: src.Program) -> dict[Label, RegAllocOutput]:
    outputs = {}
    for f in p:
        is_main = f.entry_label == Label("main")
        outputs[f.entry_label] = allocate_registers_for_body(is_main, f.body)
    return outputs

def allocate_registers_for_body(is_main: bool, blocks: src.Blocks) -> RegAllocOutput:
    cfg = control_flow_graph(blocks)
    liveness = liveness_analysis(blocks, cfg)
    interference = build_interference_graph(blocks, liveness)
    coloring = color_graph(interference)
    return assign_locations(is_main, coloring)

# Implementation

REG_ORDER = ilist(
    # can not be used for register allocation
    zero, sp, fp, tp, gp, ra, t0, t1,
    # can be used for register allocation
    a0, a1, a2, a3, a4, a5, a6, a7,
    s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11,
    t2, t3, t4, t5, t6,
)

REGISTER_TO_COLOR = {r: i - 8 for i, r in enumerate(REG_ORDER)}
COLOR_TO_REGISTER = {v: k for k, v in REGISTER_TO_COLOR.items()}

type Color = int  # colors are represented by natural numbers
type Node = Id | Register  # nodes in the inference graph

# the read set of an argument in read position
def read_set_src_arg(arg: src.ArgRead) -> set[Node]:
    match arg:
        case Register(_):
            return {arg}
        case Id(_):
            return {arg}
        case src.Offset(arg2, _):
            return read_set_src_arg(arg2)
        case Label(_) | src.Const(_, _):
            return set()

# the read set of an argument in write position
def read_set_dst_arg(arg: src.ArgWrite) -> set[Node]:
    match arg:
        case Register(_):
            return set()
        case Id(_):
            return set()
        case src.Offset(arg2, _):
            return read_set_src_arg(arg2)

# the write set of an argument in read position is always empty
def write_set_src_arg(arg: src.ArgRead) -> set[Node]:
    return set()

# the write set of an argument in write position
def write_set_dst_arg(arg: src.ArgWrite) -> set[Node]:
    match arg:
        case Register(_):
            return {arg}
        case Id(_):
            return {arg}
        case src.Offset(_, _):
            return set()

# the read set of an instruction
def read_set(i: src.Instr) -> set[Node]:
    match i:
        case src.Move(rd, rs):
            return read_set_dst_arg(rd) | read_set_src_arg(rs)
        case src.Call(rs, arity, _):
            fun_arg_regs: set[Node] = set(FUNCTION_ARG_REGISTERS[:arity])
            return fun_arg_regs | read_set_src_arg(rs)
        case src.Instr2(_, rd, rs1, rs2):
            return read_set_dst_arg(rd) | read_set_src_arg(rs1) | read_set_src_arg(rs2)
        case src.Branch(_, rs1, rs2, rs3):
            return read_set_src_arg(rs1) | read_set_src_arg(rs2) | read_set_src_arg(rs3)
        case src.Jump(rs):
            return read_set_src_arg(rs)

# the write set of an instruction
def write_set(i: src.Instr) -> set[Node]:
    match i:
        case src.Move(rd, rs):
            return write_set_dst_arg(rd) | write_set_src_arg(rs)
        case src.Call(rs, _, _):
            call_svd_regs: set[Node] = set(CALLER_SAVED_REGISTERS) 
            return call_svd_regs | write_set_src_arg(rs)
        case src.Instr2(_, rd, rs1, rs2):
            return write_set_dst_arg(rd) | write_set_src_arg(rs1) | write_set_src_arg(rs2)
        case src.Branch(_, rs1, rs2, rs3):
            return write_set_src_arg(rs1) | write_set_src_arg(rs2) | write_set_src_arg(rs3)
        case src.Jump(rs):
            return write_set_src_arg(rs)

def control_flow_graph(p: src.Blocks) -> DirectedGraph[Label]:
    cfg: DirectedGraph[Label] = DirectedGraph()
    for source, block in p.items():
        match block:
            case [*_, src.Jump(target)]:
                cfg.add_edge(source, target)
            case _:
                pass
        match block:
            case [*_, src.Branch(_, _, _, target), _]:
                cfg.add_edge(source, target)
            case _:
                pass
    return cfg

@dataclass
class BlockLiveness:
    block_in: set[Node]
    instr_out: list[set[Node]]

# Liveness information for the blocks inside a function definitions
type FunLiveness = dict[Label, BlockLiveness]

def debug_print_liveness(liveness: FunLiveness, p: src.Blocks) -> None:
    print("–– LIVENESS ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––")
    for label, block in p.items():
        print(f"{label}:")
        print(f"\t  {liveness[label].block_in}")
        for i, live in zip(block, liveness[label].instr_out):
            print(f"{src.pretty_instr(i)}")
            print(f"\t  {live}")
    print("––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––")

def liveness_analysis(p: src.Blocks, cfg: DirectedGraph[Label]) -> FunLiveness:
    liveness = {lab: BlockLiveness(set(), [set() for _ in b]) for lab, b in p.items()}
    liveness[Label("exit")] = BlockLiveness(set(), [])
    queue = deque(cfg.nodes())
    while queue:
        label = queue.pop()
        prev_live_block_in = liveness[label].block_in.copy()
        cur_live_out: set[Node] = reduce(
            set.union, (liveness[ln].block_in for ln in cfg.neighbors_out(label)), set()
        )
        if label in p:
            for i, instr in reversed(list(enumerate(p[label]))):
                liveness[label].instr_out[i] = cur_live_out
                cur_live_out = (cur_live_out - write_set(instr)) | read_set(instr)
        if cur_live_out != prev_live_block_in:
            liveness[label].block_in = cur_live_out
            queue.extend(cfg.neighbors_in(label))
    return liveness

def build_interference_graph(p: src.Blocks, liveness: FunLiveness) -> UndirectedGraph[Node]:
    graph: UndirectedGraph[Node] = UndirectedGraph()

    for label, block in p.items():
        for i, instr in enumerate(block):
            r = read_set(instr)
            w = write_set(instr)

            for x in r | w:
                graph.add_node(x)

            live_out = liveness[label].instr_out[i]

            match instr:
                case src.Call(Label(l), _) if l not in ["print_int64", "input_int64"]:
                    # Cause all live variables to be spilled during
                    # garbage collection by adding interference with
                    # all registers. User functions are also included
                    # because they may trigger garbage collection.
                    for x in live_out:
                        for ro in REG_ORDER:
                            graph.add_edge(x, ro)
                case src.Move(d, s):
                    for x in live_out:
                        if x != d and x != s:
                            for y in w:
                                graph.add_edge(y, x)
                case _:
                    for d in w:
                        for x in live_out:
                            if x != d:
                                graph.add_edge(d, x)

    return graph

def color_graph(graph: UndirectedGraph[Node]) -> dict[Id, Color]:
    colors: dict[Id, Color] = {}
    saturation: dict[Id, set[Color]] = {n: set() for n in graph.nodes() if type(n) is Id}
    queue: PriorityQueue[Id] = PriorityQueue()

    for n in graph.nodes():
        match n:
            case src.Id(_):
                for x in graph.neighbors(n):
                    match x:
                        case Register(_):
                            saturation[n] |= {REGISTER_TO_COLOR[x]}
                        case _:
                            pass
                queue.push(n, len(saturation[n]))

    while queue:
        head = queue.pop()
        sat = saturation[head]
        color = next(x for x in count() if x not in sat)

        for x in graph.neighbors(head):
            match x:
                case src.Id(_):
                    if color not in saturation[x]:
                        queue.increment(x)
                        saturation[x] |= {color}

        colors[head] = color

    return colors

def assign_locations(is_main: bool, coloring: dict[Id, Color]) -> RegAllocOutput:
    env: dict[Id, Register | tgt.Offset] = {}
    offset: int = 16
    callee_saved: set[Register] = set()
    if is_main:
        callee_saved = set(CALLEE_SAVED_REGISTERS) - {fp, sp}
    else:
        for color in coloring.values():
            if color in COLOR_TO_REGISTER:
                reg = COLOR_TO_REGISTER[color]
                if reg in CALLEE_SAVED_REGISTERS:
                    callee_saved.add(reg)

    offset += len(callee_saved) * 8

    mapping: dict[Color, tgt.Offset] = {}

    for id, color in coloring.items():
        if color in COLOR_TO_REGISTER:
            env[id] = COLOR_TO_REGISTER[color]
        else:
            if color in mapping:
                env[id] = mapping[color]
            else: 
                offset += 8
                off = tgt.Offset(fp, -offset)
                env[id] = off
                mapping[color] = off

    return RegAllocOutput(env, offset, callee_saved)
