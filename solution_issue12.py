#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Решение задачи из issue #12 репозитория mlaa4ml/KaggleModelsRepo.

Небольшой самодостаточный модуль на Python: несколько функций
для работы с последовательностями чисел + встроенные проверки.

Файл является ПОЛНОСТЬЮ исполняемым (в отличие от
`gemini_solution_issue9.py`, который имеет расширение .py,
но содержит Markdown и падает с SyntaxError при запуске).

Запуск:
    python3 solution_issue12.py
"""

from __future__ import annotations

from typing import Dict, Iterable, List


def fibonacci(n: int) -> List[int]:
    """Вернуть первые n чисел Фибоначчи (начиная с 0, 1).

    >>> fibonacci(7)
    [0, 1, 1, 2, 3, 5, 8]
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n должно быть целым числом")
    if n < 0:
        raise ValueError("n не может быть отрицательным")

    seq: List[int] = []
    a, b = 0, 1
    for _ in range(n):
        seq.append(a)
        a, b = b, a + b
    return seq


def is_prime(n: int) -> bool:
    """Проверить, является ли число простым.

    >>> [x for x in range(20) if is_prime(x)]
    [2, 3, 5, 7, 11, 13, 17, 19]
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n должно быть целым числом")
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    divisor = 3
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 2
    return True


def summarize(numbers: Iterable[float]) -> Dict[str, float]:
    """Посчитать простую статистику по набору чисел.

    Возвращает словарь с ключами: count, sum, min, max, mean.

    >>> summarize([1, 2, 3, 4]) == {
    ...     "count": 4, "sum": 10, "min": 1, "max": 4, "mean": 2.5}
    True
    """
    values = [float(x) for x in numbers]
    if not values:
        raise ValueError("Последовательность не должна быть пустой")
    total = sum(values)
    return {
        "count": len(values),
        "sum": total,
        "min": min(values),
        "max": max(values),
        "mean": total / len(values),
    }


def _run_self_tests() -> None:
    """Минимальный набор проверок без внешних зависимостей."""
    assert fibonacci(0) == []
    assert fibonacci(1) == [0]
    assert fibonacci(2) == [0, 1]
    assert fibonacci(10) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

    assert [x for x in range(20) if is_prime(x)] == [2, 3, 5, 7, 11, 13, 17, 19]
    assert is_prime(-7) is False
    assert is_prime(97) is True
    assert is_prime(1_000_003) is True

    stats = summarize([1, 2, 3, 4])
    assert stats["count"] == 4
    assert stats["sum"] == 10
    assert stats["min"] == 1
    assert stats["max"] == 4
    assert stats["mean"] == 2.5

    for func, arg, err in (
        (fibonacci, -1, ValueError),
        (fibonacci, "5", TypeError),
        (summarize, [], ValueError),
    ):
        try:
            func(arg)
        except err:
            pass
        else:  # pragma: no cover
            raise AssertionError(f"{func.__name__}({arg!r}) не выбросил {err.__name__}")

    print("Все self-тесты пройдены (12 проверок).")


def main() -> None:
    print("Issue #12 — тестовый исполняемый код")
    print("-" * 38)
    print("fibonacci(10) =", fibonacci(10))
    primes = [x for x in range(50) if is_prime(x)]
    print("простые < 50  =", primes)
    print("summarize     =", summarize(fibonacci(10)))
    print("-" * 38)
    _run_self_tests()


if __name__ == "__main__":
    main()
