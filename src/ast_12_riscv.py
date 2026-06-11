from dataclasses import dataclass
from typing import Literal

from register import Register
from label import Label
from util.immutable_list import IList

# Constants

type Const = int

# Offsets

@dataclass(frozen=True)
class Offset:
    reg: Register
    offset: int

# Instructions

type Instr = Label | Load | LoadAddress | Store | RInstr | IInstr2 | IInstr1 \
           | Call | CallIndirect | Jump | JumpIndirect | Return | Branch \
           | Directive | Label

# Assembler Directives

type Directive = DGlobal | DAlign

# .globl LABEL
@dataclass(frozen=True)
class DGlobal:
    label: Label

# .align INT
@dataclass(frozen=True)
class DAlign:
    num_bits: int

# Register Instructions

type RInstrName = Literal["add", "sub", "mul", "div", "and", "xor", "sltu", "slt", "sll", "srl"]

@dataclass(frozen=True)
class RInstr:
    name: RInstrName  # name of the instruction
    rd: Register  # destination register
    rs1: Register  # source register 1
    rs2: Register  # source register 2

# Binary Immediate Instructions

type IInstr2Name = Literal["addi", "xori", "slti", "slli", "srli"]

@dataclass(frozen=True)
class IInstr2:
    name: IInstr2Name  # name of the instruction
    rd: Register  # destination register
    rs: Register  # source register
    imm: int  # immediate value

# Unary Immediate Instructions

type IInstr1Name = Literal["li"]

@dataclass(frozen=True)
class IInstr1:
    name: IInstr1Name  # name of the instruction
    rd: Register  # destination register
    imm: int  # immediate value

# Memory Instructions

# ld DST,SRC
@dataclass(frozen=True)
class Load:
    dst: Register
    src: Offset

# sd SRC,DST
@dataclass(frozen=True)
class Store:
    src: Register
    dst: Offset

# la DST,SRC_LABEL
@dataclass(frozen=True)
class LoadAddress:
    dst: Register
    src: Label

# Control Flow Instructions

# call
@dataclass(frozen=True)
class Call:
    target: Label

# jalr register
# short for:
# jalr ra, register, 0
@dataclass(frozen=True)
class CallIndirect:
    target: Register

# j label
# short for:
# jal zero, label, 0
@dataclass(frozen=True)
class Jump:
    label: Label

# jr register
# short for:
# jalr zero, register, 0
@dataclass(frozen=True)
class JumpIndirect:
    label: Register
    offset: int

# Branch Instructions
type BranchName =  Literal["beq", "bne", "blt", "bge"]

@dataclass(frozen=True)
class Branch:
    cc: BranchName # name of the comparison
    rs1: Register  # source register 1
    rs2: Register  # source register 2
    target: Label  # target block

# ret
@dataclass(frozen=True)
class Return:
    pass

# Programs

type Program = IList[Instr]

# Pretty Printing

def pretty_arg(a: Register | Offset | Const | Label) -> str:
    match a:
        case Register(r):
            return r
        case Offset(r, o):
            return f"{o}({r.name})"
        case Label(l):
            return f"{l}"
        case int(i):
            return f"{i}"

def pretty_instr(i: Instr) -> str:
    match i:
        case Jump(label):
            return f"\tj\t{label}"
        case JumpIndirect(r, offset):
            return f"\tjr\t{r}, {offset}"
        case Branch(cc, src1, src2, target):
            return f"\t{cc}\t{pretty_arg(src1)},{pretty_arg(src2)},{target}"
        case Label(l):
            return f"{l}: "
        case Load(dst, src):
            return f"\tld\t{pretty_arg(dst)},{pretty_arg(src)}"
        case LoadAddress(dst, src):
            return f"\tla\t{pretty_arg(dst)},{pretty_arg(src)}"
        case Store(dst, src):
            return f"\tsd\t{pretty_arg(dst)},{pretty_arg(src)}"
        case RInstr(nm, dst, src1, src2):
            return f"\t{nm}\t{pretty_arg(dst)},{pretty_arg(src1)},{pretty_arg(src2)}"
        case IInstr2(nm, dst, src, imm):
            return f"\t{nm}\t{pretty_arg(dst)},{pretty_arg(src)},{pretty_arg(imm)}"
        case IInstr1(nm, dst, imm):
            return f"\t{nm}\t{pretty_arg(dst)},{pretty_arg(imm)}"
        case Call(l):
            return f"\tcall\t{l}"
        case CallIndirect(r):
            return f"\tjalr\t{r}"
        case Return():
            return "\tret"
        case DGlobal(l):
            return f"\n\t.globl\t{l}"
        case DAlign(n):
            return f"\t.align\t{n}"
        case Label(l):
            return f"{l}:"

def pretty(p: Program) -> str:
    return "\n".join(pretty_instr(i) for i in p)
