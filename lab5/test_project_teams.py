import unittest

from project_teams import ProjectTeam, TeamMember


def make_team(size=4, count=0):
    team = ProjectTeam("Alpha", size)
    for number in range(1, count + 1):
        team.add_member(TeamMember(number, f"User{number}"))
    return team


class TeamMemberTests(unittest.TestCase):
    def test_valid_member_trims_name(self):
        member = TeamMember(1, "  Amina ")
        self.assertEqual((member.member_id, member.name), (1, "Amina"))

    def test_invalid_id_type_and_value(self):
        for bad in (True, "1", 1.5):
            with self.assertRaises(TypeError):
                TeamMember(bad, "A")
        for bad in (0, -3):
            with self.assertRaises(ValueError):
                TeamMember(bad, "A")

    def test_empty_name(self):
        for bad in ("", "   ", None):
            with self.assertRaises(ValueError):
                TeamMember(1, bad)

    def test_equality_by_id_and_readonly(self):
        self.assertEqual(TeamMember(1, "A"), TeamMember(1, "B"))
        member = TeamMember(1, "A")
        with self.assertRaises(AttributeError):
            member.name = "X"


class ProjectTeamTests(unittest.TestCase):
    def test_add_and_snapshot(self):
        team = make_team(count=2)
        self.assertEqual(team.size, 2)
        self.assertEqual(team.free_slots, 2)
        snapshot = team.members
        self.assertIsInstance(snapshot, tuple)
        self.assertEqual([m.member_id for m in snapshot], [1, 2])

    def test_duplicate_member_rejected_state_kept(self):         # ошибочный сценарий 1
        team = make_team(count=2)
        with self.assertRaises(ValueError):
            team.add_member(TeamMember(1, "Copy"))
        self.assertEqual(team.size, 2)

    def test_team_limit_boundary(self):                          # граничный сценарий
        team = make_team(size=3, count=3)
        self.assertEqual(team.free_slots, 0)
        with self.assertRaises(ValueError):
            team.add_member(TeamMember(4, "Extra"))
        self.assertEqual(team.size, 3)

    def test_add_wrong_type(self):                               # ошибочный сценарий 2
        with self.assertRaises(TypeError):
            make_team().add_member({"id": 1})

    def test_assign_unknown_member(self):                        # ошибочный сценарий 3
        with self.assertRaises(KeyError):
            make_team(count=1).assign_role(99, "developer")

    def test_invalid_role(self):
        team = make_team(count=1)
        with self.assertRaises(ValueError):
            team.assign_role(1, "manager")
        with self.assertRaises(TypeError):
            team.assign_role(1, 5)
        self.assertIsNone(team.role_of(1))

    def test_only_one_leader(self):
        team = make_team(count=2)
        team.assign_role(1, "leader")
        with self.assertRaises(ValueError):
            team.assign_role(2, "leader")
        team.assign_role(1, "leader")                      # повтор для того же участника допустим
        team.assign_role(1, "developer")                   # лидер освободил роль
        team.assign_role(2, "leader")
        self.assertEqual(team.role_of(2), "leader")

    def test_roles_distribution_is_copy(self):
        team = make_team(count=3)
        team.assign_role(1, "leader")
        team.assign_role(2, "developer")
        team.assign_role(3, "developer")
        distribution = team.roles_distribution
        self.assertEqual(distribution, {"leader": ("User1",), "developer": ("User2", "User3")})
        distribution["leader"] = ("Hacker",)
        distribution["tester"] = ("X",)
        self.assertEqual(team.roles_distribution["leader"], ("User1",))
        self.assertNotIn("tester", team.roles_distribution)

    def test_unassigned_and_missing_roles(self):
        team = make_team(count=3)
        self.assertEqual(team.missing_roles, ("leader", "developer"))
        team.assign_role(1, "leader")
        self.assertEqual(team.missing_roles, ("developer",))
        self.assertEqual([m.member_id for m in team.unassigned], [2, 3])
        team.assign_role(2, "developer")
        self.assertTrue(team.is_ready)

    def test_confirm_requires_leader_and_developer(self):
        team = make_team(count=2)
        team.assign_role(1, "leader")
        with self.assertRaises(ValueError):
            team.confirm()
        self.assertFalse(team.is_confirmed)
        team.assign_role(2, "developer")
        team.confirm()
        self.assertTrue(team.is_confirmed)

    def test_confirmed_team_is_closed(self):
        team = make_team(count=2)
        team.assign_role(1, "leader")
        team.assign_role(2, "developer")
        team.confirm()
        with self.assertRaises(ValueError):
            team.add_member(TeamMember(3, "Late"))
        with self.assertRaises(ValueError):
            team.assign_role(2, "tester")
        self.assertEqual(team.role_of(2), "developer")

    def test_invalid_team_parameters(self):
        with self.assertRaises(ValueError):
            ProjectTeam("  ", 3)
        with self.assertRaises(ValueError):
            ProjectTeam("A", 1)               # меньше числа обязательных ролей
        with self.assertRaises(TypeError):
            ProjectTeam("A", "3")

    def test_summary_returns_text_and_repr_hides_internals(self):
        team = make_team(count=1)
        self.assertIn("User1: без роли", team.summary())
        self.assertNotIn("_roles", repr(team))
        self.assertNotIn("_members", repr(team))

    def test_instances_do_not_share_state(self):
        first, second = make_team(count=1), make_team(count=0)
        self.assertEqual(second.size, 0)
        self.assertEqual(first.size, 1)


if __name__ == "__main__":
    unittest.main()
