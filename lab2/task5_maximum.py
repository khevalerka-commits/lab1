# Задание 5. Поиск максимума без max().
scores = [67, 82, 45, 91, 76, 88, 54]
maximum = scores[0]   # начальное состояние: первый элемент

print("score | maximum до | score > maximum | maximum после")
for score in scores:
    before = maximum
    if score > maximum:
        maximum = score          # изменение состояния
        condition = "да"
    else:
        condition = "нет"
    print(f"{score:^5} | {before:^10} | {condition:^15} | {maximum:^13}")

print("Максимум:", maximum)
