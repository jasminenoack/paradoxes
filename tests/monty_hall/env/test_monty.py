import random
from monty_hall.env.monty import Monty, ActionType, State, StepResult, Result, Action

class TestInit:
    def test_creates_doors(self):
        rng = random.Random(42)
        monty = Monty(rng=rng)
        assert len(monty.doors) == 3
        assert monty.winning_door == monty.doors[2]
        assert all(not door.is_open for door in monty.doors)

    def test_creates_doors_with_custom_count(self):
        rng = random.Random(42)
        monty = Monty(door_count=5, rng=rng)
        assert len(monty.doors) == 5
        assert monty.winning_door == monty.doors[0]


class TestReset:
    def test_reset_resets_game_state(self):
        rng = random.Random(42)
        monty = Monty(rng=rng)
        original_doors = monty.doors.copy()
        original_winning_door = monty.winning_door
        monty.doors[0].is_open = True
        monty.selected_door = monty.doors[1]
        assert monty.winning_door == monty.doors[2]
        monty.last_action = ActionType.USER_ACTION
        monty.reset()

        assert monty.doors != original_doors
        assert monty.winning_door != original_winning_door
        assert monty.selected_door is None
        assert all(not door.is_open for door in monty.doors)
        assert monty.last_action is None

class TestSelectDoor:
    def test_selects_door(self):
        rng = random.Random(42)
        monty = Monty(rng=rng)
        result = monty.select_door(1)
        assert monty.selected_door
        assert monty.selected_door == monty.doors[1]
        assert not monty.selected_door.is_open
        assert monty.last_action == ActionType.USER_ACTION
        assert result == StepResult(
            action=Action.CHOOSE,
            score_delta=0
        )

    def test_selects_door_twice(self):
        rng = random.Random(42)
        monty = Monty(rng=rng)
        monty.select_door(1)
        monty.host_opens_door()
        monty.select_door(2)
        assert monty.selected_door
        assert monty.selected_door == monty.doors[2]
        assert not monty.selected_door.is_open

    def test_cannot_select_open_door(self):
        rng = random.Random(42)
        monty = Monty(rng=rng)
        monty.doors[1].is_open = True
        try:
            monty.select_door(1)
        except ValueError as e:
            assert str(e) == "Cannot select an open door"
        else:
            assert False, "Expected ValueError not raised"

    def test_cannot_select_invalid_door(self):
        rng = random.Random(42)
        monty = Monty(rng=rng)
        try:
            monty.select_door(3)
        except ValueError as e:
            assert str(e) == "Invalid door index"
        else:
            assert False, "Expected ValueError not raised"

    def test_fails_if_last_action_was_not_host_action(self):
        rng = random.Random(42)
        monty = Monty(rng=rng)
        monty.last_action = ActionType.USER_ACTION
        try:
            monty.select_door(1)
        except ValueError as e:
            assert str(e) == "Cannot select a door after a user action"
        else:
            assert False, "Expected ValueError not raised"


class TestHostOpensDoor:
    def test_opens_door(self):
        rng = random.Random(42)
        monty = Monty(rng=rng)
        monty.select_door(1)
        monty.host_opens_door()
        assert monty.doors[0].is_open
        assert not monty.doors[1].is_open
        assert not monty.doors[2].is_open
        assert monty.last_action == ActionType.HOST_ACTION

    def test_cannot_open_last_door(self):
        rng = random.Random(42)
        monty = Monty(rng=rng)
        monty.select_door(1)
        monty.host_opens_door()
        monty.select_door(2)
        try:
            monty.host_opens_door()
        except ValueError as e:
            assert str(e) == "Cannot open a door when only two unopened doors remain"
        else:
            assert False, "Expected ValueError not raised"

    def test_can_open_more_than_one_door_if_multiple_doors(self):
        rng = random.Random(42)
        monty = Monty(door_count=4, rng=rng)
        monty.select_door(1)
        monty.host_opens_door()
        assert sum(door.is_open for door in monty.doors) == 1
        assert not monty.doors[0].is_open
        assert not monty.doors[1].is_open
        assert monty.doors[2].is_open
        assert not monty.doors[3].is_open


        monty.select_door(1)
        monty.host_opens_door()
        assert sum(door.is_open for door in monty.doors) == 2
        assert not monty.doors[0].is_open
        assert not monty.doors[1].is_open
        assert monty.doors[2].is_open
        assert monty.doors[3].is_open

    def test_will_not_open_same_door_twice(self):
        rng = random.Random(42)
        monty = Monty(rng=rng, door_count=10)
        monty.selected_door = monty.doors[1]
        monty.winning_door = monty.doors[0]
        monty.select_door(1)
        monty.host_opens_door()
        assert sum(door.is_open for door in monty.doors) == 1
        monty.select_door(1)
        monty.host_opens_door()
        assert sum(door.is_open for door in monty.doors) == 2
        monty.select_door(1)
        monty.host_opens_door()
        assert sum(door.is_open for door in monty.doors) == 3
        monty.select_door(1)
        monty.host_opens_door()
        assert sum(door.is_open for door in monty.doors) == 4
        monty.select_door(1)
        monty.host_opens_door()
        assert sum(door.is_open for door in monty.doors) == 5
        monty.select_door(1)
        monty.host_opens_door()
        assert sum(door.is_open for door in monty.doors) == 6
        monty.select_door(1)
        monty.host_opens_door()
        assert sum(door.is_open for door in monty.doors) == 7
        monty.select_door(1)
        monty.host_opens_door()
        assert sum(door.is_open for door in monty.doors) == 8
        assert monty.selected_door
        assert not monty.selected_door.is_open
        assert not monty.winning_door.is_open

    def test_cannot_open_door_if_none_selected(self):
        rng = random.Random(42)
        monty = Monty(rng=rng)
        try:
            monty.host_opens_door()
        except ValueError as e:
            assert str(e) == "No door selected"
        else:
            assert False, "Expected ValueError not raised"

    def test_fails_if_last_action_was_not_user_action(self):
        rng = random.Random(42)
        monty = Monty(rng=rng)
        monty.select_door(1)
        monty.last_action = ActionType.HOST_ACTION
        try:
            monty.host_opens_door()
        except ValueError as e:
            assert str(e) == "Cannot open a door after a host action"
        else:
            assert False, "Expected ValueError not raised"

class TestCheckHasWon:
    def test_fails_if_more_than_two_doors_closed(self):
        rng = random.Random(42)
        monty = Monty(rng=rng, door_count=4)
        monty.select_door(1)
        monty.host_opens_door()
        monty.select_door(1)
        try:
            monty.has_won()
        except ValueError as e:
            assert str(e) == "Cannot check win state when more than two doors are closed"
        else:
            assert False, "Expected ValueError not raised"

    def test_not_won_if_selected_door_not_winning(self):
        rng = random.Random(42)
        monty = Monty(rng=rng)
        monty.select_door(0)
        monty.host_opens_door()
        assert not monty.has_won()

    def test_won_if_selected_door_is_winning(self):
        rng = random.Random(42)
        monty = Monty(rng=rng)
        monty.select_door(2)
        monty.host_opens_door()
        monty.select_door(2)
        assert monty.has_won()

    def test_fails_if_no_door_selected(self):
        rng = random.Random(42)
        monty = Monty(rng=rng)
        try:
            monty.has_won()
        except ValueError as e:
            assert str(e) == "No door selected"
        else:
            assert False, "Expected ValueError not raised"

    def test_has_not_won_if_last_action_was_host_action(self):
        rng = random.Random(42)
        monty = Monty(rng=rng)
        monty.select_door(1)
        monty.host_opens_door()
        monty.select_door(2)
        monty.last_action = ActionType.HOST_ACTION
        assert not monty.has_won()

class TestDone:
    def test_done_if_two_doors_and_lost(self):
        rng = random.Random(42)
        monty = Monty(rng=rng)
        monty.select_door(0)
        monty.host_opens_door()
        monty.select_door(0)
        assert not monty.has_won()
        assert monty.done()

    def test_done_if_two_doors_and_won(self):
        rng = random.Random(42)
        monty = Monty(rng=rng)
        monty.select_door(2)
        monty.host_opens_door()
        monty.select_door(2)
        assert monty.has_won()
        assert monty.done()

    def test_not_done_if_has_not_acted(self):
        rng = random.Random(42)
        monty = Monty(rng=rng)
        monty.select_door(0)
        monty.host_opens_door()
        assert not monty.done()

    def test_not_done_unless_last_action_was_user_action(self):
        rng = random.Random(42)
        monty = Monty(rng=rng)
        monty.select_door(0)
        monty.host_opens_door()
        monty.last_action = ActionType.HOST_ACTION
        assert not monty.done()

    def test_done_if_last_action_was_user_action(self):
        rng = random.Random(42)
        monty = Monty(rng=rng)
        monty.select_door(0)
        monty.host_opens_door()
        monty.last_action = ActionType.USER_ACTION
        assert monty.done()

class SwitchDoor:
    def test_swaps_to_a_random_door(self):
        rng = random.Random(42)
        monty = Monty(rng=rng)
        monty.select_door(0)
        monty.host_opens_door()
        original_selected_door = monty.selected_door
        result = monty.switch_door()
        assert monty.selected_door != original_selected_door
        assert monty.selected_door
        assert not monty.selected_door.is_open
        assert monty.last_action == ActionType.USER_ACTION
        assert result == StepResult(
            action=Action.SWITCH,
            score_delta=100
        )

    def test_fails_if_no_door_selected(self):
        rng = random.Random(42)
        monty = Monty(rng=rng)
        try:
            monty.switch_door()
        except ValueError as e:
            assert str(e) == "No door selected"
        else:
            assert False, "Expected ValueError not raised"

class TestStand:
    def test_stands_on_current_door(self):
        rng = random.Random(42)
        monty = Monty(rng=rng)
        monty.select_door(0)
        monty.host_opens_door()
        original_selected_door = monty.selected_door
        result = monty.stand()
        assert monty.selected_door == original_selected_door
        assert monty.last_action == ActionType.USER_ACTION
        assert result == StepResult(
            action=Action.STAY,
            score_delta=0
        )

    def test_fails_if_no_door_selected(self):
        rng = random.Random(42)
        monty = Monty(rng=rng)
        try:
            monty.stand()
        except ValueError as e:
            assert str(e) == "No door selected"
        else:
            assert False, "Expected ValueError not raised"


class TestGetState:
    def test_returns_initial_state(self):
        rng = random.Random(42)
        monty = Monty(rng=rng)
        state = monty.get_state()
        assert state == State(
            available_doors=tuple(monty.doors),
            selected_door=None,
            open_doors=()
        )

    def test_returns_state_after_selecting_door(self):
        rng = random.Random(42)
        monty = Monty(rng=rng)
        monty.select_door(0)
        state = monty.get_state()
        assert state == State(
            available_doors=tuple(monty.doors),
            selected_door=monty.selected_door,
            open_doors=()
        )

    def test_returns_state_after_host_opens_door(self):
        rng = random.Random(42)
        monty = Monty(rng=rng)
        monty.select_door(2)
        monty.host_opens_door()
        state = monty.get_state()
        assert state == State(
            available_doors=(monty.doors[1], monty.doors[2]),
            selected_door=monty.selected_door,
            open_doors=(monty.doors[0], )
        )

class TestGetResult:
    def test_returns_result_after_game(self):
        rng = random.Random(42)
        monty = Monty(rng=rng)
        monty.select_door(2)
        monty.host_opens_door()
        monty.select_door(2)
        result = monty.get_result()
        assert result == Result(
            won=True,
            score=100
        )

    def test_returns_result_after_losing_game(self):
        rng = random.Random(42)
        monty = Monty(rng=rng)
        monty.select_door(0)
        monty.host_opens_door()
        monty.select_door(0)
        result = monty.get_result()
        assert result == Result(
            won=False
        )

    def test_fails_if_game_not_done(self):
        rng = random.Random(42)
        monty = Monty(rng=rng)
        try:
            monty.get_result()
        except ValueError as e:
            assert str(e) == "Game not done"
        else:
            assert False, "Expected ValueError not raised"