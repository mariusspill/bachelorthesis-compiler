from dataclasses import dataclass

@dataclass(frozen=True)
class Label:
    label: str

    def __str__(self) -> str:
        return self.label

    @staticmethod
    def fresh(s: str) -> 'Label':
        global fresh_label_counter
        x = f"{s}_{fresh_label_counter}"
        fresh_label_counter += 1
        return Label(x)

fresh_label_counter = 0
