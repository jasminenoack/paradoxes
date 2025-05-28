import random
from monty_hall.agents.base import BaseAgent, Action, ActionSetup
from monty_hall.env.monty import State


def _select_random_door(observation: State) -> ActionSetup:
    return ActionSetup(
                action_name=Action.CHOOSE,
                arguments=[random.choice(range(len(observation.available_doors)))],
                keyword_arguments={},
            )

def _switch_door(observation: State) -> ActionSetup:
    return ActionSetup(
        action_name=Action.SWITCH,
        arguments=[],
        keyword_arguments={},
    )

def _stay_door(observation: State) -> ActionSetup:
    return ActionSetup(
        action_name=Action.STAY,
        arguments=[],
        keyword_arguments={},
    )


class Stander(BaseAgent):
    def act(self, observation: State) -> ActionSetup:
        if not observation.selected_door:
            return _select_random_door(observation)
        return _stay_door(observation)

class Switcher(BaseAgent):
    def act(self, observation: State) -> ActionSetup:
        if not observation.selected_door:
            return _select_random_door(observation)
        return _switch_door(observation)


class Random(BaseAgent):
    def act(self, observation: State) -> ActionSetup:
        if not observation.selected_door:
            return _select_random_door(observation)
        if random.random() < 0.5:
            return _stay_door(observation)
        return _switch_door(observation)


class Door2(BaseAgent):
    def act(self, observation: State) -> ActionSetup:
        """
        Always choose door 2.
        """
        return ActionSetup(
            action_name=Action.CHOOSE,
            arguments=[2],
            keyword_arguments={},
        )