import ast_9_sel as src
import ast_10_mem as tgt
from register import *
from register_allocation import RegAllocOutput
from util.immutable_list import ilist, IList
from identifier import Id
from label import Label
from register import Register

def assign_homes(p: src.Program, reg_info: dict[Label, RegAllocOutput]) -> tgt.Program:
    return IList([assign_homes_fun(d, reg_info) for d in p])

def assign_homes_fun(f: src.Function, reg_info: dict[Label, RegAllocOutput]) -> tgt.Function:
    return tgt.Function(
        f.entry_label,
        f.start_label,
        f.end_label,
        assign_homes_body(f.body, reg_info[f.entry_label].env),
    )

def assign_homes_body(
    blocks: src.Blocks,
    env: dict[Id, Register | tgt.Offset],
) -> tgt.Blocks:
    out: tgt.Blocks = {}
    for label, block in blocks.items():
        block_out: tgt.Block = ilist()
        for i in block:
            block_out += ilist(assign_homes_instr(env, i))
        out[label] = block_out
    return out

def assign_homes_instr(env: dict[Id, Register | tgt.Offset], i: src.Instr) -> tgt.Instr:
    match i:
        case src.Jump(label):
            return tgt.Jump(label)
        case src.Branch(cc, rs1, rs2, target):
            return tgt.Branch(cc, assign_home_src(env, rs1), assign_home_src(env, rs2), target)
        case src.Move(dst, src_):
            return tgt.Move(assign_home_dst(env, dst), assign_home_src(env, src_))
        case src.Call(src_, _, is_tail_call):
            return tgt.Call(assign_home_src(env, src_), is_tail_call)
        case src.Instr2(op, dst, src1, src2):
            return tgt.Instr2(
                op,
                assign_home_dst(env, dst),
                assign_home_src(env, src1),
                assign_home_src(env, src2),
            )

def assign_home_dst(env: dict[Id, Register | tgt.Offset], arg: src.ArgWrite) -> tgt.ArgWrite:
    match arg:
        case Id(_) as x:
            return assign_home_id(env, x)
        case Register(r):
            return Register(r)
        case src.Offset(e, i):
            match e:
                case Register(r):
                    return tgt.Offset(Register(r), i)
                case Label(l):
                    return tgt.Offset(Label(l), i)
                case Id(_) as x:
                    return tgt.Offset(assign_home_id(env, x), i)

def assign_home_src(env: dict[Id, Register | tgt.Offset], arg: src.ArgRead) -> tgt.ArgRead:
    match arg:
        case src.Const(i, size):
            return tgt.Const(i, size)
        case Label(l):
            return Label(l)
        case _:
            return assign_home_dst(env, arg)

def assign_home_id(env: dict[Id, Register | tgt.Offset], x: Id) -> Register | tgt.Offset:
    if x not in env:
        raise Exception(
            f"Expected {x} to have either a register or stack location assigned!"
        )
    return env[x]
