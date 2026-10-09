"""Демонстрация областей видимости LEGB (дополнительный пример)."""
x = "global"                      # G — глобальная область модуля


def outer():
    x = "enclosing"                # E — охватывающая область
    def inner():
        x = "local"                # L — локальная область
        return x
    return inner(), x


def make_call_counter():
    count = 0                      # E — состояние в охватывающей функции
    def register_call():
        nonlocal count             # разрешает изменить count из E
        count += 1
        return count
    return register_call


print("Local/Enclosing:", outer())
print("Global:", x)
print("Built-in:", len([1, 2, 3]))      # len ищется в B
counter = make_call_counter()
print("Счётчик:", counter(), counter(), counter())
