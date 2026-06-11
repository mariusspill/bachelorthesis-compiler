from dataclasses import dataclass

from register import Register
from label import Label
from types_ import *
from util.immutable_list import IList
import ast_12_riscv as riscv

from ast_12_riscv import (
    Const as Const,
    Offset as Offset,
    Directive as Directive,
    DGlobal as DGlobal,
    RInstrName as RInstrName,
    RInstr as RInstr,
    IInstr2 as IInstr2,
    IInstr1 as IInstr1,
    Load as Load,
    LoadAddress as LoadAddress,
    Store as Store,
    Call as Call,
    CallIndirect as CallIndirect,
    Jump as Jump,
    BranchName as BranchName,
    Branch as Branch,
    Return as Return, 
)


type Instr = riscv.Instr | TailJump | TailJumpIndirect

# Invented instructions for tail calls

@dataclass(frozen=True)
class TailJump:
    target: Label

@dataclass(frozen=True)
class TailJumpIndirect:
    target: Register

# Blocks

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

def pretty_instr(i: Instr) -> str:
    match i:
        case TailJump(r):
            return f"\ttail_jmp\t{r}"
        case TailJumpIndirect(r):
            return f"\ttail_jmp_indirect\t{r}"
        case _:
            return riscv.pretty_instr(i)

