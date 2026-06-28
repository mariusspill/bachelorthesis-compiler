from dataclasses import dataclass
from typing import Literal

from util.immutable_list import ilist

@dataclass(frozen=True)
class Register:
    type Name = Literal[
        "zero", "ra", "sp", "gp", "tp", "t0", "t1", "t2", "fp", "s1", "a0", "a1",
        "a2", "a3", "a4", "a5", "a6", "a7", "s2", "s3", "s4", "s5", "s6", "s7",
        "s8", "s9", "s10", "s11", "t3", "t4", "t5", "t6",
        "ft0", "ft1", "ft2", "ft3", "ft4", "ft5", "ft6", "ft7",
        "fs0", "fs1",
        "fa0", "fa1", "fa2", "fa3", "fa4", "fa5", "fa6", "fa7",
        "fs2", "fs3", "fs4", "fs5", "fs6", "fs7", "fs8", "fs9", "fs10", "fs11",
        "ft8", "ft9", "ft10", "ft11"
    ]
    name: Name

    def __str__(self) -> str:
        return self.name

zero = Register("zero") # hardwired zero
ra = Register("ra")     # return address
sp = Register("sp")     # stack pointer
gp = Register("gp")     # global pointer
tp = Register("tp")     # thread pointer
t0 = Register("t0")     # temporary register 0
t1 = Register("t1")     # temporary register 1
t2 = Register("t2")     # temporary register 2
fp = Register("fp")     # frame pointer / saved register 0
s1 = Register("s1")     # saved register 1
a0 = Register("a0")     # function argument 0 / return value 0
a1 = Register("a1")     # function argument 1 / return value 1
a2 = Register("a2")     # function argument 2
a3 = Register("a3")     # function argument 3
a4 = Register("a4")     # function argument 4
a5 = Register("a5")     # function argument 5
a6 = Register("a6")     # function argument 6
a7 = Register("a7")     # function argument 7
s2 = Register("s2")     # saved register 2
s3 = Register("s3")     # saved register 3
s4 = Register("s4")     # saved register 4
s5 = Register("s5")     # saved register 5
s6 = Register("s6")     # saved register 6
s7 = Register("s7")     # saved register 7
s8 = Register("s8")     # saved register 8
s9 = Register("s9")     # saved register 9
s10 = Register("s10")   # saved register 10
s11 = Register("s11")   # saved register 11
t3 = Register("t3")     # temporary register 3
t4 = Register("t4")     # temporary register 4
t5 = Register("t5")     # temporary register 5
t6 = Register("t6")     # temporary register 6
ft0 = Register("ft0")   # floating-point temporary register 0
ft1 = Register("ft1")   # floating-point temporary register 1
ft2 = Register("ft2")   # floating-point temporary register 2
ft3 = Register("ft3")   # floating-point temporary register 3
ft4 = Register("ft4")   # floating-point temporary register 4
ft5 = Register("ft5")   # floating-point temporary register 5
ft6 = Register("ft6")   # floating-point temporary register 6
ft7 = Register("ft7")   # floating-point temporary register 7
fs0 = Register("fs0")   # floating-point saved register 0
fs1 = Register("fs1")   # floating-point saved register 1
fa0 = Register("fa0")   # floating-point function argument 0 / return value 0
fa1 = Register("fa1")   # floating-point function argument 1 / return value 1
fa2 = Register("fa2")   # floating-point function argument 2
fa3 = Register("fa3")   # floating-point function argument 3
fa4 = Register("fa4")   # floating-point function argument 4
fa5 = Register("fa5")   # floating-point function argument 5
fa6 = Register("fa6")   # floating-point function argument 6
fa7 = Register("fa7")   # floating-point function argument 7
fs2 = Register("fs2")   # floating-point saved register 2
fs3 = Register("fs3")   # floating-point saved register 3
fs4 = Register("fs4")   # floating-point saved register 4
fs5 = Register("fs5")   # floating-point saved register 5
fs6 = Register("fs6")   # floating-point saved register 6
fs7 = Register("fs7")   # floating-point saved register 7
fs8 = Register("fs8")   # floating-point saved register 8
fs9 = Register("fs9")   # floating-point saved register 9
fs10 = Register("fs10") # floating-point saved register 10
fs11 = Register("fs11") # floating-point saved register 11
ft8 = Register("ft8")   # floating-point temporary register 8
ft9 = Register("ft9")   # floating-point temporary register 9
ft10 = Register("ft10") # floating-point temporary register 10
ft11 = Register("ft11") # floating-point temporary register 11

# a list of all callee saved registers
CALLEE_SAVED_REGISTERS = ilist(sp, fp, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11)

# a list of all caller saved registers
CALLER_SAVED_REGISTERS = ilist(ra, t0, t1, t2, a0, a1, a2, a3, a4, a5, a6, a7, t3, t4, t5, t6)

# a list of all registers used to store function arguments
FUNCTION_ARG_REGISTERS = ilist(a0, a1, a2, a3, a4, a5, a6, a7)
