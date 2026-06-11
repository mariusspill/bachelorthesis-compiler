import os
os.environ["PYTHONHASHSEED"] = "1"

from shutil import rmtree
from argparse import ArgumentParser
from subprocess import run, PIPE, STDOUT
from pathlib import Path
from textwrap import indent

TEST_DIR = Path(__file__).parent
BASE_DIR = TEST_DIR.parent
INTERPRETER_PATH = BASE_DIR / "src" / "interpreter.py"
COMPILER_PATH = BASE_DIR / "src" / "compiler.py"
RUNTIME_PATH = BASE_DIR / "runtime" / "runtime.c"

arg_parser = ArgumentParser(
    prog="test",
    description="Runs the interpreter and compiler on test files and compares the output.",
)
arg_parser.add_argument(
    "-i",
    "--src",
    metavar="PATH",
    help="file or directory of test files to run (default: if/)",
)
arg_parser.add_argument(
    "--gcc",
    metavar="PATH",
    help="name or path of the gcc cross compilation binary (default: riscv64-linux-gnu-gcc)",
)
arg_parser.add_argument(
    "--qemu",
    metavar="PATH",
    help="name or path of the qemu binary (default: qemu-riscv64-static)",
)
arg_parser.add_argument(
    "--py",
    metavar="PATH",
    help="name or path of the python3.12 binary (default: python3.12)",
)
args = arg_parser.parse_args()

if args.src is None:
    paths = [ p for p in Path(TEST_DIR).iterdir() if p.is_dir() ]
    paths.sort()
else:
    paths = [ Path(args.src) ]

gcc_bin = "riscv64-linux-gnu-gcc" if args.gcc is None else Path(args.gcc)
qemu_bin = "qemu-riscv64-static" if args.gcc is None else Path(args.qemu)
python_bin = "python3.12" if args.py is None else Path(args.py)

src_paths = []
for p in paths:
    if p.is_dir():
        src_paths2 = list(p.glob("*.py"))
        src_paths2.sort()
        print(f"Running tests for python files in directory {p}:")
        for p2 in src_paths2:
            print(f"  {p2.name}")
        src_paths += src_paths2
    else:
        print(f"Running tests for file {p}")
        src_paths = [p]

input_paths = [p.with_suffix(".in") for p in src_paths]

print()

def run_with_input(args: list[str | Path], input: bytes) -> tuple[int, str]:
    res = run(args, stdout=PIPE, stderr=STDOUT, input=input)
    return res.returncode, res.stdout.decode("utf-8")

def run_interpreter(src_path: Path, input: bytes, verbose: bool) -> tuple[int, str]:
    args = [python_bin, INTERPRETER_PATH, "-i", str(src_path)]
    if verbose:
        args.append("-V")
    return run_with_input(args, input_)

def run_compiler(src_path: Path, tgt_path: Path, verbose: bool) -> tuple[int, str]:
    args = [
        python_bin,
        str(BASE_DIR / "src" / "compiler.py"),
        "-i",
        str(src_path),
        "-o",
        str(asm_path),
    ]
    if verbose:
        args.append("-V")
    return run_with_input(args, b"")

def run_gcc(src_path: Path, runtime_path: Path, tgt_path: Path) -> tuple[int, str]:
    args = [gcc_bin, "-static", str(src_path), str(runtime_path), "-o", str(tgt_path)]
    return run_with_input(args, b"")

def run_qemu(prog_path: Path, input: bytes) -> tuple[int, str]:
    args = [qemu_bin, str(prog_path)]
    return run_with_input(args, input)

passed: list[Path] = []
failed: list[Path] = []

tmp_dir = BASE_DIR / "tmp"
try:
    rmtree(tmp_dir)
except Exception:
    pass
tmp_dir.mkdir()

ANSI_ERASE_LINE = "\33[2K"

for i, (src_path, input_path) in enumerate(zip(src_paths, input_paths)):
    print(f"{ANSI_ERASE_LINE}Running test {i+1} / {len(src_paths)}: {src_path}...\r", end="")
    if input_path.exists():
        input_ = input_path.read_bytes()
    else:
        input_ = b""

    (exit_code, interpreter_output) = run_interpreter(src_path, input_, verbose=False)
    if exit_code != 0:
        (exit_code, interpreter_output) = run_interpreter(src_path, input_, verbose=True)
        failed += [src_path]
        print("––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––")
        print(f"Running interpreter failed on source '{src_path.name}'.")
        print()
        print("Source:")
        print()
        print(indent(src_path.read_text().strip(), " " * 4))
        print()
        if input_path.exists():
            print("Input:")
            print()
            print(indent(input_.decode("utf-8").strip(), " " * 4))
            print()
        print("Error:")
        print()
        print(indent(interpreter_output, " " * 4))
        print()
        continue

    asm_path = tmp_dir / Path(src_path.name).with_suffix(".S")

    (exit_code, compiler_output) = run_compiler(src_path, asm_path, verbose=True)
    if exit_code != 0:
        failed += [src_path]
        print("––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––")
        print(f"Running compiler failed on source '{src_path.name}'.")
        print()
        print("Source:")
        print()
        print(indent(src_path.read_text().strip(), " " * 4))
        print()
        print("Error:")
        print()
        print(indent(compiler_output, " " * 4))
        print()
        continue

    prog_path = tmp_dir / asm_path.with_suffix("")

    (exit_code, gcc_output) = run_gcc(asm_path, RUNTIME_PATH, prog_path)
    if exit_code != 0:
        failed += [src_path]
        print("––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––")
        print(f"Running gcc failed on source '{src_path.name}'.")
        print()
        print("Source:")
        print()
        print(indent(src_path.read_text().strip(), " " * 4))
        print()
        print("Error:")
        print()
        print(indent(gcc_output, " " * 4))
        print()
        continue

    (exit_code, qemu_output) = run_qemu(prog_path, input_)
    if exit_code != 0:
        failed += [src_path]
        print("––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––")
        print(f"Running qemu failed on source '{src_path.name}'.")
        print()
        print("Source:")
        print()
        print(indent(src_path.read_text().strip(), " " * 4))
        print()
        print("Exit Code:")
        print()
        print(indent(str(exit_code), " " * 4))
        print()
        print("Output:")
        print()
        print(indent(qemu_output, " " * 4))
        print()
        continue

    if interpreter_output != qemu_output:
        failed += [src_path]
        print("––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––")
        print(f"Interpreter and compiled program produce different outputs on source '{src_path.name}'.")
        print()
        print("Source:")
        print()
        print(indent(src_path.read_text().strip(), " " * 4))
        print()
        print("Interpreter Output:")
        print()
        print(indent(interpreter_output, " " * 4))
        print()
        print("Compiled Program Output:")
        print()
        print(indent(qemu_output, " " * 4))
        print()
        continue

    passed += [src_path]
    # print(res)

print("––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––")
print(f"{len(passed)} / {len(src_paths)} tests passed.")
if len(failed) > 0:
    print()
    print("The following tests failed:")
    for p in failed:
        print(f"  {p.name}")
