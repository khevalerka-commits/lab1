"""Объектная модель проектных команд (лабораторная работа № 5, вариант 9).

TeamMember — участник (неизменяемая идентичность: id и имя).
ProjectTeam — команда ограниченного размера: состав, роли, обязательные роли.
"""


class TeamMember:
    """Участник проектной команды с неизменяемыми идентификатором и именем."""

    def __init__(self, member_id, name):
        if isinstance(member_id, bool) or not isinstance(member_id, int):
            raise TypeError("Идентификатор должен быть целым числом")
        if member_id <= 0:
            raise ValueError("Идентификатор должен быть положительным")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Имя не должно быть пустым")
        self._member_id = member_id
        self._name = name.strip()

    @property
    def member_id(self):
        """Идентификатор участника (только чтение)."""
        return self._member_id

    @property
    def name(self):
        """Имя участника (только чтение)."""
        return self._name

    def __eq__(self, other):
        if not isinstance(other, TeamMember):
            return NotImplemented
        return self._member_id == other._member_id

    def __hash__(self):
        return hash(self._member_id)

    def __repr__(self):
        return f"TeamMember(member_id={self._member_id!r}, name={self._name!r})"


class ProjectTeam:
    """Проектная команда: ограниченный состав, роли и обязательные роли.

    Инварианты:
      * участники уникальны, их число не больше max_size;
      * у участника не более одной роли, роль входит в ROLES;
      * роль лидера у команды не более чем у одного участника;
      * подтверждённая команда содержит всех участников обязательных ролей
        и закрыта для изменений.
    """

    ROLES = ("leader", "developer", "designer", "tester", "analyst")
    REQUIRED_ROLES = ("leader", "developer")

    def __init__(self, name, max_size):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Название команды не должно быть пустым")
        if isinstance(max_size, bool) or not isinstance(max_size, int):
            raise TypeError("Размер команды должен быть целым числом")
        if max_size < len(self.REQUIRED_ROLES):
            raise ValueError(
                f"Размер команды должен быть не меньше {len(self.REQUIRED_ROLES)}"
            )
        self._name = name.strip()
        self._max_size = max_size
        self._members = {}      # member_id -> TeamMember (экземплярный атрибут)
        self._roles = {}        # member_id -> роль
        self._confirmed = False

    # ---------- запросы ----------
    @property
    def name(self):
        """Название команды."""
        return self._name

    @property
    def max_size(self):
        """Максимальное число участников."""
        return self._max_size

    @property
    def size(self):
        """Текущее число участников."""
        return len(self._members)

    @property
    def free_slots(self):
        """Число свободных мест."""
        return self._max_size - len(self._members)

    @property
    def is_confirmed(self):
        """True, если команда подтверждена."""
        return self._confirmed

    @property
    def members(self):
        """Неизменяемый снимок состава (в порядке добавления)."""
        return tuple(self._members.values())

    def role_of(self, member_id):
        """Возвращает роль участника или None, если роль не назначена."""
        self._require_member(member_id)
        return self._roles.get(member_id)

    @property
    def roles_distribution(self):
        """Копия распределения: роль -> кортеж имён (только занятые роли)."""
        distribution = {}
        for role in self.ROLES:
            names = tuple(
                self._members[mid].name
                for mid, assigned in self._roles.items() if assigned == role
            )
            if names:
                distribution[role] = names
        return distribution

    @property
    def unassigned(self):
        """Кортеж участников без роли."""
        return tuple(m for mid, m in self._members.items() if mid not in self._roles)

    @property
    def missing_roles(self):
        """Кортеж обязательных ролей, которые ещё никому не назначены."""
        assigned = set(self._roles.values())
        return tuple(role for role in self.REQUIRED_ROLES if role not in assigned)

    @property
    def is_ready(self):
        """True, если все обязательные роли назначены."""
        return not self.missing_roles

    def summary(self):
        """Возвращает текст состава и ролей (не печатает)."""
        state = "подтверждена" if self._confirmed else "не подтверждена"
        lines = [f"Команда «{self._name}» ({self.size}/{self._max_size}, {state})"]
        for member in self._members.values():
            lines.append(f"  - {member.name}: {self._roles.get(member.member_id, 'без роли')}")
        if self.missing_roles:
            lines.append("  Не хватает ролей: " + ", ".join(self.missing_roles))
        return "\n".join(lines)

    # ---------- команды ----------
    def add_member(self, member):
        """Добавляет участника; проверки выполняются до изменения состояния."""
        self._require_open()
        if not isinstance(member, TeamMember):
            raise TypeError("Ожидается объект TeamMember")
        if member.member_id in self._members:
            raise ValueError("Участник уже в команде")
        if len(self._members) >= self._max_size:
            raise ValueError("Команда заполнена")
        self._members[member.member_id] = member

    def assign_role(self, member_id, role):
        """Назначает участнику роль (заменяет прежнюю); лидер — только один."""
        self._require_open()
        self._require_member(member_id)
        if not isinstance(role, str):
            raise TypeError("Роль должна быть строкой")
        if role not in self.ROLES:
            raise ValueError(f"Неизвестная роль: {role}")
        if role == "leader":
            current = [mid for mid, r in self._roles.items() if r == "leader"]
            if current and current[0] != member_id:
                raise ValueError("Лидер уже назначен")
        self._roles[member_id] = role

    def confirm(self):
        """Подтверждает команду, если назначены все обязательные роли."""
        self._require_open()
        if self.missing_roles:
            raise ValueError("Не назначены роли: " + ", ".join(self.missing_roles))
        self._confirmed = True

    # ---------- внутренние детали ----------
    def _require_member(self, member_id):
        if member_id not in self._members:
            raise KeyError("Участник не найден")

    def _require_open(self):
        if self._confirmed:
            raise ValueError("Команда подтверждена и закрыта для изменений")

    def __repr__(self):
        return f"ProjectTeam(name={self._name!r}, max_size={self._max_size!r})"
