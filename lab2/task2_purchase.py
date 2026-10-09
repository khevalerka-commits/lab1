# Задание 2. Расчёт стоимости покупки со скидкой.
price = float(input("Цена товара: "))        # цена одного товара
quantity = int(input("Количество: "))        # количество товаров
discount_percent = float(input("Скидка: "))  # скидка в процентах

total_without_discount = price * quantity                         # стоимость без скидки
discount_amount = total_without_discount * discount_percent / 100  # размер скидки
total_to_pay = total_without_discount - discount_amount           # итог

print("Стоимость без скидки:", round(total_without_discount))
print("Размер скидки:", round(discount_amount))
print("К оплате:", round(total_to_pay))
