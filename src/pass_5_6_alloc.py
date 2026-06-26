import ast_5_closures as src
import ast_6_alloc as tgt
from identifier import Id
from util.immutable_list import *
from types_ import *

def alloc(p: src.Program, types: dict) -> tgt.Program:
    return IList([alloc_decl(d, types) for d in p])

def alloc_decl(d: src.Decl, types: dict) -> tgt.Decl:
    match d:
        case src.DFun(name, params, body):
            matching_key = next((k for k in types if k.name == name.label), None)
            local_types = types[matching_key] if matching_key is not None else {}
            return tgt.DFun(name, params, alloc_stmts(body, local_types))

def alloc_stmts(ss: IList[src.Stmt], types: dict) -> IList[tgt.Stmt]:
    return IList([alloc_stmt(s, types) for s in ss])

def alloc_stmt(s: src.Stmt, types: dict) -> tgt.Stmt:
    match s:
        case src.SExpr(e):
            e_out = alloc_expr(e, types)
            return tgt.SExpr(e_out)
        case src.SPrint(e):
            e_out = alloc_expr(e, types)
            return tgt.SPrint(e_out)
        case src.SAssign(x, e):
            lhs = alloc_lhs(x, types)
            e_out = alloc_expr(e, types)
            return tgt.SAssign(lhs, e_out)
        case src.SIf(e, b1, b2):
            e_out = alloc_expr(e, types)
            b1_out = alloc_stmts(b1, types)
            b2_out = alloc_stmts(b2, types)
            return tgt.SIf(e_out, b1_out, b2_out)
        case src.SWhile(e, b):
            e_out = alloc_expr(e, types)
            b_out = alloc_stmts(b, types)
            return tgt.SWhile(e_out, b_out)
        case src.SReturn(e):
            e_out = alloc_expr(e, types)
            return tgt.SReturn(e_out)

def alloc_lhs(lhs: src.Lhs, types: dict) -> tgt.Lhs:
    match lhs:
        case src.LId(x):
            return tgt.LId(x)
        case src.LSubscript(e, i):
            return tgt.LSubscript(alloc_expr(e, types), i)

def alloc_expr(e: src.Expr, types: dict) -> tgt.Expr:
    match e:
        case src.EConstFloat(c):
            body: IList[tgt.Stmt] = ilist()

            num_words = 2 # one for the header, one for the float
            num_bytes = num_words * 8

            # Start a garbage collection if we're out of memory.
            body += ilist(
                tgt.SIf(
                    tgt.EOp2(
                        tgt.EOp2(tgt.EGlobal('gc_free_ptr'), '+', tgt.EConst(num_bytes, '64bit')),
                        '<',
                        tgt.EGlobal('gc_fromspace_end')
                    ),
                    ilist(),
                    ilist(tgt.SCollect(num_words)),
                )
            )

            # Allocate space for the float
            v = Id.fresh("v")
            body += ilist(tgt.SAssign(tgt.LId(v), tgt.EAllocate(1))) # one because it needs eight bytes (64-bit) for a float or one word

            x = Id.fresh("flt")
            body += ilist(tgt.SAssign(tgt.LId(x), tgt.EConstFloat(c)))

            body += ilist(tgt.SAssign(tgt.LSubscript(tgt.EVar(v), 0), tgt.EVar(x)))


            return tgt.EBegin(body, tgt.EVar(v))
        case src.EConst(c, size):
            return tgt.EConst(c, size)
        case src.EVar(x):
            return tgt.EVar(x)
        case src.EInput():
            return tgt.EInput()
        case src.EOp1(op, e1):
            e1_out = alloc_expr(e1, types)

            isf1 = is_float(e1, types)

            if isf1:

                num_words = 2
                num_bytes = num_words * 8

                body: IList[tgt.Stmt] = ilist()

                t1 = Id.fresh("flt")
                body += ilist(tgt.SAssign(tgt.LId(t1), e1_out))
                unboxed1 = tgt.ETupleAccess(tgt.EVar(t1), 0)

                

                # Start a garbage collection if we're out of memory.
                body += ilist(
                    tgt.SIf(
                        tgt.EOp2(
                            tgt.EOp2(tgt.EGlobal('gc_free_ptr'), '+', tgt.EConst(num_bytes, '64bit')),
                            '<',
                            tgt.EGlobal('gc_fromspace_end')
                        ),
                        ilist(),
                        ilist(tgt.SCollect(num_words)),
                    )
                )

                # Allocate space for the tuple
                v = Id.fresh("v")
                body += ilist(tgt.SAssign(tgt.LId(v), tgt.EAllocate(1)))


                x = Id.fresh("flt")
                body += ilist(tgt.SAssign(tgt.LId(x), tgt.EOp1(op, unboxed1)))

                body += ilist(tgt.SAssign(tgt.LSubscript(tgt.EVar(v), 0), tgt.EVar(x)))

                return tgt.EBegin(body, tgt.EVar(v))
            else:
                return tgt.EOp1(op, e1_out) 
        case src.EOp2(e1, op, e2):
            e1_out = alloc_expr(e1, types)
            e2_out = alloc_expr(e2, types)

            body: IList[tgt.Stmt] = ilist()

            isf1 = is_float(e1, types)
            isf2 = is_float(e2, types)

            if isf1 or isf2:
                num_words = 2 # one for the header, one for the float
                num_bytes = num_words * 8

                if isf1:
                    t1 = Id.fresh("flt")
                    body += ilist(tgt.SAssign(tgt.LId(t1), e1_out))
                    unboxed1 = tgt.ETupleAccess(tgt.EVar(t1), 0)
                else:
                    unboxed1 = e1_out

                if isf2:
                    t2 = Id.fresh("flt")
                    body += ilist(tgt.SAssign(tgt.LId(t2), e2_out))
                    unboxed2 = tgt.ETupleAccess(tgt.EVar(t2), 0)
                else:
                    unboxed2 = e2_out

                if op == '+' or op == '-':
                    # Start a garbage collection if we're out of memory.
                    body += ilist(
                        tgt.SIf(
                            tgt.EOp2(
                                tgt.EOp2(tgt.EGlobal('gc_free_ptr'), '+', tgt.EConst(num_bytes, '64bit')),
                                '<',
                                tgt.EGlobal('gc_fromspace_end')
                            ),
                            ilist(),
                            ilist(tgt.SCollect(num_words)),
                        )
                    )

                    # Allocate space for the tuple
                    v = Id.fresh("v")
                    body += ilist(tgt.SAssign(tgt.LId(v), tgt.EAllocate(1)))


                    x = Id.fresh("flt")
                    body += ilist(tgt.SAssign(tgt.LId(x), tgt.EOp2(unboxed1, op, unboxed2)))

                    body += ilist(tgt.SAssign(tgt.LSubscript(tgt.EVar(v), 0), tgt.EVar(x)))

                    return tgt.EBegin(body, tgt.EVar(v))
                else:
                    # Return a boolean that doesnt have to be boxed
                    return tgt.EBegin(body, tgt.EOp2(unboxed1, op, unboxed2))
            else:
                return tgt.EOp2(e1_out, op, e2_out)

        case src.EIf(e1, e2, e3):
            e1_out = alloc_expr(e1, types)
            e2_out = alloc_expr(e2, types)
            e3_out = alloc_expr(e3, types)
            return tgt.EIf(e1_out, e2_out, e3_out)
        case src.ETuple(es):
            body: IList[tgt.Stmt] = ilist()

            # We need 8 bytes for the garbage collector tag and
            # 8 bytes for each element as all our values currently
            # take 8 bytes (boolean, int, tuple pointer).
            num_words = 1 + len(es)
            num_bytes = num_words * 8

            # Translate entry expressions and assign the results to
            # new temporary variables.
            xs = []
            for e in es:
                e_out = alloc_expr(e, types)
                x = Id.fresh("tup")
                body += ilist(tgt.SAssign(tgt.LId(x), e_out))
                xs += [x]

            # Start a garbage collection if we're out of memory.
            body += ilist(
                tgt.SIf(
                    tgt.EOp2(
                        tgt.EOp2(tgt.EGlobal('gc_free_ptr'), '+', tgt.EConst(num_bytes, '64bit')),
                        '<',
                        tgt.EGlobal('gc_fromspace_end')
                    ),
                    ilist(),
                    ilist(tgt.SCollect(num_words)),
                )
            )

            # Allocate space for the tuple
            v = Id.fresh("v")
            body += ilist(tgt.SAssign(tgt.LId(v), tgt.EAllocate(len(es))))

            # Copy the entry values into the tuple
            for i, x in enumerate(xs):
                body += ilist(tgt.SAssign(tgt.LSubscript(tgt.EVar(v), i), tgt.EVar(x)))

            return tgt.EBegin(body, tgt.EVar(v))
        case src.ETupleAccess(e, i):
            return tgt.ETupleAccess(alloc_expr(e, types), i)
        case src.ETupleLen(e):
            return tgt.ETupleLen(alloc_expr(e, types))
        case src.ECall(e_func, e_args):
            return tgt.ECall(alloc_expr(e_func, types), alloc_exprs(e_args, types))
        case src.EFunRef(name):
            return tgt.EFunRef(name)
        case src.EBegin(ss, e):
            return tgt.EBegin(alloc_stmts(ss, types), alloc_expr(e, types))

def alloc_exprs(es: IList[src.Expr], types: dict) -> IList[tgt.Expr]:
    return IList([alloc_expr(e, types) for e in es])


def is_float(e: src.Expr, types: dict) -> bool:
    match e:
        case src.EConstFloat(c):
            return True
        case src.ETupleAccess(src.EVar(v), i):
            return isinstance(types[v].ts[i], TFloat)
        case src.EOp2(a, ('+' | '-'), b):
            return is_float(a, types) or is_float(b, types)
        case src.EOp1('-', a):
            return is_float(a, types)
        case _:
            return False