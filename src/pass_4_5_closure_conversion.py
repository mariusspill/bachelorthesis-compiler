import ast_4_conv_ass as src
import ast_5_closures as tgt
from identifier import Id
from label import Label
from types_ import *
from util.immutable_list import *

def closure_conv(p: src.Program) -> tgt.Program:
    decls_out: list[tgt.Decl] = []
    for d in p:
        closure_conv_decl(decls_out, d)
    return IList(decls_out)

def closure_conv_decl(decls_out: list[tgt.Decl], d: src.Decl) -> None:
    match d:
        case src.DFun(name, params, body):
            new_params = ilist(Id.fresh("closure")) + params
            new_body = closure_conv_stmts(decls_out, body)
            decls_out.append(tgt.DFun(name, new_params, new_body))

def closure_conv_stmts(decls_out: list[tgt.Decl], ss: IList[src.Stmt]) -> IList[tgt.Stmt]:
    return IList([closure_conv_stmt(decls_out, s) for s in ss])

def closure_conv_stmt(decls_out: list[tgt.Decl], s: src.Stmt) -> tgt.Stmt:
    match s:
        case src.SExpr(e):
            e_out = closure_conv_expr(decls_out, e)
            return tgt.SExpr(e_out)
        case src.SPrint(e):
            e_out = closure_conv_expr(decls_out, e)
            return tgt.SPrint(e_out)
        case src.SAssign(lhs, e):
            lhs_out = closure_conv_lhs(decls_out, lhs)
            e_out = closure_conv_expr(decls_out, e)
            return tgt.SAssign(lhs_out, e_out)
        case src.SIf(e, b1, b2):
            e_out = closure_conv_expr(decls_out, e)
            b1_out = closure_conv_stmts(decls_out, b1)
            b2_out = closure_conv_stmts(decls_out, b2)
            return tgt.SIf(e_out, b1_out, b2_out)
        case src.SWhile(e, b):
            e_out = closure_conv_expr(decls_out, e)
            b_out = closure_conv_stmts(decls_out, b)
            return tgt.SWhile(e_out, b_out)
        case src.SReturn(e):
            e_out = closure_conv_expr(decls_out, e)
            return tgt.SReturn(e_out)

def closure_conv_lhs(decls_out: list[tgt.Decl], lhs: src.Lhs) -> tgt.Lhs:
    match lhs:
        case src.LId(x):
            return tgt.LId(x)
        case src.LSubscript(e, i):
            return tgt.LSubscript(closure_conv_expr(decls_out, e), i)

def closure_conv_expr(decls_out: list[tgt.Decl], e: src.Expr) -> tgt.Expr:
    match e:
        case src.EConst(c, size):
            return tgt.EConst(c, size)
        case src.EVar(x):
            return tgt.EVar(x)
        case src.EInput():
            return tgt.EInput()
        case src.EOp1(op, e1):
            e1_out = closure_conv_expr(decls_out, e1)
            return tgt.EOp1(op, e1_out)
        case src.EOp2(e1, op, e2):
            e1_out = closure_conv_expr(decls_out, e1)
            e2_out = closure_conv_expr(decls_out, e2)
            return tgt.EOp2(e1_out, op, e2_out)
        case src.EIf(e1, e2, e3):
            e1_out = closure_conv_expr(decls_out, e1)
            e2_out = closure_conv_expr(decls_out, e2)
            e3_out = closure_conv_expr(decls_out, e3)
            return tgt.EIf(e1_out, e2_out, e3_out)
        case src.ETuple(es):
            return tgt.ETuple(closure_conv_exprs(decls_out, es))
        case src.ETupleAccess(e, i):
            return tgt.ETupleAccess(closure_conv_expr(decls_out, e), i)
        case src.ETupleLen(e):
            return tgt.ETupleLen(closure_conv_expr(decls_out, e))
        case src.ECall(e_func, e_args):
            e_func_out = closure_conv_expr(decls_out, e_func)
            e_args_out = closure_conv_exprs(decls_out, e_args)
            tmp = Id.fresh("closure")
            return tgt.EBegin(
                ilist(tgt.SAssign(tgt.LId(tmp), e_func_out)),
                tgt.ECall(tgt.ETupleAccess(tgt.EVar(tmp), 0), ilist(tgt.EVar(tmp)) + e_args_out),
            )
        case src.EFunRef(name):
            return tgt.ETuple(ilist(tgt.EFunRef(name)))
        case src.ELambda(params, body, fvs):
            fun_name = Label.fresh("lambda")
            closure_name = Id.fresh("closure")

            closure_args: IList[tgt.Expr] = ilist(tgt.EFunRef(fun_name))
            fun_body: IList[tgt.Stmt] = ilist()

            # Extract free variables from new closure parameter
            for i, x in enumerate(fvs):
                fun_body += ilist(
                    tgt.SAssign(tgt.LId(x), tgt.ETupleAccess(tgt.EVar(closure_name), i+1))
                )
                closure_args += ilist(tgt.EVar(x))

            fun_body += ilist(tgt.SReturn(closure_conv_expr(decls_out, body)))
            new_params = ilist(closure_name) + params
            decls_out.append(tgt.DFun(fun_name, new_params, fun_body))

            return tgt.ETuple(closure_args)

def closure_conv_exprs(decls_out: list[tgt.Decl], es: IList[src.Expr]) -> IList[tgt.Expr]:
    return IList([closure_conv_expr(decls_out, e) for e in es])
