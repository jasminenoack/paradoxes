from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from monty_hall.env.monty import State, StepResult, Result, Action
from typing import Any

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

    def observe_result(self, result: Result) -> None:
        """
        Observe the result of the action taken by the agent.
        This method can be overridden by subclasses to handle results.
        """
        pass

    def observe_step(self, step_result: StepResult) -> None:
        """
        Observe the step taken by the agent.
        This method can be overridden by subclasses to handle observations.
        """
        pass