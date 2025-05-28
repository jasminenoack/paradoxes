from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from monty_hall.env.monty import State

class Action(Enum):
    STAY = "stay"
    SWITCH = "switch"
    CHOOSE = "select"


@dataclass
class ActionSetup:
    action_name: Action
    arguments: list[Any] = field(default_factory=list) # type: ignore
    keyword_arguments: dict[str, Any] = field(default_factory=dict)  # type: ignore

class BaseAgent(ABC):
    @abstractmethod
    def act(self, observation: State) -> ActionSetup:
        ...

    def reset(self) -> None:
        """
        Reset the agent's internal state if necessary.
        This method can be overridden by subclasses if they maintain state.
        """
        pass