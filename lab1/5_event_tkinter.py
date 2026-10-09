# Вариант 9 (дополнительное задание): событийный стиль на tkinter.
# Вычисление запускается нажатием кнопки; ввод чисел через пробел.

import tkinter as tk


def parse_numbers(text: str) -> list[int]:
    """Преобразует строку '5 10 7' в список целых. Бросает ValueError при ошибке."""
    return [int(part) for part in text.split()]


def count_multiples_of_five(values: list[int]) -> int:
    return sum(1 for n in values if n % 5 == 0)


def calculate():
    """Обработчик события нажатия кнопки «Вычислить»."""
    try:
        values = parse_numbers(entry.get())
        if not values:
            raise ValueError("пустой ввод")
        count = count_multiples_of_five(values)
        result_label.config(text=f"Кратных пяти: {count}", fg="black")
    except ValueError:
        result_label.config(text="Ошибка: введите целые числа через пробел", fg="red")


def clear():
    """Обработчик события нажатия кнопки «Очистить»."""
    entry.delete(0, tk.END)
    result_label.config(text="Нажмите кнопку", fg="black")


root = tk.Tk()
root.title("Парадигмы программирования — вариант 9")

tk.Label(root, text="Числа через пробел:").pack(padx=20, pady=(10, 0))
entry = tk.Entry(root, width=40)
entry.insert(0, "5 10 7 15 22 30 4 25 9 40 3 12")
entry.pack(padx=20, pady=5)

result_label = tk.Label(root, text="Нажмите кнопку")
result_label.pack(padx=20, pady=10)

tk.Button(root, text="Вычислить", command=calculate).pack(padx=20, pady=5)
tk.Button(root, text="Очистить", command=clear).pack(padx=20, pady=(0, 10))

root.mainloop()
