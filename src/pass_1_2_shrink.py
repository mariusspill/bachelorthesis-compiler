import ast_1_python as src
import ast_2_shrunk as tgt
from types_ import *
from util.immutable_list import *
from identifier import Id

def shrink(p: src.Program) -> tgt.Program:
    out: IList[tgt.Decl] = ilist()
    stmts: IList[src.Stmt] = ilist()
    for d in p.body:
        match d:
            case src.DFun():
                out += ilist(shrink_decl(d))
            case src.SClass(name, fields):
                # this case happens, when we are on the top level.
                # thus, create constructor with the name of the form: 
                # def name(f1, ..., fn):
                #     return (f1, ..., fn)
                ids = IList([x for x, _ in fields])
                out += ilist(
                    tgt.DFun(name, ids, ilist(tgt.SReturn(tgt.ETuple(IList([tgt.EVar(x) for x in ids])))))
                )
            case s:
                stmts += ilist(s)
    main = tgt.DFun(Id("main"), ilist(), shrink_stmts(stmts))
    out += ilist(main)
    return out

def shrink_decl(d: src.Decl) -> tgt.Decl:
    match d:
        case src.DFun(name, params, _, body):
            params_out = IList([x for (x, _) in params])
            return tgt.DFun(name, params_out, shrink_stmts(body))

def shrink_stmts(ss: IList[src.Stmt]) -> IList[tgt.Stmt]:
    return IList([shrink_stmt(s) for s in ss])

def shrink_stmt(s: src.Stmt) -> tgt.Stmt:
    match s:
        case src.SExpr(e):
            e_out = shrink_expr(e)
            return tgt.SExpr(e_out)
        case src.SPrint(e):
            e_out = shrink_expr(e)
            return tgt.SPrint(e_out)
        case src.SAssign(x, _, e):
            e_out = shrink_expr(e)
            return tgt.SAssign(x, e_out)
        case src.SIf(e, b1, b2):
            e_out = shrink_expr(e)
            b1_out = shrink_stmts(b1)
            b2_out = shrink_stmts(b2)
            return tgt.SIf(e_out, b1_out, b2_out)
        case src.SWhile(e, b):
            e_out = shrink_expr(e)
            b_out = shrink_stmts(b)
            return tgt.SWhile(e_out, b_out)
        case src.SReturn(e):
            e_out = shrink_expr(e)
            return tgt.SReturn(e_out)
        case src.SClass(name, fields):
            # this case happens, when we are in a function already.
            # thus, create constructor of the form: 
            # name = lambda f1. ... lambda fn. (f1, ..., fn)
            ids = IList([x for x, _ in fields])
            return tgt.SAssign(name, tgt.ELambda(ids, tgt.ETuple(IList([tgt.EVar(x) for x in ids]))))

def shrink_expr(e: src.Expr) -> tgt.Expr:
    match e:
        case src.EConst(c):
            return tgt.EConst(c, '63bit')
        case src.EVar(x):
            return tgt.EVar(x)
        case src.EInput():
            return tgt.EInput()
        case src.EOp1(op, e1):
            e1_out = shrink_expr(e1)
            return tgt.EOp1(op, e1_out)
        case src.EOp2(e1, op, e2):
            e1_out = shrink_expr(e1)
            e2_out = shrink_expr(e2)
            match op:
                case "and":
                    return tgt.EIf(e1_out, e2_out, tgt.EConst(False, '63bit'))
                case "or":
                    return tgt.EIf(e1_out, tgt.EConst(True, '63bit'), e2_out)
                case "is":
                    # As tuples are represented as pointers, the 'is' operator
                    # corresponds simply to equality.
                    return tgt.EOp2(e1_out, "==", e2_out)
                case _:
                    return tgt.EOp2(e1_out, op, e2_out)
        case src.EIf(e1, e2, e3):
            e1_out = shrink_expr(e1)
            e2_out = shrink_expr(e2)
            e3_out = shrink_expr(e3)
            return tgt.EIf(e1_out, e2_out, e3_out)
        case src.ETuple(es):
            return tgt.ETuple(IList([shrink_expr(e) for e in es]))
        case src.ETupleAccess(e, i):
            return tgt.ETupleAccess(shrink_expr(e), i)
        case src.ETupleLen(e):
            return tgt.ETupleLen(shrink_expr(e))
        case src.ECall(e_fun, e_args):
            e_fun_out = shrink_expr(e_fun)
            e_args_out = IList([shrink_expr(arg) for arg in e_args])
            return tgt.ECall(e_fun_out, e_args_out)
        case src.ELambda(params, body):
            return tgt.ELambda(params, shrink_expr(body))
        case src.EField(e, _, idx):
            assert idx is not None, "`idx` is set during type checking."
            return tgt.ETupleAccess(shrink_expr(e), idx)
