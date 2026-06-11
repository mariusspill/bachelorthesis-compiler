from dataclasses import dataclass

from typing import Literal

from identifier import Id
from label import Label
from types_ import *
from util.immutable_list import IList

# Unary Operators

type Op1 = Literal["-", "not"]

# Binary Operators

type Op2 = Literal["+", "-", "==", "!=", "<=", "<", ">", ">="]

# Expressions

type Expr = EConst | EVar | EOp1 | EOp2 | EInput | EIf \
          | ETuple | ETupleAccess | ETupleLen \
          | ECall | EFunRef | ELambda

@dataclass(frozen=True)
class EConst:
    value: int | bool | None
    size: Literal['64bit', '63bit']

@dataclass(frozen=True)
class EVar:
    name: Id

@dataclass(frozen=True)
class EOp1:
    op: Op1
    operand: Expr

@dataclass(frozen=True)
class EOp2:
    left: Expr
    op: Op2
    right: Expr

@dataclass(frozen=True)
class EInput:
    pass

@dataclass(frozen=True)
class EIf:
    test: Expr
    body: Expr
    orelse: Expr

@dataclass(frozen=True)
class ETuple:
    es: IList[Expr]

@dataclass(frozen=True)
class ETupleAccess:
    e: Expr
    index: int

@dataclass(frozen=True)
class ETupleLen:
    e: Expr

@dataclass(frozen=True)
class ECall:
    fun: Expr
    args: IList[Expr]

@dataclass(frozen=True)
class EFunRef:
    fun: Label

@dataclass(frozen=True)
class ELambda:
    params: IList[Id]
    body: Expr
    fvs: IList[Id]

# Left-hand sides of Assign Statements

type Lhs = LId | LSubscript

@dataclass
class LId:
    id: Id

@dataclass
class LSubscript:
    e: Expr
    offset: int

# Statements

type Stmt = SExpr | SPrint | SAssign | SIf | SWhile | SReturn

@dataclass(frozen=True)
class SExpr:
    e: Expr

@dataclass(frozen=True)
class SPrint:
    e: Expr

@dataclass(frozen=True)
class SAssign:
    lhs: Lhs
    rhs: Expr

@dataclass(frozen=True)
class SIf:
    test: Expr
    body: IList[Stmt]
    orelse: IList[Stmt]

@dataclass(frozen=True)
class SWhile:
    test: Expr
    body: IList[Stmt]

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
        case SExpr(e):
            return pretty_expr(e)
        case SAssign(lhs, e):
            return f"{pretty_lhs(lhs)} = {pretty_expr(e)}"
        case SPrint(e):
            return "print(" + pretty_expr(e) + ")"
        case SIf(test, body, orelse):
            return f"if {pretty_expr(test)}:\n" \
                   f"{indent(pretty_stmts(body))}\n" \
                   f"else:\n" \
                   f"{indent(pretty_stmts(orelse))}"
        case SWhile(test, body):
            return f"while {pretty_expr(test)}:\n{indent(pretty_stmts(body))}"
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
        case EOp2(e1, op, e2):
            return f"({pretty_expr(e1)} {op} {pretty_expr(e2)})"
        case EInput():
            return "input_int()"
        case EIf(test, body, orelse):
            return f"({pretty_expr(body)} if {pretty_expr(test)} else {pretty_expr(orelse)})"
        case ETuple(entries):
            if len(entries) == 1:
                return "(" + pretty_expr(entries[0]) + ",)"
            else:
                return "(" + ", ".join(pretty_expr(e) for e in entries) + ")"
        case ETupleAccess(e, i):
            return f"{pretty_expr(e)}[{i}]"
        case ETupleLen(e):
            return f"len({pretty_expr(e)})"
        case ECall(func, args):
            args_str = ", ".join(pretty_expr(e) for e in args)
            return f"{pretty_expr(func)}({args_str})"
        case EFunRef(name):
            return f"{name}"
        case ELambda(params, body, fvs):
            params_str = ", ".join(str(x) for x in params)
            body_str = pretty_expr(body)
            fvs_str = ", ".join(str(x) for x in fvs)
            return f"lambda[{fvs_str}] {params_str}: {body_str}"
