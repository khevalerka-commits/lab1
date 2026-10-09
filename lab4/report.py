"""Преобразование результатов в текст (без печати)."""


def format_average(value):
    """Форматирует среднее значение; для None возвращает тире."""
    return "—" if value is None else f"{value:.2f}"


def format_rating(rows):
    """Возвращает текст рейтинга группы."""
    lines = ["Рейтинг группы"]
    for position, row in enumerate(rows, start=1):
        average = format_average(row["average"])
        lines.append(
            f"{position}. {row['name']}: {average} — {row['status']}"
        )
    return "\n".join(lines)
