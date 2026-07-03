from typing import Literal

import ast_8_exp as src
import ast_9_sel as tgt
from identifier import Id
from label import Label
from register import *
from util.immutable_list import ilist, IList
from types_ import *


def select(p: src.Program, types: dict) -> tgt.Program:
    return IList([select_decl(d, types) for d in p])

def select_decl(d: src.Decl, types: dict) -> tgt.Function:
    match d:
        case src.DFun(label, params, start_label, end_label, body):
            # extract name of the function
            matching_key = next((k for k in types if k.name == label.label), None)
            # get entry with the functions scope
            local_types = types[matching_key] if matching_key is not None else {}
            out: tgt.Blocks = {}
            for label_, block in body.items():
                out[label_] = select_block(end_label, block, local_types)
            param_moves = IList([
                tgt.Move(x, reg)
                for x, reg in zip(params, FUNCTION_ARG_REGISTERS)
            ])
            out[start_label] = param_moves + out[start_label]
            return tgt.Function(label, start_label, end_label, out)

def select_block(end_label: Label, p: src.Block, types: dict) -> tgt.Block:
    out: tgt.Block = ilist()
    for s in p:
        out += select_stmt(end_label, s, types)
    return out

def select_stmt(end_label: Label, s: src.Stmt, types: dict) -> IList[tgt.Instr]:
    match s:
        case src.SPrint(e):
            atom = select_atom(e)
            if types[atom] == TFloat():
                tmp = Id.fresh("tmp")
                return ilist(                
                tgt.Move(tmp, tgt.Offset(select_atom(e), 7)),
                tgt.Move(fa0, tmp),
                tgt.Call(Label("print_float"), 1, 'normal'),)
            else:
                return ilist(
                    tgt.Move(a0, select_atom(e)),
                    # Divide the argument by 2 to remove the tag bit.
                    # Note that right-shifting would cause issues with negative numbers!
                    tgt.Instr2('div', a0, a0, tgt.Const(2, '64bit')),
                    tgt.Call(Label("print_int64"), 1, 'normal'),
                )
        case src.SAssign(lhs, src.EConst(_, _) as e):
            lhs_out = select_lhs(lhs)
            return ilist(
                tgt.Move(lhs_out, select_atom(e))
            )
        case src.SAssign(lhs, src.EConstFloat(_) as e):
            lhs_out = select_lhs(lhs)
            return ilist(
                tgt.Move(lhs_out, select_atom(e))
            )
        case src.SAssign(lhs, src.EVar(y)):
            lhs_out = select_lhs(lhs)
            return ilist(
                tgt.Move(lhs_out, y)
            )
        case src.SAssign(lhs, src.EInput()):
            lhs_out = select_lhs(lhs)
            return ilist(
                tgt.Call(Label("input_int64"), 0, 'normal'),
                # Multiply the argument by 2 to add the tag bit.
                # Note that left-shifting would cause issues with negative numbers!
                tgt.Instr2('mul', a0, a0, tgt.Const(2, '64bit')),
                tgt.Move(lhs_out, a0),
            )
        case src.SAssign(lhs, src.EOp1(op, e)):
            match op:
                case "not":
                    return ilist(
                        tgt.Instr2("sub", select_lhs(lhs), tgt.Const(2, "64bit"), select_atom(e))
                    )
                case "-":
                    return ilist(
                        tgt.Instr2("sub", select_lhs(lhs), tgt.Const(0, "64bit"), select_atom(e))
                    )
                case "int_to_float":
                    lhs_out = select_lhs(lhs)
                    tmp = Id.fresh("tmp")
                    return ilist(
                        tgt.Move(tmp, select_atom(e)),
                        tgt.Instr2("srl", tmp, tmp, tgt.Const(1, '64bit')),
                        tgt.Instr2("fcvt.d.l", fa0, fa0, tmp),
                        tgt.Move(lhs_out, fa0),
                    )
        case src.SAssign(lhs, src.EOp2Arith(e1, op, e2)):
            lh = select_lhs(lhs)
            e1a = select_atom(e1)
            e2a = select_atom(e2)
            if types.get(e1a) == TFloat() and types.get(e2a) == TFloat():
                tmp1 = Id.fresh("tmp")
                tmp2 = Id.fresh("tmp")

                result = ilist(
                    tgt.Move(tmp1, e1a),
                    tgt.Move(fa0, tmp1), 
                    tgt.Move(tmp2, e2a),
                    tgt.Move(fa1, tmp2)
                )
                match op: 
                    case '+':
                        result += ilist(tgt.Instr2("fadd.d", fa0, fa0, fa1))
                    case '-':
                        result += ilist(tgt.Instr2("fsub.d", fa0, fa0, fa1))
                    case '*':
                        result += ilist(tgt.Instr2("fmul.d", fa0, fa0, fa1))
                    case '/':
                        result += ilist(tgt.Instr2("fdiv.d", fa0, fa0, fa1))
                result += ilist(tgt.Move(lh, fa0))
                return result
            else:
                match op:
                    case "+":
                        return ilist(
                            tgt.Instr2("add", select_lhs(lhs), select_atom(e1), select_atom(e2))
                        )
                    case "-":
                        return ilist(
                            tgt.Instr2("sub", select_lhs(lhs), select_atom(e1), select_atom(e2))
                        )
        case src.SAssign(lhs, src.EOp2Comp(e1, op, e2)):
            lhs_out = select_lhs(lhs)
            e1a = select_atom(e1)
            e2a = select_atom(e2)
            if types.get(e1a) == TFloat() and types.get(e2a) == TFloat():
                tmp1 = Id.fresh("tmp")
                tmp2 = Id.fresh("tmp")
                result = ilist(
                    tgt.Move(tmp1, select_atom(e1)),
                    tgt.Move(fa0, tmp1), 
                    tgt.Move(tmp2, select_atom(e2)),
                    tgt.Move(fa1, tmp2)
                )
                match op:
                    case "==":
                        result += ilist(tgt.Instr2("feq.d", lhs_out, fa0, fa1))
                    case "!=":
                        result += ilist(tgt.Instr2("feq.d", lhs_out, fa0, fa1),
                                        tgt.Instr2("xor", lhs_out, lhs_out, tgt.Const(1, '64bit')))
                    case "<":
                        result += ilist(tgt.Instr2("flt.d", lhs_out, fa0, fa1))
                    case ">":
                        result += ilist(tgt.Instr2("flt.d", lhs_out, fa1, fa0))
                    case "<=":
                        result += ilist(tgt.Instr2("fle.d", lhs_out, fa0, fa1))
                    case ">=":
                        result += ilist(tgt.Instr2("fle.d", lhs_out, fa1, fa0))
                return result + ilist(tgt.Instr2("sll", lhs_out, lhs_out, tgt.Const(1, '64bit')))
            else:
                match op:
                    case "==":
                        return ilist(
                            tgt.Instr2("sub", lhs_out, select_atom(e1), select_atom(e2)),
                            tgt.Instr2("sltu", lhs_out, lhs_out, tgt.Const(1, '64bit')),
                            # Left shift because of tagging
                            tgt.Instr2("sll", lhs_out, lhs_out, tgt.Const(1, '64bit')),
                        )
                    case "!=":
                        return ilist(
                            tgt.Instr2("sub", lhs_out, select_atom(e1), select_atom(e2)),
                            tgt.Instr2("sltu", lhs_out, zero, lhs_out),
                            # Left shift because of tagging
                            tgt.Instr2("sll", lhs_out, lhs_out, tgt.Const(1, '64bit')),
                        )
                    case "<":
                        return ilist(
                            tgt.Instr2("slt", lhs_out, select_atom(e1), select_atom(e2)),
                            # Left shift because of tagging
                            tgt.Instr2("sll", lhs_out, lhs_out, tgt.Const(1, '64bit')),
                        )
                    case ">":
                        return ilist(
                            tgt.Instr2("slt", lhs_out, select_atom(e2), select_atom(e1)),
                            # Left shift because of tagging
                            tgt.Instr2("sll", lhs_out, lhs_out, tgt.Const(1, '64bit')),
                        )
                    case "<=":
                        return ilist(
                            tgt.Instr2("slt", lhs_out, select_atom(e2), select_atom(e1)),
                            tgt.Instr2("xor", lhs_out, lhs_out, tgt.Const(1, '64bit')),
                            # Left shift because of tagging
                            tgt.Instr2("sll", lhs_out, lhs_out, tgt.Const(1, '64bit')),
                        )
                    case ">=":
                        return ilist(
                            tgt.Instr2("slt", lhs_out, select_atom(e1), select_atom(e2)),
                            tgt.Instr2("xor", lhs_out, lhs_out, tgt.Const(1, '64bit')),
                            # Left shift because of tagging
                            tgt.Instr2("sll", lhs_out, lhs_out, tgt.Const(1, '64bit')),
                        )
        case src.SAssign(lhs, src.EAllocate(num_elems)):
            lhs_out = select_lhs(lhs)
            tmp = Id.fresh("tmp")
            free_ptr = tgt.Offset(Label("gc_free_ptr"), 0)
            return ilist(
                # Move the free_ptr into a new temporary.
                tgt.Instr2('add', tmp, free_ptr, tgt.Const(1, '64bit')),
                # Increment the free_ptr by the amount of memory we want to allocate,
                # such that subsequent allocation don't use the same memory region again.
                tgt.Instr2('add', free_ptr, free_ptr, tgt.Const(8*(num_elems + 1), '64bit')),
                # Now the old free_ptr in tmp is the begin of our allocated memory region.
                # Initialize the meta data in the first byte of the allocated memory
                # with a 0 tag (not yet copied) and the length auf the tuple in the other 63bit.
                tgt.Move(tgt.Offset(tmp, -1), tgt.Const(num_elems, '63bit')),
                # Use the tagged old free_ptr as the result.
                tgt.Move(lhs_out, tmp),
            )
        case src.SAssign(lhs, src.ETupleLen(e)):
            lhs_out = select_lhs(lhs)
            match select_atom(e):
                case tgt.Const(_, _):
                    raise Exception("Cannot take tuple length of an integer")
                case tgt.Id(_) as x:
                    return ilist(
                        # Get the meta data. We subtract 1 because of the heap pointer tag.
                        # The tag is 0, so the meta data directly contains the length in 63bit form
                        # Move the result into the lhs
                        tgt.Move(lhs_out, tgt.Offset(x, -1))
                    )
        case src.SAssign(lhs, src.ETupleAccess(e, i)):
            lhs_out = select_lhs(lhs)
            match select_atom(e):
                case tgt.Const(_, _):
                    raise Exception("Subscripting on a constant is forbidden")
                case tgt.Id(_) as x:
                    return ilist(
                        tgt.Move(lhs_out, tgt.Offset(x, 8 * (i + 1) - 1))
                    )
        case src.SAssign(lhs, src.EGlobal(g)):
            lhs_out = select_lhs(lhs)
            return ilist(
                tgt.Move(lhs_out, tgt.Offset(Label(g), 0))
            )
        case src.SAssign(lhs, src.EFunRef(label)):
            lhs_out = select_lhs(lhs)
            return ilist(
                tgt.Move(lhs_out, label)
            )
        case src.SAssign(lhs, src.ECall(e_func, e_args)):
            lhs_out = select_lhs(lhs)
            b_args = IList([
                tgt.Move(reg, select_atom(arg))
                for reg, arg in zip(FUNCTION_ARG_REGISTERS, e_args)
            ])
            e_func_out = select_atom(e_func)
            match e_func_out:
                case tgt.Const(_, _):
                    raise Exception("Impossible: function call on constant")
            return b_args + ilist(
                tgt.Call(e_func_out, len(e_args), 'normal'),
                tgt.Move(lhs_out, a0),
            )
        case src.STailCall(e_func, e_args):
            e_args_out = IList([
                tgt.Move(reg, select_atom(arg))
                for reg, arg in zip(FUNCTION_ARG_REGISTERS, e_args)
            ])
            e_func_out = select_atom(e_func)
            match e_func_out:
                case tgt.Const(_, _):
                    raise Exception("Impossible: function call on constant")
            return e_args_out + ilist(
                tgt.Call(e_func_out, len(e_args), 'tail call')
            )
        case src.SReturn(e):
            return ilist(
                tgt.Move(a0, select_atom(e)),
                tgt.Jump(end_label),
            )
        case src.SCollect(num_words):
            return ilist(
                # Argument 1 is the current stack pointer
                tgt.Move(a0, sp),
                # Argument 2 is the number of words we wanted to
                # allocate, but ran out of heap memory.
                tgt.Move(a1, tgt.Const(num_words, '64bit')),
                # Call the collect function from the runtime.
                tgt.Call(Label("gc_collect"), 2, 'normal'),
            )
        case src.SIf(src.EOp2Comp(e1, op, e2), body_label, orelse_label):
            e1a = select_atom(e1)
            e2a = select_atom(e2)
            if types.get(e1a) == TFloat() and types.get(e2a) == TFloat():
                tmp1 = Id.fresh("tmp")
                tmp2 = Id.fresh("tmp")
                result = ilist(
                    tgt.Move(tmp1, e1a),
                    tgt.Move(fa0, tmp1), 
                    tgt.Move(tmp2, e2a),
                    tgt.Move(fa1, tmp2)
                )
                match op:
                    case "==":
                        result += ilist(tgt.Instr2("feq.d", t0, fa0, fa1))
                    case "!=":
                        result += ilist(tgt.Instr2("feq.d", t0, fa0, fa1),
                                        tgt.Instr2("xor", t0, t0, tgt.Const(1, '64bit')))
                    case "<":
                        result += ilist(tgt.Instr2("flt.d", t0, fa0, fa1))
                    case "<=":
                        result += ilist(tgt.Instr2("fle.d", t0, fa0, fa1))
                    case ">":
                        result += ilist(tgt.Instr2("flt.d", t0, fa1, fa0))
                    case ">=":
                        result += ilist(tgt.Instr2("fle.d", t0, fa1, fa0))
                return result + ilist(
                    tgt.Branch("bne", t0, zero, body_label),
                    tgt.Jump(orelse_label),
                )
            else:
                match op:
                    case "==":
                        cc: Literal["beq", "bne", "blt", "bge"] = "beq"
                    case "!=":
                        cc = "bne"
                    case "<":
                        cc = "blt"
                    case "<=":
                        cc = "bge"
                        e2, e1 = e1, e2
                    case ">":
                        cc = "blt"
                        e2, e1 = e1, e2
                    case ">=":
                        cc = "bge"
                return ilist(
                    tgt.Branch(cc, select_atom(e1), select_atom(e2), body_label),
                    tgt.Jump(orelse_label),
                )
        case src.SGoto(target):
            return ilist(tgt.Jump(target))
    raise Exception("Impossible!")

def select_lhs(lhs: src.Lhs) -> Id | tgt.Offset:
    match lhs:
        case src.LId(x):
            return x
        case src.LSubscript(e, i):
            match select_atom(e):
                case tgt.Const(_, _):
                    raise Exception("Subscripting on a constant is forbidden")
                case tgt.Id(_) as x:
                    # We subtract 1 because of the heap pointer tag
                    return tgt.Offset(x, 8*(i + 1) - 1)
    raise Exception("Impossible!")

def select_atom(e: src.ExprAtom) -> tgt.Const | Id:
    match e:
        case src.EConstFloat(c):
            return tgt.ConstFloat(c)
        case src.EConst(c, size):
            c = 0 if c is None else int(c)
            return tgt.Const(c, size)
        case src.EVar(x):
            return x