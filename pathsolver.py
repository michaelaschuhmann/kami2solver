import functools
from dataclasses import dataclass
import pprint
from typing import TypeVar, Generic


def split(path, i):
    path1 = path[0:i]
    path2 = path[i:]
    return path1, path2


def segments(path):
    segments = []
    for i in range(0, len(path)):
        if i != 0:
            segments.append(split(path, i))
    return segments


@functools.cache
def solve(path, color):
    if len(path) == 0:
        return Solution(0, (), (), ())
    elif len(path) == 1:
        return Solution(0, (path[0],), (color,), ()) \
            if path[0] == color else Solution(1, (path[0],), (color,), ())
    else:
        values = []
        for (a, b) in segments(path):
            for j in set(path):
                for i in set(path):
                    solution1 = solve(a, j)
                    solution2 = solve(b, i)
                    values.append(
                        Solution(
                            solution1.cost + solution2.cost + int(i != color)
                            + int(j != color)
                            - int(i != color and j != color and i == j),
                            (a, b), (i, j), (solution1, solution2)))
        return min(values, key=lambda t: t.cost)


Color = TypeVar("Color")


@dataclass
class Solution(Generic[Color]):
    cost: int
    segs: (tuple[int, ...], tuple[int, ...])
    colors: (Color, Color)
    children: ("Solution", "Solution")


def main():
    path = ("pink", "lila", "pink", "türkis", "pink", "lila", "pink", "lila")

    solution = solve(path, "pink")
    pp = pprint.PrettyPrinter()
    pp.pprint(solution)


if __name__ == "__main__":
    main()
