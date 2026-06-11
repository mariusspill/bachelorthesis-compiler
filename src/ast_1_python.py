from dataclasses import dataclass

from typing import Literal, cast, Optional

from identifier import Id
from types_ import *
from util.immutable_list import IList

# Unary Operators

type Op1 = Literal["-", "not"]

# Binary Operators

type Op2 = Literal["+", "-", "==", "!=", "<=", "<", ">", ">=", "and", "or", "is"]

# Expressions

type Expr = EConst | EVar | EOp1 | EOp2 | EInput | EIf \
          | ETuple | ETupleAccess | ETupleLen \
          | ECall | ELambda | EField

@dataclass(frozen=True)
class EConst:
    value: int | bool | None

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
class ELambda:
    params: IList[Id]
    body: Expr

@dataclass
class EField:
    e: Expr
    name: Id
    idx: int | None = None  # set during type checking: indicates the position of this field in the class

# Statements

type Stmt = SExpr | SPrint | SAssign | SIf | SWhile | SReturn | SClass

@dataclass(frozen=True)
class SExpr:
    expr: Expr

@dataclass(frozen=True)
class SPrint:
    expr: Expr

@dataclass(frozen=True)
class SAssign:
    lhs: Id
    ty: Optional[Type]
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

@dataclass(frozen=True)
class SClass:
    name: Id
    fields: IList[tuple[Id, Type]]

# Declarations

type Decl = DFun

# Function Definition
@dataclass(frozen=True)
class DFun:
    name: Id
    params: IList[tuple[Id, Type]]
    ret_ty: Type
    body: IList[Stmt]

# Programs

@dataclass
class Program:
    body: IList[Decl | Stmt]

# Pretty Printing

def indent(s: str) -> str:
    return "\n".join(4 * " " + l for l in s.splitlines())

def pretty(p: Program) -> str:
    return "\n".join(pretty_decl_or_stmt(d) for d in p.body)

def pretty_decl_or_stmt(d: Decl | Stmt) -> str:
    match d:
        case DFun(name, params, ret_ty, body):
            params_str = ", ".join(f"{x}: {pretty_type(t)}" for (x, t) in params)
            return f"def {name}({params_str}) -> {pretty_type(ret_ty)}:\n" + \
                   indent(pretty_stmts(body)) + "\n"
        case stmt:
            return pretty_stmt(stmt)

def pretty_stmts(ss: IList[Stmt]) -> str:
    return "\n".join(pretty_stmt(s) for s in ss)

def pretty_stmt(s: Stmt) -> str:
    match s:
        case SExpr(e):
            return pretty_expr(e)
        case SAssign(x, t, e):
            if t is None:
                return f"{x} = {pretty_expr(e)}"
            else:
                return f"{x}: {pretty_type(t)} = {pretty_expr(e)}"
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
        case SClass(name, fields):
            field_str = "\n".join(f"{x}: {pretty_type(t)}" for (x, t) in fields)
            return f"class {name}:\n{indent(field_str)}\n"

def pretty_expr(e: Expr) -> str:
    match e:
        case EConst(x) | EVar(x):
            return str(x)
        case EOp1(op, e):
            return f"{op} {pretty_expr(e)}"
        case EOp2(e1, op, e2):
            return f"({pretty_expr(e1)} {op} {pretty_expr(e2)})"
        case EInput():
            return "input_int()"
        case EIf(test, body, orelse):
            return f"({pretty_expr(body)} if {pretty_expr(test)} else {pretty_expr(orelse)})"
        case ETuple(entries):
            return "(" + ", ".join(pretty_expr(e) for e in entries) + ")"
        case ETupleAccess(e, i):
            return f"{pretty_expr(e)}[{i}]"
        case ETupleLen(e):
            return f"len({pretty_expr(e)})"
        case ECall(func, args):
            args_str = ", ".join(pretty_expr(e) for e in args)
            return f"{pretty_expr(func)}({args_str})"
        case ELambda(params, body):
            params_str = ", ".join(str(x) for x in params)
            body_str = pretty_expr(body)
            return f"lambda {params_str}: {body_str}"
        case EField(e, name, _):
            return f"{pretty_expr(e)}.{name}"

def pretty_anything(x: Program | Decl | Stmt | Expr) -> str:
    try:
        y = pretty(cast(Program, x))
        if y is None:
            raise Exception("not it")
        return y
    except:
        pass

    try:
        y = pretty_decl_or_stmt(cast(Decl, x))
        if y is None:
            raise Exception("not it")
        return y
    except:
        pass

    try:
        y = pretty_stmt(cast(Stmt, x))
        if y is None:
            raise Exception("not it")
        return y
    except:
        pass

    return pretty_expr(cast(Expr, x))
