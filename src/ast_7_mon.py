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
type Op2Comp = Literal["==", "!=", "<=", "<", ">", ">="]

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

type Expr = ExprAtom | EOp1 | EOp2Arith | EOp2Comp | EInput \
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

type Stmt = SPrint | SAssign | SIf | SWhile | SCollect | SReturn

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
    body: IList[Stmt]
    orelse: IList[Stmt]

@dataclass(frozen=True)
class SWhile:
    test_body: IList[Stmt]
    test_expr: EOp2Comp
    loop_body: IList[Stmt]

@dataclass(frozen=True)
class SCollect:
    num_bytes: int

@dataclass(frozen=True)
class SReturn:
    e: Expr

# Declarations

type Decl = DFun

# Function Definition
@dataclass(frozen=True)
class DFun:
    name: Label
    params: IList[Id]
    body: IList[Stmt]

# Programs

type Program = IList[Decl]

# Pretty Printing

def indent(s: str) -> str:
    return "\n".join(4 * " " + l for l in s.splitlines())

def pretty(p: Program) -> str:
    return "\n\n".join(pretty_decl(d) for d in p)

def pretty_decl(d: Decl) -> str:
    match d:
        case DFun(name, params, body):
            params_str = ", ".join(str(x) for x in params)
            return f"def {name}({params_str}):\n" + \
                   indent(pretty_stmts(body))

def pretty_stmts(ss: IList[Stmt]) -> str:
    return "\n".join(pretty_stmt(s) for s in ss)

def pretty_stmt(s: Stmt) -> str:
    match s:
        case SAssign(lhs, e):
            return pretty_lhs(lhs) + " = " + pretty_expr(e)
        case SPrint(e):
            return "print(" + pretty_expr(e) + ")"
        case SIf(test, body, orelse):
            return f"if {pretty_expr(test)}:\n" \
                   f"{indent(pretty_stmts(body))}\n" \
                   f"else:\n" \
                   f"{indent(pretty_stmts(orelse))}"
        case SWhile(test_body, test_expr, loop_body):
            if len(test_body) > 0:
                test_body_str = "".join(pretty_stmt(s) + "\n" for s in test_body)
                return (
                    "while {\n" +
                    indent(test_body_str + pretty_expr(test_expr)) + "\n" +
                    "}:\n" +
                    indent(pretty_stmts(loop_body))
                )
            else:
                return (
                    "while { " + pretty_expr(test_expr) + " }:\n" +
                    indent(pretty_stmts(loop_body))
                )
        case SCollect(num_words):
            return f"collect({num_words})"
        case SReturn(e):
            return f"return {pretty_expr(e)}"

def pretty_lhs(lhs: Lhs) -> str:
    match lhs:
        case LId(x):
            return str(x)
        case LSubscript(e, i):
            return f"{pretty_expr(e)}[{i}]"

def pretty_expr(e: Expr) -> str:
    match e:
        case EVar(x):
            return str(x)
        case EConst(x, size):
            return str(x) + ("" if size == "64bit" else "°")
        case EOp1(op, e):
            return f"{op} {pretty_expr(e)}"
        case EOp2Arith(e1, op, e2) | EOp2Comp(e1, op, e2):
            return f"({pretty_expr(e1)} {op} {pretty_expr(e2)})"
        case EInput():
            return "input_int()"
        case ETupleAccess(e, i):
            return f"{pretty_expr(e)}[{i}]"
        case ETupleLen(e):
            return f"len({pretty_expr(e)})"
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
        case EFunRef(name):
            return f"{name}"
