"""Точка входа: python -m university_rating.main"""
from .rating import build_rating
from .report import format_rating


def load_demo_data():
    """Возвращает демонстрационные записи студентов."""
    return [
        {"id": 101, "name": "Amina", "scores": [88, 92, 79]},
        {"id": 102, "name": "Dias", "scores": [45, 52, 48]},
        {"id": 103, "name": "Mira", "scores": []},
    ]


def main():
    """Координирует вызовы и выводит результат."""
    students = load_demo_data()
    print(format_rating(build_rating(students)))          # порог по умолчанию (50)
    print()
    print("Порог допуска 40:")
    print(format_rating(build_rating(students, pass_mark=40)))
    print()
    print("Порог допуска 90:")
    print(format_rating(build_rating(students, pass_mark=90)))


if __name__ == "__main__":
    main()
