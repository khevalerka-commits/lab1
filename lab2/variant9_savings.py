# Вариант 9. Накопительный счёт: начальный баланс 100 000, ежемесячно +2%.
# Выводится баланс каждого из 12 месяцев.

balance = 100000.0     # состояние: текущий баланс
rate_percent = 2       # ежемесячная ставка, %
months = 12            # количество месяцев

print(f"Начальный баланс: {balance:,.2f}")
print("Месяц | Начислено | Баланс")

for month in range(1, months + 1):
    interest = round(balance * rate_percent / 100, 2)  # проценты за месяц
    balance = round(balance + interest, 2)             # изменение состояния
    print(f"{month:^5} | {interest:>9,.2f} | {balance:>12,.2f}")

print(f"Итоговый баланс через {months} мес.: {balance:,.2f}")
print(f"Всего начислено процентов: {balance - 100000:,.2f}")
