from dataclasses import dataclass
from enum import Enum
import random


class ActionType(Enum):
    USER_ACTION = "user_action"
    HOST_ACTION = "host_action"


@dataclass
class Door:
    index: int
    is_open: bool = False

@dataclass
class State:
    available_doors: list[Door]
    selected_door: Door | None
    open_doors: list[Door]


class Monty:
    def __init__(self, door_count: int=3, rng: random.Random | None=None):
        self.door_count = door_count
        self.rng = rng or random.Random()
        self.selected_door: Door | None = None
        self.reset()

    def _set_winning_door(self):
        winning_index = self.rng.randint(0, self.door_count - 1)
        self.winning_door = self.doors[winning_index]

    def reset(self):
        self.winning_door = None
        self.selected_door = None
        self.doors: list[Door] =[
            Door(index=i) for i in range(self.door_count)
        ]
        self._set_winning_door()
        self.last_action: ActionType | None = None

    def select_door(self, door_index: int):
        if door_index < 0 or door_index >= self.door_count:
            raise ValueError("Invalid door index")
        if self.doors[door_index].is_open:
            raise ValueError("Cannot select an open door")
        if self.last_action == ActionType.USER_ACTION:
            raise ValueError("Cannot select a door after a user action")
        self.selected_door = self.doors[door_index]
        self.last_action = ActionType.USER_ACTION

    def host_opens_door(self):
        if not self.selected_door:
            raise ValueError("No door selected")
        if self.last_action != ActionType.USER_ACTION:
            raise ValueError("Cannot open a door after a host action")
        unopened_doors = [
            door for door in self.doors
            if not door.is_open
        ]
        if len(unopened_doors) <= 2:
            raise ValueError("Cannot open a door when only two unopened doors remain")
        selectable_doors = [
            door for door in self.doors
            if door != self.selected_door and not door.is_open and door != self.winning_door
        ]
        door_to_open = self.rng.choice(selectable_doors)
        door_to_open.is_open = True
        self.last_action = ActionType.HOST_ACTION

    def has_won(self) -> bool:
        if not self.selected_door:
            raise ValueError("No door selected")
        if not self.last_action == ActionType.USER_ACTION:
            return False
        count_closed_doors = sum(not door.is_open for door in self.doors)
        if count_closed_doors > 2:
            raise ValueError("Cannot check win state when more than two doors are closed")
        return self.selected_door == self.winning_door

    def done(self) -> bool:
        two_doors_left = sum(not door.is_open for door in self.doors) == 2
        user_acted_last = self.last_action == ActionType.USER_ACTION
        return two_doors_left and user_acted_last

    def switch_door(self):
        if not self.selected_door:
            raise ValueError("No door selected")
        unopened_doors = [
            door for door in self.doors
            if not door.is_open and door != self.selected_door
        ]
        if len(unopened_doors) != 1:
            raise ValueError("Cannot switch doors when more than one unopened door remains")
        self.selected_door = unopened_doors[0]
        self.last_action = ActionType.USER_ACTION

    def stand(self):
        if not self.selected_door:
            raise ValueError("No door selected")
        if self.last_action == ActionType.USER_ACTION:
            raise ValueError("Cannot stand after a user action")
        self.last_action = ActionType.USER_ACTION

    def get_state(self) -> State:
        available_doors = [
            door for door in self.doors if not door.is_open
        ]
        open_doors = [
            door for door in self.doors if door.is_open
        ]
        return State(
            available_doors=available_doors,
            selected_door=self.selected_door,
            open_doors=open_doors
        )