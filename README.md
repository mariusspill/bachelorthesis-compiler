# Nanopass Python-to-RISC-V Compiler with Floating-Point Support

A Nanopass-style compiler that translates a subset of Python to RISC-V assembly, originally built for the Compiler Construction lecture (supporting bools, ints, and tuples) and extended as part of a bachelor's thesis to add full floating-point support — literals, arithmetic, comparisons, int/float coercion, closures, and the garbage-collector changes needed to support boxed floats safely.

See [`thesis/`](thesis) for the full write-up: design decisions, implementation details, and evaluation.

## Structure

- [`src/`](src) — the compiler itself, organized as a sequence of small passes (parsing, type checking, closure conversion, heap allocation, instruction selection, register allocation, and more), each transforming one intermediate representation into the next.
- [`runtime/`](runtime) — the C runtime, including `print_int64`/`print_float` and the copying garbage collector.
- [`tests/`](tests) — the test suite, run against a reference interpreter; [`tests/float_ext/`](tests/float_ext) covers the floating-point extension specifically.
- [`thesis/`](thesis) — the LaTeX source of the accompanying bachelor's thesis.

## Usage

The `./do` script wraps everything in Docker (gcc for RISC-V, QEMU, Python):

```
./do compile PATH   # compile a Python source file to RISC-V assembly
./do run PATH        # compile and run it under QEMU
./do test [PATH]     # run the full test suite, or a specific test file/folder
./do shell           # open a shell inside the container
```

Pass `--no-docker` / `-nd` to run any command directly on the host instead.

## License

MIT — see [`LICENSE`](LICENSE).
