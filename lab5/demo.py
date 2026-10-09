"""Демонстрационный запуск: python demo.py"""
from project_teams import ProjectTeam, TeamMember


def try_action(title, action):
    """Выполняет действие и печатает результат или сообщение об ошибке."""
    try:
        action()
        print(f"[OK]     {title}")
    except (TypeError, ValueError, KeyError) as error:
        print(f"[ОШИБКА] {title}: {error.args[0]}")


def main():
    team = ProjectTeam("Alpha", max_size=4)
    amina, dias = TeamMember(1, "Amina"), TeamMember(2, "Dias")
    mira, timur, aigul = TeamMember(3, "Mira"), TeamMember(4, "Timur"), TeamMember(5, "Aigul")

    for member in (amina, dias, mira, timur):
        team.add_member(member)
    print(f"Участников: {team.size}, свободных мест: {team.free_slots}")
    try_action("добавить Amina повторно", lambda: team.add_member(amina))
    try_action("добавить пятого (Aigul)", lambda: team.add_member(aigul))

    team.assign_role(1, "leader")
    team.assign_role(2, "developer")
    try_action("второй лидер (Mira)", lambda: team.assign_role(3, "leader"))
    try_action("роль «manager»", lambda: team.assign_role(3, "manager"))
    try_action("неизвестный участник 99", lambda: team.assign_role(99, "tester"))
    team.assign_role(3, "designer")

    print()
    print(team.summary())
    print("Распределение ролей:", team.roles_distribution)
    print("Без роли:", [m.name for m in team.unassigned])

    # обязательные роли: лидер и разработчик
    other = ProjectTeam("Beta", max_size=3)
    other.add_member(TeamMember(10, "Ruslan"))
    other.assign_role(10, "leader")
    print()
    print("Beta, не хватает ролей:", other.missing_roles)
    try_action("подтвердить Beta без разработчика", other.confirm)
    other.add_member(TeamMember(11, "Zhanna"))
    other.assign_role(11, "developer")
    try_action("подтвердить Beta после назначения", other.confirm)
    try_action("добавить участника в подтверждённую Beta",
               lambda: other.add_member(TeamMember(12, "Nurlan")))
    print()
    print(other.summary())


if __name__ == "__main__":
    main()
