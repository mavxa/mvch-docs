#!/usr/bin/env python3
"""Строит кратчайший маршрут по сетке маркеров 6x6 без ROS."""

import argparse
from collections import deque


SIZE = 6


def neighbors(marker: int):
    row, column = divmod(marker, SIZE)
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        next_row, next_column = row + dr, column + dc
        if 0 <= next_row < SIZE and 0 <= next_column < SIZE:
            yield next_row * SIZE + next_column


def build_route(start: int, target: int, blocked: set[int]):
    queue = deque([start])
    previous = {start: None}

    while queue:
        current = queue.popleft()
        if current == target:
            break
        for candidate in neighbors(current):
            if candidate not in blocked and candidate not in previous:
                previous[candidate] = current
                queue.append(candidate)

    if target not in previous:
        return None

    route = []
    current = target
    while current is not None:
        route.append(current)
        current = previous[current]
    return list(reversed(route))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("start", type=int, help="Стартовый маркер 0..35")
    parser.add_argument("target", type=int, help="Целевой маркер 0..35")
    parser.add_argument(
        "--blocked",
        type=int,
        nargs="*",
        default=[],
        help="Маркеры, через которые нельзя ехать",
    )
    args = parser.parse_args()

    if not 0 <= args.start < SIZE * SIZE or not 0 <= args.target < SIZE * SIZE:
        parser.error("start и target должны быть от 0 до 35")

    blocked = set(args.blocked)
    blocked.discard(args.start)
    blocked.discard(args.target)
    route = build_route(args.start, args.target, blocked)
    if route is None:
        raise SystemExit("Маршрут не найден")
    print(" -> ".join(map(str, route)))


if __name__ == "__main__":
    main()

