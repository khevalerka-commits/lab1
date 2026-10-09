# Вариант 9: подсчитать числа, кратные пяти.
# Функциональный стиль: композиция отбора, преобразования и суммирования
# без изменяемых переменных и без побочных эффектов.

numbers = [5, 10, 7, 15, 22, 30, 4, 25, 9, 40, 3, 12]

# 1) filter + map + sum: каждое подходящее число превращается в 1, единицы суммируются
result_map = sum(map(lambda n: 1, filter(lambda n: n % 5 == 0, numbers)))

# 2) генераторное выражение
result_gen = sum(1 for n in numbers if n % 5 == 0)

# 3) отдельный список кратных пяти (list comprehension)
multiples = [n for n in numbers if n % 5 == 0]

# 4) len от отфильтрованной последовательности
result_len = len(list(filter(lambda n: n % 5 == 0, numbers)))

print("Кратные пяти:", multiples)
print("filter + map + sum:", result_map)
print("генераторное выражение:", result_gen)
print("len(filter):", result_len)
