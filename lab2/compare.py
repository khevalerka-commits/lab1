# Сравнительное задание: сумма положительных чисел.
numbers = [-4, 7, -2, 10, 5, -8]

# Императивный стиль
total = 0
for number in numbers:
    if number > 0:
        total = total + number
        print("total после", number, "=", total)
print("Императивно:", total)

# Декларативная запись
total = sum(number for number in numbers if number > 0)
print("Декларативно:", total)
