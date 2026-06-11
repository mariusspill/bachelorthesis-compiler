import ast_3_revealed as src
import ast_4_conv_ass as tgt
from identifier import Id
from types_ import *
from util.immutable_list import *

def conv_ass(p: src.Program) -> tgt.Program:
    return IList([conv_ass_decl(d) for d in p])

def conv_ass_decl(d: src.Decl) -> tgt.Decl:
    match d:
        case src.DFun(name, params, body):
            # Analyse variables that need boxing
            fvs = free_in_lambda_stmts(body)
            avs = assigned_vars_stmts(body) | set(params)
            AF = fvs.intersection(avs)

            new_body: IList[tgt.Stmt] = ilist()

            # Create boxes for the variables
            for x in AF:
                if x in params:
                    e: tgt.Expr = tgt.EVar(x)
                else:
                    e = tgt.EConst(0, '64bit')
                new_body += ilist(tgt.SAssign(tgt.LId(x), tgt.ETuple(ilist(e))))

            # Replace all uses of the variables with subscripts into the boxes
            new_body += conv_ass_stmts(AF, body)

            return tgt.DFun(name, params, new_body)

def conv_ass_stmts(AF: set[Id], ss: IList[src.Stmt]) -> IList[tgt.Stmt]:
    return IList([conv_ass_stmt(AF, s) for s in ss])

def conv_ass_stmt(AF: set[Id], s: src.Stmt) -> tgt.Stmt:
    match s:
        case src.SExpr(e):
            e_out = conv_ass_expr(AF, e)
            return tgt.SExpr(e_out)
        case src.SPrint(e):
            e_out = conv_ass_expr(AF, e)
            return tgt.SPrint(e_out)
        case src.SAssign(x, e):
            if x in AF:
                lhs: tgt.Lhs = tgt.LSubscript(tgt.EVar(x), 0)
            else:
                lhs = tgt.LId(x)
            e_out = conv_ass_expr(AF, e)
            return tgt.SAssign(lhs, e_out)
        case src.SIf(e, b1, b2):
            e_out = conv_ass_expr(AF, e)
            b1_out = conv_ass_stmts(AF, b1)
            b2_out = conv_ass_stmts(AF, b2)
            return tgt.SIf(e_out, b1_out, b2_out)
        case src.SWhile(e, b):
            e_out = conv_ass_expr(AF, e)
            b_out = conv_ass_stmts(AF, b)
            return tgt.SWhile(e_out, b_out)
        case src.SReturn(e):
            e_out = conv_ass_expr(AF, e)
            return tgt.SReturn(e_out)

def conv_ass_expr(AF: set[Id], e: src.Expr) -> tgt.Expr:
    match e:
        case src.EConst(c, size):
            return tgt.EConst(c, size)
        case src.EVar(x):
            if x in AF:
                return tgt.ETupleAccess(tgt.EVar(x), 0)
            else:
                return tgt.EVar(x)
        case src.EInput():
            return tgt.EInput()
        case src.EOp1(op, e1):
            e1_out = conv_ass_expr(AF, e1)
            return tgt.EOp1(op, e1_out)
        case src.EOp2(e1, op, e2):
            e1_out = conv_ass_expr(AF, e1)
            e2_out = conv_ass_expr(AF, e2)
            return tgt.EOp2(e1_out, op, e2_out)
        case src.EIf(e1, e2, e3):
            e1_out = conv_ass_expr(AF, e1)
            e2_out = conv_ass_expr(AF, e2)
            e3_out = conv_ass_expr(AF, e3)
            return tgt.EIf(e1_out, e2_out, e3_out)
        case src.ETuple(es):
            return tgt.ETuple(conv_ass_exprs(AF, es))
        case src.ETupleAccess(e, i):
            return tgt.ETupleAccess(conv_ass_expr(AF, e), i)
        case src.ETupleLen(e):
            return tgt.ETupleLen(conv_ass_expr(AF, e))
        case src.ECall(e_func, e_args):
            return tgt.ECall(conv_ass_expr(AF, e_func), conv_ass_exprs(AF, e_args))
        case src.EFunRef(name):
            return tgt.EFunRef(name)
        case src.ELambda(params, body):
            body_out = conv_ass_expr(AF, body)
            return tgt.ELambda(params, body_out, IList(list(free_vars(e))))

def conv_ass_exprs(AF: set[Id], es: IList[src.Expr]) -> IList[tgt.Expr]:
    return IList([conv_ass_expr(AF, e) for e in es])

def free_vars(e: src.Expr) -> set[Id]:
    match e:
        case src.EConst(_, _):
            return set()
        case src.EVar(x):
            return {x}
        case src.EInput():
            return set()
        case src.EOp1(_, e1):
            return free_vars(e1)
        case src.EOp2(e1, _, e2):
            return free_vars(e1) | free_vars(e2)
        case src.EIf(e1, e2, e3):
            return free_vars(e1) | free_vars(e2) | free_vars(e3)
        case src.ETuple(es):
            return free_vars_list(es)
        case src.ETupleAccess(e, _):
            return free_vars(e)
        case src.ETupleLen(e):
            return free_vars(e)
        case src.ECall(e_func, e_args):
            return free_vars(e_func) | free_vars_list(e_args) 
        case src.EFunRef(_):
            return set()
        case src.ELambda(params, body):
            return free_vars(body) - set(params)

def free_vars_list(es: IList[src.Expr]) -> set[Id]:
    fvs = set()
    for e in es:
        fvs |= free_vars(e)
    return fvs

def free_in_lambda(e: src.Expr) -> set[Id]:
    match e:
        case src.EConst(_, _):
            return set()
        case src.EVar(_):
            return set()
        case src.EInput():
            return set()
        case src.EOp1(_, e1):
            return free_in_lambda(e1)
        case src.EOp2(e1, _, e2):
            return free_in_lambda(e1) | free_in_lambda(e2)
        case src.EIf(e1, e2, e3):
            return free_in_lambda(e1) | free_in_lambda(e2) | free_in_lambda(e3)
        case src.ETuple(es):
            return free_in_lambda_list(es)
        case src.ETupleAccess(e, _):
            return free_in_lambda(e)
        case src.ETupleLen(e):
            return free_in_lambda(e)
        case src.ECall(e_func, e_args):
            return free_in_lambda(e_func) | free_in_lambda_list(e_args) 
        case src.EFunRef(_):
            return set()
        case src.ELambda(_, _):
            return free_vars(e)

def free_in_lambda_list(es: IList[src.Expr]) -> set[Id]:
    fvs = set()
    for e in es:
        fvs |= free_in_lambda(e)
    return fvs

def free_in_lambda_stmt(s: src.Stmt) -> set[Id]:
    match s:
        case src.SExpr(e):
            return free_in_lambda(e)
        case src.SPrint(e):
            return free_in_lambda(e)
        case src.SAssign(_, e):
            return free_in_lambda(e)
        case src.SIf(e, b1, b2):
            return free_in_lambda(e) | free_in_lambda_stmts(b1) | free_in_lambda_stmts(b2)
        case src.SWhile(e, b):
            return free_in_lambda(e) | free_in_lambda_stmts(b)
        case src.SReturn(e):
            return free_in_lambda(e)

def free_in_lambda_stmts(ss: IList[src.Stmt]) -> set[Id]:
    fvs = set()
    for s in ss:
        fvs |= free_in_lambda_stmt(s)
    return fvs

def assigned_vars_stmt(s: src.Stmt) -> set[Id]:
    match s:
        case src.SAssign(x, _):
            return {x}
        case src.SIf(_, body_true, body_false):
            return assigned_vars_stmts(body_true) | assigned_vars_stmts(body_false)
        case src.SWhile(_, body):
            return assigned_vars_stmts(body)
        case _:
            return set()

def assigned_vars_stmts(ss: IList[src.Stmt]) -> set[Id]:
    avs = set()
    for s in ss:
        avs |= assigned_vars_stmt(s)
    return avs
