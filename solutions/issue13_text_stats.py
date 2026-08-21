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
