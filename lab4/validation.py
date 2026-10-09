"""Проверка типов, обязательных полей и диапазонов."""


def validate_scores(scores):
    """Возвращает проверенную копию последовательности баллов."""
    if not isinstance(scores, (list, tuple)):
        raise TypeError("scores должен быть списком или кортежем")
    checked = []
    for score in scores:
        if isinstance(score, bool) or not isinstance(score, (int, float)):
            raise TypeError("Балл должен быть числом")
        if not 0 <= score <= 100:
            raise ValueError("Балл должен быть от 0 до 100")
        checked.append(float(score))
    return checked


def validate_student(student):
    """Проверяет обязательные поля записи студента."""
    if not isinstance(student, dict):
        raise TypeError("Запись студента должна быть словарём")
    required = {"id", "name", "scores"}
    missing = required - student.keys()
    if missing:
        raise ValueError(f"Отсутствуют поля: {sorted(missing)}")


def validate_pass_mark(pass_mark):
    """Проверяет порог допуска (число от 0 до 100) и возвращает его как float."""
    if isinstance(pass_mark, bool) or not isinstance(pass_mark, (int, float)):
        raise TypeError("Порог допуска должен быть числом")
    if not 0 <= pass_mark <= 100:
        raise ValueError("Порог допуска должен быть от 0 до 100")
    return float(pass_mark)
