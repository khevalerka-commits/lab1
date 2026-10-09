import ast
import pathlib
import unittest

from university_rating import build_rating, build_student_result
from university_rating.calculations import calculate_average, determine_status
from university_rating.report import format_rating
from university_rating.validation import validate_pass_mark, validate_scores


def student(student_id, name, scores):
    return {"id": student_id, "name": name, "scores": scores}


class RatingTests(unittest.TestCase):
    # ---- базовая часть ----
    def test_empty_average(self):
        self.assertIsNone(calculate_average([]))

    def test_status_boundary(self):
        self.assertEqual(determine_status(49.99), "не допущен")
        self.assertEqual(determine_status(50), "допущен")

    def test_invalid_score(self):
        with self.assertRaises(ValueError):
            validate_scores([80, 101])

    def test_score_wrong_types(self):
        with self.assertRaises(TypeError):
            validate_scores(["80"])
        with self.assertRaises(TypeError):
            validate_scores([True])

    def test_score_limits_are_valid(self):
        self.assertEqual(validate_scores([0, 100]), [0.0, 100.0])

    def test_source_is_not_changed(self):
        students = [{"id": 1, "name": "Test", "scores": [70, 80]}]
        before = [{"id": 1, "name": "Test", "scores": [70, 80]}]
        build_rating(students)
        self.assertEqual(students, before)

    def test_empty_students_list(self):
        self.assertEqual(build_rating([]), [])

    def test_empty_scores_status(self):
        result = build_student_result(student(1, "Mira", []))
        self.assertIsNone(result["average"])
        self.assertEqual(result["status"], "нет данных")

    def test_missing_name_field(self):
        with self.assertRaises(ValueError) as ctx:
            build_rating([{"id": 1, "scores": [70]}])
        self.assertIn("name", str(ctx.exception))

    def test_no_average_goes_last(self):
        rows = build_rating([student(1, "A", []), student(2, "B", [10])])
        self.assertEqual([r["name"] for r in rows], ["B", "A"])

    def test_equal_averages_stable_order(self):
        rows = build_rating([student(1, "X", [60]), student(2, "Y", [60]), student(3, "Z", [60])])
        self.assertEqual([r["name"] for r in rows], ["X", "Y", "Z"])
        self.assertEqual(rows, build_rating([student(1, "X", [60]), student(2, "Y", [60]), student(3, "Z", [60])]))

    def test_format_has_no_print_and_returns_text(self):
        text = format_rating(build_rating([student(1, "Mira", [])]))
        self.assertEqual(text, "Рейтинг группы\n1. Mira: — — нет данных")

    # ---- индивидуальное расширение (вариант 9): настраиваемый порог допуска ----
    def test_pass_mark_changes_status(self):
        students = [student(1, "Dias", [45, 52, 48])]        # среднее 48.33
        self.assertEqual(build_rating(students)[0]["status"], "не допущен")
        self.assertEqual(build_rating(students, pass_mark=40)[0]["status"], "допущен")
        self.assertEqual(build_rating(students, pass_mark=90)[0]["status"], "не допущен")

    def test_pass_mark_boundary_is_inclusive(self):
        self.assertEqual(determine_status(60, pass_mark=60), "допущен")
        self.assertEqual(determine_status(59.99, pass_mark=60), "не допущен")

    def test_pass_mark_limits_valid(self):
        self.assertEqual(validate_pass_mark(0), 0.0)
        self.assertEqual(validate_pass_mark(100), 100.0)

    def test_pass_mark_out_of_range_raises_value_error(self):
        for bad in (-1, 100.5):
            with self.assertRaises(ValueError):
                build_rating([student(1, "A", [70])], pass_mark=bad)

    def test_pass_mark_wrong_type_raises_type_error(self):
        for bad in ("50", True, None):
            with self.assertRaises(TypeError):
                build_rating([student(1, "A", [70])], pass_mark=bad)

    def test_pass_mark_does_not_change_order_or_average(self):
        students = [student(1, "A", [90]), student(2, "B", [40])]
        low = build_rating(students, pass_mark=10)
        high = build_rating(students, pass_mark=95)
        self.assertEqual([r["name"] for r in low], [r["name"] for r in high])
        self.assertEqual([r["average"] for r in low], [r["average"] for r in high])

    def test_empty_scores_ignore_pass_mark(self):
        self.assertEqual(build_rating([student(1, "M", [])], pass_mark=0)[0]["status"], "нет данных")


class StructureTests(unittest.TestCase):
    """Проверка направления зависимостей: низкоуровневые модули не импортируют main/report."""

    @staticmethod
    def imports_of(path):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        found = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.level == 1 and node.module:
                found.add(node.module)
        return found

    def test_no_import_cycles_and_correct_direction(self):
        package = pathlib.Path(__file__).resolve().parent.parent / "university_rating"
        names = ["validation", "calculations", "rating", "report", "main"]
        graph = {n: self.imports_of(package / f"{n}.py") for n in names}
        self.assertEqual(graph["validation"], set())
        self.assertEqual(graph["calculations"], set())
        self.assertEqual(graph["report"], set())
        self.assertEqual(graph["rating"], {"calculations", "validation"})
        self.assertEqual(graph["main"], {"rating", "report"})
        # поиск цикла обходом в глубину
        visiting, done = set(), set()

        def dfs(node):
            self.assertNotIn(node, visiting, "обнаружен циклический импорт")
            if node in done:
                return
            visiting.add(node)
            for dep in graph.get(node, ()):
                dfs(dep)
            visiting.discard(node)
            done.add(node)

        for name in names:
            dfs(name)


if __name__ == "__main__":
    unittest.main()
