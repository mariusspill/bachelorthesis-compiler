# The interesting parts happen at function declarations and function calls

import ast_5_closures as src
import ast_5_closures as tgt
from identifier import Id
from types_ import *
from util.immutable_list import *

def limit(p: src.Program) -> tgt.Program:
    return IList([limit_decl(d) for d in p])

def limit_decl(d: src.Decl) -> tgt.Decl:
    match d:
        case src.DFun(name, params, body):
            if len(params) > 8:
                first_params = params[:7]
                rest_params = params[7:]
                rest_param = Id("params:rest")
                params = first_params + ilist(rest_param)
                new_stmts = IList([
                    tgt.SAssign(tgt.LId(x), tgt.ETupleAccess(tgt.EVar(rest_param), i))
                    for (i, x) in enumerate(rest_params)
                ])
                body = new_stmts + body
            return tgt.DFun(name, params, limit_stmts(body))

def limit_stmts(ss: IList[src.Stmt]) -> IList[tgt.Stmt]:
    return IList([limit_stmt(s) for s in ss])

def limit_stmt(s: src.Stmt) -> tgt.Stmt:
    match s:
        case src.SExpr(e):
            e_out = limit_expr(e)
            return tgt.SExpr(e_out)
        case src.SPrint(e):
            e = limit_expr(e)
            return tgt.SPrint(e)
        case src.SAssign(lhs, e):
            e_out = limit_expr(e)
            lhs = limit_lhs(lhs)
            return tgt.SAssign(lhs, e_out)
        case src.SIf(e, b1, b2):
            e_out = limit_expr(e)
            b1_out = limit_stmts(b1)
            b2_out = limit_stmts(b2)
            return tgt.SIf(e_out, b1_out, b2_out)
        case src.SWhile(e, b):
            e_out = limit_expr(e)
            b_out = limit_stmts(b)
            return tgt.SWhile(e_out, b_out)
        case src.SReturn(e):
            e_out = limit_expr(e)
            return tgt.SReturn(e_out)

def limit_lhs(lhs: src.Lhs) -> tgt.Lhs:
    match lhs:
        case src.LId(x):
            return tgt.LId(x)
        case src.LSubscript(e, i):
            return tgt.LSubscript(limit_expr(e), i)

def limit_expr(e: src.Expr) -> tgt.Expr:
    match e:
        case src.EConst(c, size):
            return tgt.EConst(c, size)
        case src.EVar(x):
            return tgt.EVar(x)
        case src.EInput():
            return tgt.EInput()
        case src.EOp1(op, e1):
            e1_out = limit_expr(e1)
            return tgt.EOp1(op, e1_out)
        case src.EOp2(e1, op, e2):
            e1_out = limit_expr(e1)
            e2_out = limit_expr(e2)
            return tgt.EOp2(e1_out, op, e2_out)
        case src.EIf(e1, e2, e3):
            e1_out = limit_expr(e1)
            e2_out = limit_expr(e2)
            e3_out = limit_expr(e3)
            return tgt.EIf(e1_out, e2_out, e3_out)
        case src.ETuple(es):
            return tgt.ETuple(limit_exprs(es))
        case src.ETupleAccess(e, i):
            return tgt.ETupleAccess(limit_expr(e), i)
        case src.ETupleLen(e):
            return tgt.ETupleLen(limit_expr(e))
        case src.ECall(e_func, e_args):
            if len(e_args) > 8:
                e_args = e_args[:7] + ilist(tgt.ETuple(e_args[7:]))
            return tgt.ECall(limit_expr(e_func), limit_exprs(e_args))
        case src.EFunRef(name):
            return tgt.EFunRef(name)
        case src.EBegin(ss, e):
            return tgt.EBegin(limit_stmts(ss), limit_expr(e))

def limit_exprs(es: IList[src.Expr]) -> IList[tgt.Expr]:
    return IList([limit_expr(e) for e in es])

