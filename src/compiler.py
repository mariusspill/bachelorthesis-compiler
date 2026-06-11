from argparse import ArgumentParser
from sys import exit
from typing import Any, Optional

import ast_1_python
import ast_2_shrunk
import ast_3_revealed
import ast_4_conv_ass
import ast_5_closures
import ast_6_alloc
import ast_7_mon
import ast_8_exp
import ast_9_sel
import ast_10_mem
import ast_11_patched
import ast_12_riscv
from pass_0_1_parser import parse, ParseError
from pass_1_2_shrink import shrink
from pass_2_2_uniquify import uniquify
from pass_2_3_reveal_functions import reveal
from pass_3_4_convert_assignments import conv_ass
from pass_4_5_closure_conversion import closure_conv
from pass_5_5_limit_functions import limit
from pass_5_6_alloc import alloc
from pass_6_7_monadic import monadic
from pass_7_8_explicate import explicate
from pass_8_9_select import select
from pass_9_10_assign_homes import assign_homes
from pass_10_10_optimize import optimize
from pass_10_11_patch_instructions import patch_instructions
from pass_11_12_add_prelude import add_prelude_and_conclusion
from type_checker import type_check, TypeError
from register_allocation import allocate_registers

# Read commandline arguments

arg_parser = ArgumentParser(
    prog="pycomp",
    description="Compiles a subset of Python to RISC-V assembly.",
)
arg_parser.add_argument(
    "-i", "--src", metavar="PATH", required=True, help="source file to compile"
)
arg_parser.add_argument(
    "-o",
    "--tgt",
    metavar="PATH",
    help="target file to save the assembly to (default: print to stdout)",
)
arg_parser.add_argument(
    "-v", "--verbose", action="store_true", help="debug print the output of all passes"
)
arg_parser.add_argument(
    "-V",
    "--very-verbose",
    action="store_true",
    help="debug print also the early parsing chart",
)
args = arg_parser.parse_args()

src_path: str = args.src
tgt_path: Optional[str] = args.tgt
verbose: bool = args.verbose
very_verbose: bool = args.very_verbose

if very_verbose:
    verbose = True

# Compilation

if verbose:
    print("\n===== READING SOURCE FILE =====\n")
try:
    with open(src_path, "r") as f:
        src_str = f.read()
except OSError as err:
    print(f"Failed reading from source file {src_path}: {err}")
    exit(1)
if verbose:
    print(src_str)

if verbose:
    print("\n===== PARSING =====\n")
try:
    ast: Any = parse(src_str)
except ParseError as err:
    print(err)
    exit(1)
if verbose:
    print(f"{ast}\n\n{ast_1_python.pretty(ast)}")

if verbose:
    print("\n===== TYPE CHECKING =====\n")
try:
    type_check(ast)
except TypeError as err:
    print(err)
    exit(1)
if verbose:
    print("Program is well-typed.")

if verbose:
    print("\n===== SHRINKING =====\n")
ast = shrink(ast)
if verbose:
    print(ast_2_shrunk.pretty(ast))

if verbose:
    print("\n===== UNIQUIFY =====\n")
ast = uniquify(ast)
if verbose:
    print(ast_2_shrunk.pretty(ast))

if verbose:
    print("\n===== REVEAL FUNCTIONS =====\n")
ast = reveal(ast)
if verbose:
    print(ast_3_revealed.pretty(ast))

if verbose:
    print("\n===== CONVERT ASSIGNMENTS =====\n")
ast = conv_ass(ast)
if verbose:
    print(ast_4_conv_ass.pretty(ast))

if verbose:
    print("\n===== CLOSURE CONVERSION =====\n")
ast = closure_conv(ast)
if verbose:
    print(ast_5_closures.pretty(ast))

if verbose:
    print("\n===== LIMIT FUNCTIONS =====\n")
ast = limit(ast)
if verbose:
    print(ast_5_closures.pretty(ast))

if verbose:
    print("\n===== HEAP ALLOCATION =====\n")
ast = alloc(ast)
if verbose:
    print(ast_6_alloc.pretty(ast))

if verbose:
    print("\n===== MONADIC NORMALFORM =====\n")
ast = monadic(ast)
if verbose:
    print(ast_7_mon.pretty(ast))

if verbose:
    print("\n===== EXPLICATE CONTROL =====\n")
blocks = explicate(ast)
if verbose:
    print(ast_8_exp.pretty(blocks))

if verbose:
    print("\n===== INSTRUCTION SELECTION =====\n")
blocks = select(blocks)
if verbose:
    print(ast_9_sel.pretty(blocks))

if verbose:
    print("\n===== REGISTER ALLOCATION =====\n")
reg_allocs = allocate_registers(blocks)
if verbose:
    for l, reg_alloc in reg_allocs.items():
        print(f"{l}:")
        for key, val in reg_alloc.env.items():
            print(f"\t{key}: {val}")

if verbose:
    print("\n===== ASSIGN HOMES =====\n")
ast = assign_homes(blocks, reg_allocs)
if verbose:
    print(ast_10_mem.pretty(ast))

if verbose:
    print("\n===== OPTIMIZE =====\n")
ast = optimize(ast)
if verbose:
    print(ast_10_mem.pretty(ast))

if verbose:
    print("\n===== PATCH INSTRUCTIONS =====\n")
ast = patch_instructions(ast)
if verbose:
    print(ast_11_patched.pretty(ast))

if verbose:
    print("\n===== ADD PRELUDE & CONCLUSION =====\n")
ast = add_prelude_and_conclusion(ast, reg_allocs)
if verbose:
    print(ast_12_riscv.pretty(ast))

tgt_str = ast_12_riscv.pretty(ast)

if verbose:
    print("\n===== WRITING OUTPUT ASSEMBLY =====\n")
if tgt_path is None:
    print(tgt_str)
else:
    try:
        with open(tgt_path, "w+") as f:
            f.write(tgt_str)
    except OSError as err:
        print(f"Failed writing to target file {tgt_path}: {err}")
        exit(1)
    if verbose:
        print(f"Wrote output assembly to file {tgt_path}.")
