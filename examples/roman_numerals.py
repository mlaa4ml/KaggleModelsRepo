"""Небольшая самодостаточная утилита: конвертация римских чисел.

Тестовое задание из issue #9 — проверка работы новых инструментов
блокнота `benchmark_task_github_skill_v2.ipynb`.

Зависимостей нет, только стандартная библиотека. Запуск встроенных
проверок:

    python examples/roman_numerals.py
"""

from __future__ import annotations

# Пары идут от большего к меньшему, включая «вычитательные» формы (CM, XL, IV).
_VALUES: tuple[tuple[int, str], ...] = (
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
)

_DIGITS: dict[str, int] = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def to_roman(number: int) -> str:
    """Перевести целое число 1..3999 в римскую запись.

    >>> to_roman(1994)
    'MCMXCIV'
    """
    if not isinstance(number, int) or isinstance(number, bool):
        raise TypeError(f"ожидалось int, получено {type(number).__name__}")
    if not 1 <= number <= 3999:
        raise ValueError("поддерживается только диапазон 1..3999")

    parts: list[str] = []
    rest = number
    for value, symbol in _VALUES:
        count, rest = divmod(rest, value)
        parts.append(symbol * count)
    return "".join(parts)


def from_roman(roman: str) -> int:
    """Перевести римскую запись обратно в целое число.

    >>> from_roman('MCMXCIV')
    1994
    """
    if not isinstance(roman, str):
        raise TypeError(f"ожидалась str, получено {type(roman).__name__}")

    text = roman.strip().upper()
    if not text:
        raise ValueError("пустая строка")

    total = 0
    previous = 0
    for char in reversed(text):
        if char not in _DIGITS:
            raise ValueError(f"недопустимый символ: {char!r}")
        current = _DIGITS[char]
        if current < previous:
            total -= current
        else:
            total += current
            previous = current

    # Строгая проверка: канонической считается только та запись,
    # которую вернул бы to_roman() для полученного числа.
    if not 1 <= total <= 3999 or to_roman(total) != text:
        raise ValueError(f"неканоническая римская запись: {roman!r}")
    return total


def _self_test() -> None:
    cases = {
        1: "I",
        4: "IV",
        9: "IX",
        14: "XIV",
        40: "XL",
        90: "XC",
        400: "CD",
        1987: "MCMLXXXVII",
        1994: "MCMXCIV",
        2024: "MMXXIV",
        3999: "MMMCMXCIX",
    }
    for number, expected in cases.items():
        got = to_roman(number)
        assert got == expected, f"to_roman({number}) -> {got}, ожидалось {expected}"
        back = from_roman(expected)
        assert back == number, f"from_roman({expected!r}) -> {back}, ожидалось {number}"

    # round-trip по всему диапазону
    for number in range(1, 4000):
        assert from_roman(to_roman(number)) == number, number

    for bad in (0, -5, 4000):
        try:
            to_roman(bad)
        except ValueError:
            pass
        else:  # pragma: no cover
            raise AssertionError(f"to_roman({bad}) должен был бросить ValueError")

    for bad in ("", "IIII", "VV", "ABC", "IC"):
        try:
            from_roman(bad)
        except ValueError:
            pass
        else:  # pragma: no cover
            raise AssertionError(f"from_roman({bad!r}) должен был бросить ValueError")

    print("OK: все проверки пройдены (3999 round-trip + граничные случаи)")


if __name__ == "__main__":
    _self_test()
