import functools
from dataclasses import dataclass
import pprint
from itertools import combinations
import math
import time
from typing import TypeVar, Generic


@functools.cache
def is_connected(graph):
    if len(graph) <= 1:
        return True
    else:
        stack = [graph[0][0]]
        visited_nodes = set()
        while len(stack) > 0:
            node = stack.pop()
            if node not in visited_nodes:
                visited_nodes.add(node)
                for b in graph:
                    if b[0] == node:
                        for u in b[2]:
                            stack.append(u)
        for x in graph:
            if x[0] not in visited_nodes:
                return False
        return True


@functools.cache
def segments(graph):
    subgraphs = []
    for i in range(1, math.floor(len(graph) / 2) + 1):
        for part1 in combinations(graph, i):
            if is_connected(part1):
                part2 = ()
                for j in range(len(graph)):
                    if graph[j] not in part1:
                        part2 = part2 + (graph[j],)
                if is_connected(part2):
                    subgraphs.append((part1, part2))
    return subgraphs


@functools.cache
def solve(graph, color):
    if len(graph) == 0:
        return Solution(0, (), (), ())
    elif len(graph) == 1:
        return Solution(0, (graph[0],), (color,), ()) \
            if graph[0][1] == color \
            else Solution(1, (graph[0],), (color,), ())
    else:
        values = []
        colorlist = []
        for i in range(len(graph)):
            colorlist.append(graph[i][1])
        colors = set(colorlist)
        for (a, b) in segments(graph):
            for e in colors:
                for d in colors:
                    solution1 = solve(a, e)
                    solution2 = solve(b, d)
                    values.append(
                        Solution(
                            solution1.cost + solution2.cost + int(e != d) +
                            int(e != color and d != color),
                            (a, b), (e, d), (solution1, solution2)))
        return min(values, key=lambda t: t.cost)


Color = TypeVar("Color")


@dataclass
class Solution(Generic[Color]):
    cost: int
    segs: (int, Color, tuple[int, ...])
    colors: (Color, Color)
    children: ("Solution", "Solution")


def main():
    graph = (
        (1, "türkis", (4, )),
        (2, "türkis", (3, 4)),
        (3, "grau", (2, 5, 6, 7)),
        (4, "grau", (1, 2, 5, 7, 8, 11)),
        (5, "türkis", (3, 4, 7)),
        (6, "türkis", (3, 7, 10)),
        (7, "rot", (3, 4, 5, 6, 9, 10, 14)),
        (8, "türkis", (4, 9, 11)),
        (9, "grau", (7, 8, 11, 12, 14)),
        (10, "grau", (6, 7, 14)),
        (11, "rot", (4, 8, 9, 13, 14, 16)),
        (12, "rot", (9, 14)),
        (13, "grau", (11, 15)),
        (14, "türkis", (7, 9, 10, 11, 12, 16, 17)),
        (15, "türkis", (13, 16)),
        (16, "grau", (11, 15, 17)),
        (17, "grau", (14, 18)),
        (18, "türkis", (17, ))
    )

    solution = solve(graph, "türkis")
    pp = pprint.PrettyPrinter()
    pp.pprint(solution)


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
