# Вариант 9: подсчитать числа, кратные пяти.
# Процедурный стиль: решение разбито на функции, каждая решает одну подзадачу.

def is_multiple_of_five(number: int) -> bool:
    """Проверка: делится ли число на 5 без остатка."""
    return number % 5 == 0


def get_multiples_of_five(values: list[int]) -> list[int]:
    """Возвращает новый список чисел, кратных пяти."""
    result = []
    for number in values:
        if is_multiple_of_five(number):
            result.append(number)
    return result


def count_multiples_of_five(values: list[int]) -> int:
    """Подсчитывает количество чисел, кратных пяти."""
    return len(get_multiples_of_five(values))


def main() -> None:
    numbers = [5, 10, 7, 15, 22, 30, 4, 25, 9, 40, 3, 12]

    # Проверка отдельных функций отдельными вызовами
    print("is_multiple_of_five(15):", is_multiple_of_five(15))
    print("is_multiple_of_five(7): ", is_multiple_of_five(7))
    print("is_multiple_of_five(0): ", is_multiple_of_five(0))
    print("is_multiple_of_five(-5):", is_multiple_of_five(-5))

    print("Исходный список:", numbers)
    print("Числа, кратные пяти:", get_multiples_of_five(numbers))
    print("Количество:", count_multiples_of_five(numbers))


if __name__ == "__main__":
    main()
