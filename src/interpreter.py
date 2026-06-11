from argparse import ArgumentParser

from ast_1_python import *
from pass_0_1_parser import parse, ParseError
from type_checker import type_check, TypeError
from semantics import eval_prog

# Read commandline arguments

arg_parser = ArgumentParser(
    prog="pyinterp",
    description="Interpreter for a subset of Python.",
)
arg_parser.add_argument(
    "-i", "--src", metavar="PATH", required=True, help="source file to compile"
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

verbose: bool = args.verbose
very_verbose: bool = args.very_verbose

if very_verbose:
    verbose = True

# Interpretation

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
    ast = parse(src_str)
except ParseError as err:
    print(err)
    exit(1)
if verbose:
    print(f"{ast}\n\n{pretty(ast)}")

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
    print("\n===== EVALUATION =====\n")
eval_prog(ast)
