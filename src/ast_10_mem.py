from dataclasses import dataclass
from typing import Literal

from register import Register
from label import Label
from types_ import *
from util.immutable_list import IList

# Integer and Boolean Constants

@dataclass
class Const:
    value: int
    size: Literal['63bit', '64bit']

# Arguments

type ArgWrite = Register | Offset
type ArgRead = ArgWrite | Label | Const

# Instructions
type Instr = Move | Call | Instr2 | Jump | Branch

@dataclass(frozen=True)
class Offset:
    reg: 'Register | Label | Offset'
    offset: int

    def __str__(self) -> str:
        return f"{self.offset}({self.reg})"

# Move Instruction

@dataclass(frozen=True)
class Move:
    dst: ArgWrite
    src: ArgRead

# Call Instruction

@dataclass(frozen=True)
class Call:
    label: ArgRead
    ty: Literal['normal', 'tail call'] # whether to do a tail-call or not

@dataclass(frozen=True)
class Jump:
    label: Label

@dataclass(frozen=True)
class Branch:                                  # no reason to use them
    name: Literal["beq", "bne", "blt", "bge"]  # name of the comparison
    src1: ArgRead
    src2: ArgRead
    target: Label

# Binary Instructions

type Instr2Name = Literal["add", "sub", "mul", "div", "xor", "sltu", "slt", "and", "sll", "srl"]

@dataclass(frozen=True)
class Instr2:
    name: Instr2Name
    dst: ArgWrite
    src1: ArgRead
    src2: ArgRead

# Basic Blocks

type Block = IList[Instr]
type Blocks = dict[Label, Block]

# Functions

@dataclass(frozen=True)
class Function:
    entry_label: Label
    start_label: Label
    end_label: Label
    body: Blocks

# Programs

type Program = IList[Function]

# Pretty Printing

def indent(s: str) -> str:
    return "\n".join(4 * " " + l for l in s.splitlines())

def pretty(p: Program) -> str:
    return "\n\n".join(pretty_fun(d) for d in p)

def pretty_fun(f: Function) -> str:
    body_str = "\n".join(
        f"{lab}:\n" + pretty_block(block)
        for lab, block in f.body.items()
    )
    return f"def {f.entry_label}:\n" + indent(
        f"START_LABEL: {f.start_label}\n" +
        f"END_LABEL: {f.end_label}\n" +
        body_str
    )

def pretty_block(b: Block) -> str:
    return "\n".join([pretty_instr(i) for i in b])

def pretty_instr(i: Instr) -> str:  # type:ignore
    match i:
        case Move(dst, src):
            return f"\tmv\t{pretty_arg(dst)}, {pretty_arg(src)}"
        case Call(l, "normal"):
            return f"\tcall\t{l}"
        case Call(l, "tail call"):
            return f"\ttail_call\t{l}"
        case Instr2(nm, dst, src1, src2):
            return f"\t{nm}\t{pretty_arg(dst)}, {pretty_arg(src1)}, {pretty_arg(src2)}"
        case Jump(label):
            return f"\tj\t{label}"
        case Branch(cc, src1, src2, target):
            return f"\t{cc}\t{pretty_arg(src1)}, {pretty_arg(src2)}, {target}"

def pretty_arg(a: ArgRead) -> str:
    match a:
        case Register(r):
            return r
        case Offset(ro, o):
            return f"{o}({pretty_arg(ro)})"
        case Const(x, size):
            return str(x) + ("" if size == "64bit" else "°")
        case Label(l):
            return l
