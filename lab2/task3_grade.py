# Задание 3. Определение оценки по баллу с проверкой ввода.
try:
    score = int(input("Введите балл (0-100): "))
except ValueError:
    score = None  # ввод не является целым числом

if score is None:
    print("Ошибка: нужно ввести целое число")
elif score < 0 or score > 100:
    print("Ошибка: балл должен быть в диапазоне 0-100")
elif score >= 90:
    print("Оценка: A")
elif score >= 75:
    print("Оценка: B")
elif score >= 50:
    print("Оценка: C")
else:
    print("Оценка: F")
