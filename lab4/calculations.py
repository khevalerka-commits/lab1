"""Предметные расчёты: среднее значение и статус допуска."""

PASSING_AVERAGE = 50  # порог допуска по умолчанию


def calculate_average(scores):
    """Возвращает среднее или None для пустой последовательности."""
    return sum(scores) / len(scores) if scores else None


def determine_status(average, pass_mark=PASSING_AVERAGE):
    """Возвращает статус по среднему баллу и настраиваемому порогу допуска."""
    if average is None:
        return "нет данных"
    return "допущен" if average >= pass_mark else "не допущен"
