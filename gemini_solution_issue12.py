# Gemini 3.5 Flash Lite Test Function (Issue #12)

Реализация тестовой функции факториала и проверки простого числа для повторного теста работы в рамках задачи #12.

```python
def gemini_factorial(n: int) -> int:
    """
    Возвращает факториал числа n.
    Тестовая функция для демонстрации работы агента Google Gemini 3.5 Flash Lite (issue #12).
    """
    if n < 0:
        raise ValueError("Факториал определен только для неотрицательных чисел.")
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def gemini_is_prime(n: int) -> bool:
    """
    Проверяет, является ли число простым.
    """
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

if __name__ == "__main__":
    print("Gemini 3.5 Flash Lite Factorial test (5!):", gemini_factorial(5))
    print("Gemini 3.5 Flash Lite Prime test (17):", gemini_is_prime(17))
```
