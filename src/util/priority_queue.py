from dataclasses import dataclass, field

@dataclass
class PriorityQueue[T]:
    """
    A (simulated) heap structure that has the element with the maximum priority on top.
    """

    @dataclass(order=True)
    class Item:
        """
        An item in the max-heap.
        """

        # ignored when heap property is checked
        item: T = field(compare=False) # type: ignore
        priority: int

    # the list of items in the simulated heap
    # invariant: always sorted
    _heap: list[Item] = field(default_factory=lambda: [])

    def push(self, item: T, priority: int) -> None:
        """
        Pushes an new item to the heap.
        """
        self._heap.append(self.Item(item, priority))
        self._heap.sort()

    def pop(self) -> T:
        """
        Pops an element with maximum priority.
        If the heap is empty, then an IndexError is raised.
        """
        return self._heap.pop().item

    def increment(self, item: T) -> None:
        """
        Increments the priority of the given item by one.
        If the given item is not present in the heap, then the function returns without any action.
        If the given item is present multiple times, then the function picks the item with the smallest priority.
        """
        try:
            idx, priority = next(
                (idx, i.priority) for idx, i in enumerate(self._heap) if i.item == item
            )
        except StopIteration:
            return

        self._heap[idx] = self.Item(item, priority + 1)
        self._heap.sort()

    def is_empty(self) -> bool:
        """
        Returns True if the heap is empty, False otherwise
        """
        return not bool(self._heap)

    def __bool__(self) -> bool:
        return not self.is_empty()
