# Вариант 9: подсчитать числа, кратные пяти.
# Объектно-ориентированный стиль: данные и операции объединены в классе.

class NumberCollection:
    """Коллекция целых чисел с операциями над ней."""

    def __init__(self, numbers):
        # Защищённый атрибут: копия данных, скрытая от внешнего кода (инкапсуляция).
        # list(...) копирует входной список, чтобы внешние изменения его не портили.
        self._numbers = list(numbers)

    def get_multiples_of_five(self):
        return [n for n in self._numbers if n % 5 == 0]

    def count_multiples_of_five(self):
        return len(self.get_multiples_of_five())

    def count_even_numbers(self):
        return len([n for n in self._numbers if n % 2 == 0])

    def find_maximum(self):
        return max(self._numbers) if self._numbers else None

    def calculate_average(self):
        return sum(self._numbers) / len(self._numbers) if self._numbers else None


first = NumberCollection([5, 10, 7, 15, 22, 30, 4, 25, 9, 40, 3, 12])
print("Объект 1: кратные 5:", first.get_multiples_of_five())
print("Объект 1: количество кратных 5:", first.count_multiples_of_five())
print("Объект 1: чётных чисел:", first.count_even_numbers())
print("Объект 1: максимум:", first.find_maximum())
print("Объект 1: среднее:", round(first.calculate_average(), 2))

second = NumberCollection([1, 2, 3, 4, 50, 55, 60, 61])
print("Объект 2: кратные 5:", second.get_multiples_of_five())
print("Объект 2: количество кратных 5:", second.count_multiples_of_five())
print("Объект 2: чётных чисел:", second.count_even_numbers())
print("Объект 2: максимум:", second.find_maximum())
print("Объект 2: среднее:", round(second.calculate_average(), 2))
