
"""
Модуль для анализа текстовой статистики (разработано для issue #13).
Содержит функцию text_stats, вспомогательные утилиты и встроенные тесты.
"""

import re
from collections import Counter


def top_words(text: str, limit: int = 3) -> list:
    """Возвращает топ самых частых слов в тексте (без учёта регистра).
    Детерминированная сортировка: сначала по частоте (убывание), затем по алфавиту.
    """
    if not isinstance(text, str):
        raise TypeError("Аргумент text должен быть строкой")
    if not isinstance(limit, int) or limit < 0:
        raise ValueError("Параметр limit должен быть неотрицательным целым числом")

    if not text.strip() or limit == 0:
        return []

    # Ищем слова (поддерживаем латиницу, кириллицу, дефисы и апострофы внутри слов)
    words = re.findall(r"[a-zA-Zа-яА-ЯёЁ0-9]+(?:[-'][a-zA-Zа-яА-ЯёЁ0-9]+)*", text.lower())
    # Исключаем чисто числовые токены, если нужно считать только слова
    alpha_words = [w for w in words if not w.isdigit()]

    if not alpha_words:
        return []

    counts = Counter(alpha_words)
    # Сортировка: частота по убыванию (-count), затем слово по возрастанию (w)
    sorted_items = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return [word for word, count in sorted_items[:limit]]


def text_stats(text: str, top: int = 3) -> dict:
    """Возвращает подробную статистику по переданному тексту:
    - chars: всего символов
    - chars_no_ws: символов без пробельных
    - words: всего слов
    - unique_words: уникальных слов
    - lines: количество строк
    - top_words: список самых частых слов
    """
    if not isinstance(text, str):
        raise TypeError("Аргумент text должен быть строкой")

    chars = len(text)
    chars_no_ws = len(re.sub(r"\s", "", text))
    lines = len(text.splitlines()) if text else 0

    words_raw = re.findall(r"[a-zA-Zа-яА-ЯёЁ0-9]+(?:[-'][a-zA-Zа-яА-ЯёЁ0-9]+)*", text.lower())
    words = [w for w in words_raw if not w.isdigit()]

    return {
        "chars": chars,
        "chars_no_ws": chars_no_ws,
        "words": len(words),
        "unique_words": len(set(words)),
        "lines": lines,
"""Issue #13 — тестовое задание: небольшой код функции на Python.

Автор: агент `anthropic/claude-opus-5@default`
Ветка: `anthropic-claude-opus-5-default-issue-13`
Репозиторий: mlaa4ml/KaggleModelsRepo

Задача из issue #13: "создать небольшой код функции или какого-то действия
на любом языке программирования и записать его в файл, предложив для внесения
в главную ветку проекта".

Модуль самодостаточен: не требует зависимостей, запускается как скрипт и
сам прогоняет свои проверки (`python solutions/issue13_text_stats.py`).
"""

from __future__ import annotations

import re
import sys
from collections import Counter

__all__ = ["text_stats", "top_words", "run_self_test"]

_WORD_RE = re.compile(r"[^\W\d_]+(?:[-'][^\W\d_]+)*", flags=re.UNICODE)


def top_words(text: str, limit: int = 3) -> list[tuple[str, int]]:
    """Вернуть `limit` самых частых слов в виде списка пар (слово, частота).

    Слова приводятся к нижнему регистру. При равной частоте порядок
    детерминирован: сначала по убыванию частоты, затем по алфавиту.

    >>> top_words("Ab ab bc", limit=2)
    [('ab', 2), ('bc', 1)]
    """
    if limit < 0:
        raise ValueError("limit не может быть отрицательным")
    words = [w.lower() for w in _WORD_RE.findall(text or "")]
    counter = Counter(words)
    ordered = sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))
    return ordered[:limit]


def text_stats(text: str, top: int = 3) -> dict:
    """Посчитать простую статистику по строке текста.

    Возвращает словарь с ключами:
      * chars        — всего символов;
      * chars_no_ws  — символов без пробельных;
      * words        — всего слов;
      * unique_words — уникальных слов (без учёта регистра);
      * lines        — непустых строк;
      * top_words    — список пар (слово, частота).

    >>> stats = text_stats("Привет мир. Привет!")
    >>> stats["words"], stats["unique_words"]
    (3, 2)
    """
    if text is None:
        raise TypeError("text не может быть None")
    if not isinstance(text, str):
        raise TypeError(f"ожидалась строка, получено {type(text).__name__}")

    words = [w.lower() for w in _WORD_RE.findall(text)]
    return {
        "chars": len(text),
        "chars_no_ws": len("".join(text.split())),
        "words": len(words),
        "unique_words": len(set(words)),
        "lines": len([ln for ln in text.splitlines() if ln.strip()]),
        "top_words": top_words(text, limit=top),
    }


def run_self_test():
    """Встроенные тесты для проверки корректности работы функций."""
    sample = "Привет, мир! Привет всем. Это тест номер один, два и три. Тест-тест!"
    stats = text_stats(sample, top=2)

    assert stats["words"] > 0, "Количество слов должно быть больше 0"
    assert "привет" in stats["top_words"], "Слово 'привет' должно быть в топе"
    assert stats["lines"] == 1

    # Проверка обработки пустой строки
    empty_stats = text_stats("")
    assert empty_stats["chars"] == 0
    assert empty_stats["words"] == 0
    assert empty_stats["top_words"] == []

    # Проверка обработки исключений
    try:
        text_stats(None)
        raise AssertionError("Должен был вылететь TypeError")
    except TypeError:
        pass

    print("SELF-TEST OK: все проверки пройдены.")


if __name__ == "__main__":
    run_self_test()
    demo_text = "GitHub Copilot and Gemini agents are great tools for agentic workflows!"
    print(f"Демо анализ текста: {text_stats(demo_text, top=3)}")
def run_self_test() -> bool:
    """Мини-набор проверок без внешних зависимостей. True, если всё ок."""
    failures: list[str] = []

    def check(name: str, got, expected) -> None:
        if got != expected:
            failures.append(f"{name}: получено {got!r}, ожидалось {expected!r}")

    empty = text_stats("")
    check("empty.words", empty["words"], 0)
    check("empty.unique_words", empty["unique_words"], 0)
    check("empty.lines", empty["lines"], 0)
    check("empty.top_words", empty["top_words"], [])

    s = text_stats("Привет мир.\n\nПривет, GitHub!", top=2)
    check("ru.words", s["words"], 4)
    check("ru.unique_words", s["unique_words"], 3)
    check("ru.lines", s["lines"], 2)
    check("ru.top_words[0]", s["top_words"][0], ("привет", 2))

    check("hyphen", top_words("well-known well-known ok"), [("well-known", 2), ("ok", 1)])
    check("digits_skipped", text_stats("2026 год")["words"], 1)
    check("tie_break", top_words("b a", limit=2), [("a", 1), ("b", 1)])
    check("limit_zero", top_words("a b c", limit=0), [])

    for bad, exc in ((None, TypeError), (123, TypeError)):
        try:
            text_stats(bad)
        except exc:
            pass
        else:
            failures.append(f"text_stats({bad!r}) не выбросил {exc.__name__}")

    try:
        top_words("a", limit=-1)
    except ValueError:
        pass
    else:
        failures.append("top_words(limit=-1) не выбросил ValueError")

    if failures:
        print("SELF-TEST FAILED:")
        for f in failures:
            print("  -", f)
        return False

    print("SELF-TEST OK: 12/12 проверок пройдено")
    return True


def main(argv: list[str]) -> int:
    if len(argv) > 1:
        sample = " ".join(argv[1:])
    else:
        sample = (
            "Agentic GitHub Benchmark. Агент читает issue, "
            "создаёт ветку и предлагает изменения. Агент отчитывается."
        )
    for key, value in text_stats(sample).items():
        print(f"{key:>12}: {value}")
    print("-" * 40)
    return 0 if run_self_test() else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
