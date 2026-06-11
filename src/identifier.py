from dataclasses import dataclass

@dataclass(frozen=True)
class Id:
    name: str

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def fresh(s: str) -> 'Id':
        global fresh_id_counter
        x = f"{s}:{fresh_id_counter}"
        fresh_id_counter += 1
        return Id(x)

fresh_id_counter = 0
