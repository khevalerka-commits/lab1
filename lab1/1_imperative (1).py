# Вариант 9: подсчитать числа, кратные пяти.
# Императивный стиль: последовательность команд и явное изменение состояния.

numbers = [5, 10, 7, 15, 22, 30, 4, 25, 9, 40, 3, 12]

count = 0             # изменяемое состояние: счётчик (накопитель)
multiples = []        # изменяемое состояние: список найденных чисел
iterations = 0        # изменяемое состояние: число итераций цикла

for number in numbers:
    iterations += 1
    if number % 5 == 0:
        multiples.append(number)
        count += 1
        print(f"Итерация {iterations}: {number} кратно 5, count = {count}")
    else:
        print(f"Итерация {iterations}: {number} не кратно 5")

print("Исходный список:", numbers)
print("Числа, кратные пяти:", multiples)
print("Количество итераций цикла:", iterations)
print("Количество чисел, кратных пяти:", count)
