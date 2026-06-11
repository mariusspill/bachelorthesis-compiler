from dataclasses import dataclass
from util.immutable_list import IList
from identifier import Id

# Type Syntax

type Type = TBool | TInt | TNone | TTuple | TCallable | TClass

@dataclass(frozen=True)
class TBool:
    pass

@dataclass
class TInt:
    pass

@dataclass
class TNone:
    pass

@dataclass
class TTuple:
    ts: IList[Type]

@dataclass
class TCallable:
    param_tys: IList[Type]
    ret_ty: Type


@dataclass
class TClass:
    name: Id
    _fields: IList[tuple[Id, Type]] | None = None # set during type checking

    def __eq__(self, other: object) -> bool:
        if type(other) is TClass:
            return self.name == other.name
        return False

# Pretty Printing

def pretty_type(t: Type) -> str:
    match t:
        case TBool():
            return "bool"
        case TInt():
            return "int"
        case TNone():
            return "None"
        case TTuple(ts):
            return f"tuple[{pretty_types(ts)}]"
        case TCallable(param_tys, ret_ty):
            return f"Callable[[{pretty_types(param_tys)}], {pretty_type(ret_ty)}]"
        case TClass(name, _fields):
            return f"{name}"

def pretty_types(ts: IList[Type]) -> str:
    return ", ".join(pretty_type(t) for t in ts)
