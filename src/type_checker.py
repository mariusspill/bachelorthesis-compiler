from dataclasses import dataclass

from ast_1_python import *
from util.immutable_list import IList

from identifier import Id

# Error Type

@dataclass
class TypeError(Exception):
    msg: str

# Typing context

type TCtx = dict[Id, Type]

# Type Checking

def type_check(p: Program) -> None:
    match p:
        case Program(body):
            ctx: TCtx = dict()
            for d in body: 
                match d:
                    case DFun():
                        type_declare_def(ctx, d)
            for s in body:
                match s:
                    case SClass():
                        type_declare_class(ctx, s)
                    case DFun():
                        type_check_def(ctx, s)
                    case _:
                        type_check_stmt(ctx, s)

def type_declare_def(ctx: TCtx, d: Decl) -> None:
    match d:
        case DFun(funcvar, parameters, result_type, _):
            ftype = TCallable(IList([ty for (_, ty) in parameters]), result_type)
            if funcvar in ctx:
                raise TypeError(f"Function {funcvar} defined twice")
            ctx[funcvar] = ftype

def type_declare_class(ctx: TCtx, c: SClass) -> None:
    match c:
        case SClass(name, fields):
            if name in ctx:
                raise TypeError(f"Dataclass {name} defined twice")
            ctx[name] = TCallable(IList([t for _, t in fields]), TClass(name))
            ctx[Id(f"{name}@type")] = TClass(name, fields)

def type_check_def(ctx: TCtx, d: Decl) -> None:
    match d:
        case DFun(funcvar, parameters, result_type, body):
            type_well_formed(ctx, result_type)
            types_well_formed(ctx, IList([t for _, t in parameters]))

            local_ctx = ctx.copy()
            local_ctx.update(parameters)
            local_ctx[Id('@ret')] = result_type
            if not type_check_stmts(local_ctx, body):
                raise TypeError(f"Function {funcvar} does not return {result_type} on all paths")

def type_check_stmts(ctx: TCtx, ss: IList[Stmt]) -> bool:
    for s in ss:
        if type_check_stmt(ctx, s):
            return True
    return False

def type_check_stmt(ctx: TCtx, s: Stmt) -> bool:
    match s:
        case SExpr(e):
            _ = type_check_expr(ctx, e)
            return False
        case SPrint(e):
            te = type_check_expr(ctx, e)
            check_type_equal(te, TInt(), e)
            return False
        case SAssign(x, t, e):
            if t is None:
                te = type_check_expr(ctx, e)
                if x in ctx:
                    check_type_equal(te, ctx[x], s)
                else:
                    ctx[x] = te
                return False
            else:
                type_well_formed(ctx, t)
                if x in ctx:
                    check_type_equal(t, ctx[x], s)
                else:
                    ctx[x] = t
                check_expr(ctx, e, t)
                return False
        case SIf(test, body, orelse):
            ttest = type_check_expr(ctx, test)
            check_type_equal(ttest, TBool(), test)
            ctx_orelse = ctx.copy()
            rt_body = type_check_stmts(ctx, body)
            rt_else = type_check_stmts(ctx_orelse, orelse)
            check_ctx_equal(ctx, ctx_orelse, s)
            return rt_body and rt_else
        case SWhile(test, body):
            ttest = type_check_expr(ctx, test)
            check_type_equal(ttest, TBool(), test)
            type_check_stmts(ctx, body)
            return False
        case SReturn(e):
            if Id('@ret') not in ctx:
                raise TypeError(f"Unexpected return statement {s} on top-level of the program.")
            check_expr(ctx, e, ctx[Id('@ret')])
            return True
        case SClass():
            # locally defined class are handled the same way as toplevel classes
            # no shadowing allowed (aligning with mypy and pylance)
            type_declare_class(ctx, s)
            return False

# infer type of an expression        
def type_check_expr(ctx: TCtx, e: Expr) -> Type:
    match e:
        case EConst(x):
            match x:
                case None:
                    return TNone()
                case bool(_):
                    return TBool()
                case int(_):
                    if x >= 2 ** 62 or x < -(2 ** 62):
                        raise TypeError(f"Integer constant {x} is too large for 63bit.")
                    else:
                        return TInt()
        case EVar(x):
            if x in ctx:
                return ctx[x]
            else:
                raise TypeError(f"Undefined variable {x}.")
        case EOp1(op, e):
            te = type_check_expr(ctx, e)
            match op:
                case "-":
                    check_type_equal(te, TInt(), e)
                    return TInt()
                case "not":
                    check_type_equal(te, TBool(), e)
                    return TBool()
        case EOp2(e1, op, e2):
            t1 = type_check_expr(ctx, e1)
            t2 = type_check_expr(ctx, e2)
            if type(t1) is TTuple or type(t2) is TTuple:
                match op:
                    case "is":
                        check_type_equal(t1, t2, e)
                        return TBool()
                    case _:
                        raise TypeError(f"Operator '{op}' is not supported for tuples.")
            match op:
                case "+" | "-":
                    check_type_equal(t1, TInt(), e1)
                    check_type_equal(t2, TInt(), e2)
                    return TInt()
                case "==" | "!=":
                    check_type_equal(t1, t2, e)
                    return TBool()
                case "<=" | "<" | ">" | ">=":
                    check_type_equal(t1, TInt(), e1)
                    check_type_equal(t2, TInt(), e2)
                    return TBool()
                case "and" | "or":
                    check_type_equal(t1, TBool(), e1)
                    check_type_equal(t2, TBool(), e2)
                    return TBool()
                case "is":
                    raise TypeError("Operator 'is' used on expression of non-tuple type.")
        case EInput():
            return TInt()
        case EIf(test, body, orelse):
            ttest = type_check_expr(ctx, test)
            tbody = type_check_expr(ctx, body)
            torelse = type_check_expr(ctx, orelse)
            check_type_equal(ttest, TBool(), test)
            check_type_equal(tbody, torelse, e)
            return tbody
        case ETuple(es):
            return TTuple(IList([type_check_expr(ctx, e) for e in es]))
        case ETupleAccess(e, i):
            t = type_check_expr(ctx, e)
            match t:
                case TTuple(ts):
                    if 0 <= i < len(ts):
                        return ts[i]
                    else:
                        raise TypeError(f"Index {i} is out of bounds for tuple of length {len(ts)}.")
                case t:
                    raise TypeError(f"Tuple access on non-tuple type {t}.")
        case ETupleLen(e):
            t = type_check_expr(ctx, e)
            match t:
                case TTuple(ts):
                    return TInt()
                case t:
                    raise TypeError(f"Tuple length used on non-tuple type {t}.")
        case ECall(f, es):
            fty = type_check_expr(ctx, f)
            match fty:
                case TCallable(arg_tys, res_ty):
                    if len(es) != len(arg_tys):
                        raise TypeError(f"Calling function with wrong number of arguments {e}.")
                    for (e, ty) in zip(es, arg_tys):
                        check_expr(ctx, e, ty)
                    return res_ty
                case t:
                    raise TypeError(f"Calling non-function type {t}.")
        case ELambda():
            raise TypeError(f"Cannot synthesize type of {pretty_expr(e)}")
        case EField(f, field):
            ety = type_check_expr(ctx, f)
            match ety:
                case TClass(name): 
                    ty = ctx[Id(f"{name}@type")]
                    match ty:
                        case TClass(name, fields):
                            assert fields is not None, "fields is always set for @type variable in context"
                            e.idx = [x for x, _ in fields].index(field)
                            for fld, ty in fields:
                                if fld == field:
                                    return ty
                            raise TypeError(f"Dataclass {name} does not have a field named {field}.")
                        case _:
                            # impossible?
                            raise TypeError(f"Dataclass {name} was not (yet) defined.")
                case _:
                    raise TypeError(f"Field access not allwed on non-dataclass {ety}.")

# check expression against given type
def check_expr(ctx: TCtx, e: Expr, ty: Type) -> None:
    match e:
        case ELambda(xs, body):
            match ty:
                case TCallable(arg_tys, ret_ty):
                    if len(xs) != len(arg_tys):
                        raise TypeError(f"Wrong number of arguments: {pretty_expr(e)} - {pretty_type(ty)}.")
                    new_ctx = ctx.copy()
                    new_ctx.update(zip(xs, arg_tys))
                    check_expr(new_ctx, body, ret_ty)
                case _:
                    raise TypeError(f"Lambda cannot have type {pretty_type(ty)}.")
        case _:
            te = type_check_expr(ctx, e)
            check_type_equal(te, ty, e)

# Type Equality

def check_type_equal(thave: Type, texpect: Type, es: Expr | Stmt) -> None:
    if thave != texpect:
        raise TypeError(f"I got {repr(thave)} but I expected {repr(texpect)} in {repr(es)}.")

def check_ctx_equal(ctx1: TCtx, ctx2: TCtx, es: Expr | Stmt) -> None:
    for x in ctx1:
        if x in ctx2:
            check_type_equal(ctx1[x], ctx2[x], es)
        else:
            del ctx1[x]

# Type Well Formed

def types_well_formed(ctx: TCtx, ts: IList[Type]) -> None:
    for t in ts:
        type_well_formed(ctx, t)

def type_well_formed(ctx: TCtx, t: Type) -> None:
    match t:
        case TBool() | TInt() | TNone():
            pass
        case TTuple(ts):
            types_well_formed(ctx, ts)
        case TCallable(params, ret_ty):
            types_well_formed(ctx, params)
            type_well_formed(ctx, ret_ty)
        case TClass(name):
            if Id(f"{name}@type") not in ctx:
                raise TypeError(f"Dataclass {name} was not (yet) defined.")