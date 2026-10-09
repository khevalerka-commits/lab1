# Задание 4. Накопление состояния в цикле (без sum()).
numbers = [12, -5, 8, -3, 21, 0, 14, -7]

total = 0            # сумма всех чисел
positive_sum = 0     # сумма положительных
positive_count = 0   # количество положительных
negative_count = 0   # количество отрицательных
zero_count = 0       # количество нулей

print("Итерация | число | total | positive_sum | pos | neg | zero")
iteration = 0
for number in numbers:
    iteration += 1
    total = total + number
    if number > 0:
        positive_sum = positive_sum + number
        positive_count += 1
    elif number < 0:
        negative_count += 1
    else:
        zero_count += 1
    print(f"{iteration:^8} | {number:^5} | {total:^5} | {positive_sum:^12} | {positive_count:^3} | {negative_count:^3} | {zero_count:^4}")

print("Сумма всех чисел:", total)
print("Сумма положительных:", positive_sum)
print("Положительных:", positive_count)
print("Отрицательных:", negative_count)
print("Нулей:", zero_count)
