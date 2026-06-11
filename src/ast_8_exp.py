from dataclasses import dataclass
from typing import Literal


from identifier import Id
from label import Label
from types_ import *
from util.immutable_list import IList

# Unary Operators

type Op1 = Literal["-", "not"]

# Binary Operators

type Op2Arith = Literal["+", "-"]

# Atomic Expressions

type ExprAtom = EConst | EVar

@dataclass(frozen=True)
class EConst:
    value: int | bool | None
    size: Literal['64bit', '63bit']

@dataclass(frozen=True)
class EVar:
    name: Id

# Complex Expressions

type Expr = ExprAtom | EOp1 | EOp2Arith | EInput | EOp2Comp \
          | ETupleAccess | ETupleLen | EAllocate | EGlobal \
          | ECall | EFunRef

@dataclass(frozen=True)
class EOp1:
    op: Op1
    operand: ExprAtom

@dataclass(frozen=True)
class EOp2Arith:
    left: ExprAtom
    op: Op2Arith
    right: ExprAtom

@dataclass(frozen=True)
class EInput:
    pass

type Op2Comp = Literal["==", "!=", "<=", "<", ">", ">="]

@dataclass(frozen=True)
class EOp2Comp:
    left: ExprAtom
    cmp: Op2Comp
    right: ExprAtom

@dataclass(frozen=True)
class ETupleAccess:
    e: ExprAtom
    index: int

@dataclass(frozen=True)
class ETupleLen:
    e: ExprAtom

@dataclass(frozen=True)
class EAllocate:
    num_elems: int

type Global = Literal['gc_free_ptr', 'gc_fromspace_end']

@dataclass(frozen=True)
class EGlobal:
    var: Global

@dataclass(frozen=True)
class ECall:
    fun: ExprAtom
    args: IList[ExprAtom]

@dataclass(frozen=True)
class EFunRef:
    fun: Label

# Left-hand sides of Assign Statements

type Lhs = LId | LSubscript

@dataclass
class LId:
    id: Id

@dataclass
class LSubscript:
    e: ExprAtom
    offset: int

# Statements

type Stmt = SPrint | SAssign | SIf | SGoto | SCollect | SReturn | STailCall

@dataclass(frozen=True)

class SPrint:
    expr: ExprAtom

@dataclass(frozen=True)
class SAssign:
    lhs: Lhs
    rhs: Expr

@dataclass(frozen=True)
class SIf:
    test: EOp2Comp
    body: Label
    orelse: Label

@dataclass(frozen=True)
class SGoto:
    target: Label

@dataclass(frozen=True)
class SCollect:
    num_bytes: int

@dataclass(frozen=True)
class SReturn:
    e: ExprAtom

@dataclass(frozen=True)
class STailCall:
    func: ExprAtom
    args: IList[ExprAtom]

# Basic Blocks

type Block = IList[Stmt]
type Blocks = dict[Label, Block]

# Declarations

type Decl = DFun

# Function Definition
@dataclass(frozen=True)
class DFun:
    name: Label
    params: IList[Id]
    start_label: Label
    end_label: Label
    body: Blocks

# Programs

type Program = IList[Decl]

# Pretty Printing

def indent(s: str) -> str:
    return "\n".join(4 * " " + l for l in s.splitlines())

def pretty(p: Program) -> str:
    return "\n\n".join(pretty_decl(d) for d in p)

def pretty_decl(d: Decl) -> str:
    match d:
        case DFun(name, params, start_label, end_label, body):
            params_str = ", ".join(
                str(x)
                for x in params
            )
            body_str = "\n".join(
                f"{lab}:\n\t" + pretty_block(block)
                for lab, block in body.items()
            )
            return f"def {name}({params_str}):\n" + indent(
                f"START_LABEL: {start_label}\n" +
                f"END_LABEL: {end_label}\n" +
                body_str
            )

def pretty_block(p: Block) -> str:
    return "\n\t".join(pretty_stmt(s) for s in p)

def pretty_lhs(lhs: Lhs) -> str:
    match lhs:
        case LId(x):
            return str(x)
        case LSubscript(e, i):
            return f"{pretty_expr(e)}[{i}]"

def pretty_stmt(s: Stmt) -> str:
    match s:
        case SAssign(lhs, e):
            return pretty_lhs(lhs) + " = " + pretty_expr(e)
        case SPrint(e):
            return f"print({pretty_expr(e)})"
        case SIf(e, l1, l2):
            return f"if {pretty_expr(e)} {{ goto {l1} }} else {{ goto {l2} }}"
        case SGoto(l):
            return f"goto {l}"
        case SCollect(n):
            return f"collect({n})"
        case SReturn(e):
            return f"return {pretty_expr(e)}"
        case STailCall(e_func, e_args):
            e_args_str = ", ".join(pretty_expr(e) for e in e_args)
            return f"tail_call({pretty_expr(e_func)}, {e_args_str})"

def pretty_expr(e: Expr) -> str:
    match e:
        case EVar(x):
            return str(x)
        case EConst(x, size):
            return str(x) + ("" if size == "64bit" else "°")
        case EOp1("not", e):
            return f"not {pretty_expr(e)}"
        case EOp1(op, e):
            return f"{op}{pretty_expr(e)}"
        case EOp2Arith(e1, op, e2):
            return f"({pretty_expr(e1)} {op} {pretty_expr(e2)})"
        case EInput():
            return "input_int()"
        case EOp2Comp(e1, op, e2):
            return f"({pretty_expr(e1)} {op} {pretty_expr(e2)})"
        case EGlobal(g):
            return "@" + g
        case EAllocate(n):
            return f"allocate({n})"
        case ETupleAccess(e, i):
            return f"{pretty_expr(e)}[{i}]"
        case ETupleLen(e):
            return f"len({pretty_expr(e)})"
        case ECall(func, args):
            args_str = ", ".join(pretty_expr(e) for e in args)
            return f"{pretty_expr(func)}({args_str})"
        case EFunRef(label):
            return f"{label}"
