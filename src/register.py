from dataclasses import dataclass
from typing import Literal

from util.immutable_list import ilist

@dataclass(frozen=True)
class Register:
    type Name = Literal[
        "zero", "ra", "sp", "gp", "tp", "t0", "t1", "t2", "fp", "s1", "a0", "a1",
        "a2", "a3", "a4", "a5", "a6", "a7", "s2", "s3", "s4", "s5", "s6", "s7",
        "s8", "s9", "s10", "s11", "t3", "t4", "t5", "t6",
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

# a list of all callee saved registers
CALLEE_SAVED_REGISTERS = ilist(sp, fp, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11)

# a list of all caller saved registers
CALLER_SAVED_REGISTERS = ilist(ra, t0, t1, t2, a0, a1, a2, a3, a4, a5, a6, a7, t3, t4, t5, t6)

# a list of all registers used to store function arguments
FUNCTION_ARG_REGISTERS = ilist(a0, a1, a2, a3, a4, a5, a6, a7)
