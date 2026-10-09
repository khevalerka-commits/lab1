"""Результат одного студента и сортировка рейтинга."""
from .calculations import PASSING_AVERAGE, calculate_average, determine_status
from .validation import validate_pass_mark, validate_scores, validate_student


def build_student_result(student, pass_mark=PASSING_AVERAGE):
    """Формирует новую итоговую запись одного студента."""
    validate_student(student)
    pass_mark = validate_pass_mark(pass_mark)
    scores = validate_scores(student["scores"])
    average = calculate_average(scores)
    return {
        "id": student["id"],
        "name": student["name"],
        "average": average,
        "status": determine_status(average, pass_mark),
    }


def _sort_key(item):
    average = item["average"]
    return average is not None, average or 0


def build_rating(students, pass_mark=PASSING_AVERAGE):
    """Возвращает рейтинг, не изменяя исходные записи.

    pass_mark — порог допуска (по умолчанию 50), проверяется один раз.
    """
    pass_mark = validate_pass_mark(pass_mark)
    results = [build_student_result(item, pass_mark) for item in students]
    return sorted(results, key=_sort_key, reverse=True)
