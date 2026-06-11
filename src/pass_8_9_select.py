from typing import Literal

import ast_8_exp as src
import ast_9_sel as tgt
from identifier import Id
from label import Label
from register import *
from util.immutable_list import ilist, IList

def select(p: src.Program) -> tgt.Program:
    return IList([select_decl(d) for d in p])

def select_decl(d: src.Decl) -> tgt.Function:
    match d:
        case src.DFun(label, params, start_label, end_label, body):
            out: tgt.Blocks = {}
            for label_, block in body.items():
                out[label_] = select_block(end_label, block)
            param_moves = IList([
                tgt.Move(x, reg)
                for x, reg in zip(params, FUNCTION_ARG_REGISTERS)
            ])
            out[start_label] = param_moves + out[start_label]
            return tgt.Function(label, start_label, end_label, out)

def select_block(end_label: Label, p: src.Block) -> tgt.Block:
    out: tgt.Block = ilist()
    for s in p:
        out += select_stmt(end_label, s)
    return out

def select_stmt(end_label: Label, s: src.Stmt) -> IList[tgt.Instr]:
    match s:
        case src.SPrint(e):
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
        case src.SAssign(lhs, src.EOp2Arith(e1, op, e2)):
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
        case src.EConst(c, size):
            c = 0 if c is None else int(c)
            return tgt.Const(c, size)
        case src.EVar(x):
            return x