# Gemini 3.5 Flash Lite Test Function (Issue #9)

Реализация тестовой функции в рамках задачи #9 по проверке возможностей блокнота и репозитория.

```python
def gemini_fibonacci(n: int) -> list[int]:
    """
    Возвращает первые n чисел Фибоначчи.
    Тестовая функция для демонстрации работы агента Google Gemini 3.5 Flash Lite.
    """
    if n <= 0:
        return []
    if n == 1:
        return [0]
    fib = [0, 1]
    while len(fib) < n:
        fib.append(fib[-1] + fib[-2])
    return fib

if __name__ == "__main__":
    print("Gemini 3.5 Flash Lite Fibonacci test:", gemini_fibonacci(10))
```
