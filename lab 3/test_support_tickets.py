import unittest
from datetime import datetime

from support_tickets import (build_queue, filter_active, format_queue, is_breached,
                             priority_key, sla_deadline, status_counts, validate_ticket)


def make(ticket_id, priority="low", status="open", created=datetime(2026, 10, 9, 9, 0)):
    return {"id": ticket_id, "priority": priority, "created": created, "status": status}


class SupportTicketsTests(unittest.TestCase):
    def test_valid_ticket_returns_copy(self):
        source = make(1)
        result = validate_ticket(source)
        self.assertEqual(result, source)
        self.assertIsNot(result, source)

    def test_invalid_priority_raises_value_error(self):          # ошибочный сценарий 1
        with self.assertRaises(ValueError):
            validate_ticket(make(1, priority="urgent"))

    def test_bool_id_raises_type_error(self):                    # ошибочный сценарий 2
        with self.assertRaises(TypeError):
            validate_ticket(make(True))

    def test_created_must_be_datetime(self):                     # ошибочный сценарий 3
        bad = make(1)
        bad["created"] = "2026-10-09"
        with self.assertRaises(TypeError):
            validate_ticket(bad)

    def test_priority_key_order(self):
        older = make(1, "high", created=datetime(2026, 10, 8, 9, 0))
        newer = make(2, "high", created=datetime(2026, 10, 9, 9, 0))
        critical = make(3, "critical")
        ordered = sorted([newer, older, critical], key=priority_key)
        self.assertEqual([t["id"] for t in ordered], [3, 1, 2])

    def test_queue_contains_only_active_sorted(self):
        tickets = [make(1, "low"), make(2, "critical", "closed"),
                   make(3, "high", "in_progress"), make(4, "medium", "resolved")]
        self.assertEqual([t["id"] for t in build_queue(tickets)], [3, 1])

    def test_queue_does_not_change_input(self):
        tickets = [make(2, "low"), make(1, "high")]
        snapshot = [dict(t) for t in tickets]
        build_queue(tickets)
        self.assertEqual(tickets, snapshot)

    def test_empty_queue(self):
        self.assertEqual(build_queue([]), [])
        self.assertEqual(format_queue([], datetime(2026, 10, 9, 12, 0)), "Очередь пуста")

    def test_duplicate_ids_rejected(self):
        with self.assertRaises(ValueError):
            build_queue([make(1), make(1, "high")])

    def test_status_counts_includes_zero_statuses(self):
        counts = status_counts([make(1), make(2, status="closed")])
        self.assertEqual(counts, {"open": 1, "in_progress": 0, "resolved": 0, "closed": 1})

    def test_sla_boundary_exact_deadline_not_breached(self):      # граничный сценарий
        ticket = make(1, "critical", created=datetime(2026, 10, 9, 8, 0))   # SLA 4 ч
        deadline = sla_deadline(ticket)
        self.assertEqual(deadline, datetime(2026, 10, 9, 12, 0))
        self.assertFalse(is_breached(ticket, deadline))
        self.assertTrue(is_breached(ticket, datetime(2026, 10, 9, 12, 1)))

    def test_custom_sla_by_keyword(self):
        ticket = make(1, "low", created=datetime(2026, 10, 9, 9, 0))
        now = datetime(2026, 10, 9, 12, 0)
        self.assertFalse(is_breached(ticket, now))
        self.assertTrue(is_breached(ticket, now, sla_hours={"low": 2}))

    def test_filter_active_returns_new_list(self):
        tickets = [make(1)]
        self.assertIsNot(filter_active(tickets), tickets)


if __name__ == "__main__":
    unittest.main()
