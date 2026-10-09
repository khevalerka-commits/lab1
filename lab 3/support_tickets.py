"""Лабораторная работа № 3, вариант 9: заявки поддержки.

Процедурная программа: очередь заявок по приоритету, статистика статусов
и контроль SLA. Все данные передаются параметрами, глобальных изменяемых
коллекций нет.
"""
from datetime import datetime, timedelta
from types import MappingProxyType

# Глобальные ТОЛЬКО неизменяемые константы (Global-область).
PRIORITY_RANK = MappingProxyType({"low": 1, "medium": 2, "high": 3, "critical": 4})
STATUSES = ("open", "in_progress", "resolved", "closed")
ACTIVE_STATUSES = ("open", "in_progress")
DEFAULT_SLA_HOURS = MappingProxyType({"critical": 4, "high": 24, "medium": 48, "low": 120})
STATUS_LABELS = MappingProxyType({
    "open": "открыта", "in_progress": "в работе",
    "resolved": "решена", "closed": "закрыта",
})


def validate_ticket(ticket):
    """Проверяет заявку и возвращает НОВЫЙ нормализованный словарь.

    Ошибки: TypeError — неверный тип данных; ValueError — недопустимое значение.
    """
    if not isinstance(ticket, dict):
        raise TypeError("Заявка должна быть словарём")
    ticket_id = ticket.get("id")
    if isinstance(ticket_id, bool) or not isinstance(ticket_id, int):
        raise TypeError("Идентификатор должен быть целым числом")
    if ticket_id <= 0:
        raise ValueError("Идентификатор должен быть положительным")
    priority = ticket.get("priority")
    if not isinstance(priority, str):
        raise TypeError("Приоритет должен быть строкой")
    if priority not in PRIORITY_RANK:
        raise ValueError(f"Неизвестный приоритет: {priority}")
    created = ticket.get("created")
    if not isinstance(created, datetime):
        raise TypeError("Время создания должно быть datetime")
    status = ticket.get("status")
    if not isinstance(status, str):
        raise TypeError("Статус должен быть строкой")
    if status not in STATUSES:
        raise ValueError(f"Неизвестный статус: {status}")
    return {"id": ticket_id, "priority": priority, "created": created, "status": status}


def priority_key(ticket):
    """Ключ сортировки: выше приоритет — раньше; при равенстве старее — раньше."""
    return (-PRIORITY_RANK[ticket["priority"]], ticket["created"])


def filter_active(tickets):
    """Возвращает новый список заявок со статусами «открыта» и «в работе»."""
    return [t for t in tickets if t["status"] in ACTIVE_STATUSES]


def build_queue(tickets):
    """Строит очередь: проверка, отбор активных, сортировка. Вход не меняется."""
    checked = [validate_ticket(t) for t in tickets]
    ids = [t["id"] for t in checked]
    if len(ids) != len(set(ids)):
        raise ValueError("Идентификаторы заявок должны быть уникальными")
    return sorted(filter_active(checked), key=priority_key)


def status_counts(tickets):
    """Возвращает словарь «статус -> количество» (нулевые статусы включены)."""
    counts = {status: 0 for status in STATUSES}
    for ticket in (validate_ticket(t) for t in tickets):
        counts[ticket["status"]] += 1
    return counts


def sla_deadline(ticket, sla_hours=DEFAULT_SLA_HOURS):
    """Крайний срок обработки = время создания + SLA приоритета (в часах)."""
    hours = sla_hours[ticket["priority"]]
    if hours <= 0:
        raise ValueError("SLA должен быть положительным")
    return ticket["created"] + timedelta(hours=hours)


def hours_left(ticket, now, sla_hours=DEFAULT_SLA_HOURS):
    """Часов до дедлайна SLA (отрицательное значение — просрочка)."""
    return (sla_deadline(ticket, sla_hours) - now).total_seconds() / 3600


def is_breached(ticket, now, sla_hours=DEFAULT_SLA_HOURS):
    """SLA нарушен, только если срок СТРОГО прошёл (на границе — не нарушен)."""
    return hours_left(ticket, now, sla_hours) < 0


def make_sla_checker(now, sla_hours=DEFAULT_SLA_HOURS):
    """Замыкание: now и sla_hours лежат в Enclosing-области внутренней функции."""
    def check(ticket):
        return is_breached(ticket, now, sla_hours)
    return check


def format_queue(queue, now, sla_hours=DEFAULT_SLA_HOURS):
    """Формирует текст очереди и НЕ печатает его."""
    if not queue:
        return "Очередь пуста"
    lines = []
    for position, ticket in enumerate(queue, start=1):
        left = hours_left(ticket, now, sla_hours)
        sla_text = f"ПРОСРОЧЕНА на {-left:.1f} ч" if left < 0 else f"до дедлайна {left:.1f} ч"
        lines.append(
            f"{position}. #{ticket['id']} [{ticket['priority']}] "
            f"{STATUS_LABELS[ticket['status']]}, создана "
            f"{ticket['created']:%Y-%m-%d %H:%M} — {sla_text}"
        )
    return "\n".join(lines)


def format_counts(counts):
    """Формирует текст статистики статусов."""
    return "\n".join(f"{STATUS_LABELS[s]}: {counts[s]}" for s in STATUSES)


def main():
    """Координирует вызовы и отвечает за вывод."""
    now = datetime(2026, 10, 9, 12, 0)
    tickets = [
        {"id": 1, "priority": "critical", "created": datetime(2026, 10, 9, 10, 0), "status": "open"},
        {"id": 2, "priority": "high", "created": datetime(2026, 10, 8, 15, 0), "status": "in_progress"},
        {"id": 3, "priority": "low", "created": datetime(2026, 10, 5, 9, 0), "status": "open"},
        {"id": 4, "priority": "medium", "created": datetime(2026, 10, 9, 8, 0), "status": "resolved"},
        {"id": 5, "priority": "critical", "created": datetime(2026, 10, 9, 6, 0), "status": "open"},
        {"id": 6, "priority": "medium", "created": datetime(2026, 10, 8, 9, 0), "status": "closed"},
        {"id": 7, "priority": "medium", "created": datetime(2026, 10, 8, 10, 0), "status": "open"},
    ]
    queue = build_queue(tickets)
    print(f"Текущее время: {now:%Y-%m-%d %H:%M}")
    print("Очередь заявок:")
    print(format_queue(queue, now))
    print("\nСтатистика статусов:")
    print(format_counts(status_counts(tickets)))
    checker = make_sla_checker(now)
    overdue = [t["id"] for t in queue if checker(t)]
    print("\nЗаявки с нарушенным SLA:", overdue)
    custom = {"critical": 2, "high": 12, "medium": 24, "low": 72}  # именованный аргумент
    print("С более жёстким SLA просрочены:",
          [t["id"] for t in queue if is_breached(t, now, sla_hours=custom)])


if __name__ == "__main__":
    main()
