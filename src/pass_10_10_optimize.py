import ast_10_mem as src
import ast_10_mem as tgt
from util.immutable_list import IList, ilist

def optimize(p: src.Program) -> tgt.Program:
    return IList([optimize_fun(f) for f in p])

def optimize_fun(f: src.Function) -> tgt.Function:
    return tgt.Function(
        f.entry_label,
        f.start_label,
        f.end_label,
        optimize_blocks(f.body, f.entry_label)
    )

def optimize_blocks(blocks: src.Blocks, entry_label: src.Label) -> tgt.Blocks:
    blocks_out1 = {l: optimize_block(b) for (l, b) in blocks.items()}
    
    # Remove unreachable blocks
    blocks_out2: tgt.Blocks = {}
    explore: list[tgt.Label] = [entry_label]
    visited: set[tgt.Label] = {entry_label}
    while len(explore) > 0:
        label = explore.pop()
        block = blocks_out1[label]
        blocks_out2[label] = block
    
        match block:
            case [*_, tgt.Jump(target)]:
                if target not in visited:
                    visited.add(target)
                    explore.append(target)
        match block:
            case [*_, tgt.Branch(_, _, _, target), _]:
                if target not in visited:
                    visited.add(target)
                    explore.append(target)
        
    return blocks_out2

def optimize_block(block: src.Block) -> tgt.Block:
    block_out1: src.Block = ilist()
    i = 0
    while i < len(block):
        match block[i]:
            case src.Instr2(op, dst, src.Const(val1, size1), src.Const(val2, size2)):
                val1 = to_int_64(val1, size1)
                val2 = to_int_64(val2, size2)
                match op:
                    case "add":
                        val_out = val1 + val2
                    case "sub":
                        val_out = val1 - val2
                    case "mul":
                        val_out = val1 * val2
                    case "div":
                        val_out = val1 // val2
                    case "xor":
                        val_out = val1 != val2
                    case "sltu":
                        val_out = abs(val1 & 0xFFFFFFFFFFFFFFFF) < abs(val2 & 0xFFFFFFFFFFFFFFFF)
                    case "slt":
                        val_out = val1 < val2
                    case "and":
                        val_out = val1 and val2
                    case "sll":
                        val_out = val1 << val2
                    case "srl":
                        val_out = val1 >> val2
                val_out = simulate_over_and_underflow(int(val_out))
                block_out1 += ilist(src.Move(dst, src.Const(val_out, "64bit")))
            case src.Instr2(op, dst, src1, src.Const(val1, size1)):
                val1 = to_int_64(val1, size1)
                if op in ["add", "sub"] and val1 == 0:
                    block_out1 += ilist(src.Move(dst, src1))
                elif op in ["mul", "div"] and val1 == 1:
                    block_out1 += ilist(src.Move(dst, src1))
                elif op == "mul" and val1 == 0:
                    block_out1 += ilist(src.Move(dst, src.Const(0, "64bit")))
                else:
                    block_out1 += ilist(block[i])
            case src.Branch(cc, src.Const(val1, size1), src.Const(val2, size2), target):
                val1 = to_int_64(val1, size1)
                val2 = to_int_64(val2, size2)
                match cc:
                    case "beq":
                        if val1 == val2:
                            block_out1 += ilist(src.Jump(target))
                            break
                    case "bne":
                        if val1 != val2:
                            block_out1 += ilist(src.Jump(target))
                            break
                    case "blt":
                        if val1 < val2:
                            block_out1 += ilist(src.Jump(target))
                            break
                    case "bge":
                        if val1 >= val2:
                            block_out1 += ilist(src.Jump(target))
                            break
            case _:
                block_out1 += ilist(block[i])
        i += 1

    block_out2: src.Block = ilist()
    i = 0
    while i < len(block_out1):
        match block_out1[i]:
            case src.Move(dst1, src1):
                if dst1 != src1:
                    block_out2 += ilist(block_out1[i])
                    while i+1 < len(block_out1):
                        match block_out1[i+1]:
                            case src.Move(dst2, src2) if dst1 == src2 and src1 == dst2:
                                i = i + 1
                            case src.Move(dst2, src2) if dst2 == src2:
                                i = i + 1
                            case _:
                                break
            case _:
                block_out2 += ilist(block_out1[i])
        i += 1
    return block_out2

def to_int_64(value: int, size: str) -> int:
    return value << (1 if size == "63bit" else 0)

def simulate_over_and_underflow(i: int) -> int:
    while i > 2**63 - 1:
        i = i - (2**64)
    while i < -(2**63):
        i = i + (2**64)
    return i