import ast_7_mon as src
import ast_8_exp as tgt
from identifier import Id
from util.immutable_list import IList, ilist
from label import Label

def explicate(p: src.Program) -> tgt.Program:
    return IList([explicate_decl(d) for d in p])

def explicate_decl(d: src.Decl) -> tgt.Decl:
    match d:
        case src.DFun(name_label, params, body):
            name = name_label.label

            l_fun = Label(name)
            l_start = Label(name + "_start")
            l_end = Label(name + "_conclusion")

            out: tgt.Blocks = {}
            out[l_fun] = ilist(tgt.SGoto(l_start))
            out[l_start] = ilist()

            l = explicate_stmts(out, l_start, body)

            out[l] += ilist(tgt.SGoto(l_end))
            out[l_end] = ilist()

            return tgt.DFun(Label(name), params, l_start, l_end, out)

def explicate_stmts(out: tgt.Blocks, l: Label, p: IList[src.Stmt]) -> Label:
    for s in p:
        l = explicate_stmt(out, l, s)
    return l

def explicate_stmt(out: tgt.Blocks, l: Label, s: src.Stmt) -> Label:
    match s:
        case src.SAssign(lhs, e):
            lhs_out = explicate_lhs(lhs)
            e_out = explicate_expr(e)
            out[l] += ilist(tgt.SAssign(lhs_out, e_out))
            return l
        case src.SPrint(e):
            out[l] += ilist(tgt.SPrint(explicate_atom(e)))
            return l
        case src.SCollect(n):
            out[l] += ilist(tgt.SCollect(n))
            return l
        case src.SIf(src.EOp2Comp(a1, op, a2), b1, b2):
            body_label: Label = Label.fresh("body")
            orelse_label: Label = Label.fresh("orelse")
            cont_label: Label = Label.fresh("cont")

            test = tgt.EOp2Comp(explicate_atom(a1), op, explicate_atom(a2))
            out[l] += ilist(tgt.SIf(test, body_label, orelse_label))

            out[body_label] = ilist()
            out[orelse_label] = ilist()
            body_label_out = explicate_stmts(out, body_label, b1)
            orelse_label_out = explicate_stmts(out, orelse_label, b2)

            out[body_label_out] += ilist(tgt.SGoto(cont_label))
            out[orelse_label_out] += ilist(tgt.SGoto(cont_label))

            out[cont_label] = ilist()
            return cont_label
        case src.SWhile(test_prelude, src.EOp2Comp(a1, op, a2), b):
            test_label: Label = Label.fresh("test")
            body_label = Label.fresh("body")
            cont_label = Label.fresh("cont")

            # Finish current block with goto to `test_label`.
            out[l] += ilist(tgt.SGoto(test_label))

            # Create one (or more) blocks for the condition.
            out[test_label] = ilist()
            test_label_out = explicate_stmts(out, test_label, test_prelude)
            test = tgt.EOp2Comp(explicate_atom(a1), op, explicate_atom(a2))
            out[test_label_out] += ilist(tgt.SIf(test, body_label, cont_label))

            # Create a new block for the body, which should jump
            # to the `test_prelude_label` after running.
            out[body_label] = ilist()
            body_label_out = explicate_stmts(out, body_label, b)
            out[body_label_out] += ilist(tgt.SGoto(test_label))

            # Continue with a new block at `cont_label`
            out[cont_label] = ilist()
            return cont_label
        case src.SReturn(e):
            e_out = explicate_expr(e)
            match e_out:
                case tgt.ECall(e_func, e_args):
                    out[l] += ilist(tgt.STailCall(e_func, e_args))
                case _:
                    x = Id.fresh("x")
                    out[l] += ilist(
                        tgt.SAssign(tgt.LId(x), e_out),
                        tgt.SReturn(tgt.EVar(x)),
                    )
            return l

def explicate_lhs(lhs: src.Lhs) -> tgt.Lhs:
    match lhs:
        case src.LId(x):
            return tgt.LId(x)
        case src.LSubscript(e, i):
            return tgt.LSubscript(explicate_atom(e), i)

def explicate_expr(e: src.Expr) -> tgt.Expr:
    match e:
        case src.EVar(_) | src.EConst(_):
            return explicate_atom(e)
        case src.EInput():
            return tgt.EInput()
        case src.EOp1(op, a):
            e_out = explicate_atom(a)
            return tgt.EOp1(op, e_out)
        case src.EOp2Arith(a1, op, a2):
            a1_out = explicate_atom(a1)
            a2_out = explicate_atom(a2)
            return tgt.EOp2Arith(a1_out, op, a2_out)
        case src.EOp2Comp(a1, op, a2):
            a1_out = explicate_atom(a1)
            a2_out = explicate_atom(a2)
            return tgt.EOp2Comp(a1_out, op, a2_out)
        case src.EGlobal(x):
            return tgt.EGlobal(x)
        case src.EAllocate(n):
            return tgt.EAllocate(n)
        case src.ETupleLen(e1):
            e1_out = explicate_atom(e1)
            return tgt.ETupleLen(e1_out)
        case src.ETupleAccess(e1, i):
            e1_out = explicate_atom(e1)
            return tgt.ETupleAccess(e1_out, i)
        case src.ECall(e_func, e_args):
            e_func_out = explicate_atom(e_func)
            e_args_out = explicate_atoms(e_args)
            return tgt.ECall(e_func_out, e_args_out)
        case src.EFunRef(name):
            return tgt.EFunRef(name)

def explicate_atoms(es: IList[src.ExprAtom],) -> IList[tgt.ExprAtom]:
    return IList([explicate_atom(e) for e in es])

def explicate_atom(a: src.ExprAtom) -> tgt.ExprAtom:
    match a:
        case src.EVar(x):
            return tgt.EVar(x)
        case src.EConst(x, size):
            return tgt.EConst(x, size)