from collections import defaultdict
import random
from monty_hall.agents.base import BaseAgent, Action, ActionSetup
from monty_hall.env.monty import State, StepResult, Result

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

class RLItsProbablyFine(BaseAgent):
    def __init__(self) -> None:
        super().__init__()
        self._q_table: defaultdict[State, defaultdict[str, float]] = defaultdict(
            lambda: defaultdict(float)
        )
        self.actions = [Action.CHOOSE, Action.STAY, Action.SWITCH]
        self.alpha = 0.1
        self.epsilon = 0.1
        self.last_observation: State | None = None

    def act(self, observation: State) -> ActionSetup:
        self.last_observation = observation
        if not observation.selected_door:
            return _select_random_door(observation)
        if random.random() < self.epsilon:
            action = random.choice([Action.STAY, Action.SWITCH])
            return ActionSetup(
                action_name=action,
                arguments=[],
                keyword_arguments={},
            )
        should_move = self._q_table[self.last_observation][Action.SWITCH.value]
        should_stay = self._q_table[self.last_observation][Action.STAY.value]
        if should_move > should_stay:
            return _switch_door(observation)
        return _stay_door(observation)

    def observe_step(self, step_result: StepResult) -> None:
        if not self.last_observation:
            raise ValueError("No last observation to update Q-table with.")
        action = step_result.action
        score_delta = step_result.score_delta
        old_score = self._q_table[self.last_observation][action.value]
        new_score = old_score + self.alpha * (score_delta - old_score)
        self._q_table[self.last_observation][action.value] = new_score


class RLItsProbablyFineDecayingEpsilon(RLItsProbablyFine):
    def __init__(self, initial_epsilon: float = 0.2, decay_rate: float = 0.99) -> None:
        super().__init__()
        self.epsilon = initial_epsilon
        self.initial_epsilon = initial_epsilon
        self.min_epsilon = 0.01
        self.episode = 0
        self.decay_rate = 0.999
        self.episode_count = 0

    def observe_result(self, result: Result) -> None:
        super().observe_result(result)
        self.episode_count += 1
        self.epsilon = max(self.min_epsilon, self.initial_epsilon * (self.decay_rate ** self.episode_count))


# class RLMyFavoriteDoor(BaseAgent):
#     def __init__(self) -> None:
#         super().__init__()
#         self.positive_feelings_towards_door: dict[int, float] = defaultdict(float)

# class RLMyFavoriteAction(BaseAgent):
#     def __init__(self) -> None:
#         super().__init__()
#         self.positivity_towards_action: dict[Action, float] = defaultdict(float)

# class MyFavoriteActionWithContext(BaseAgent):
#     def __init__(self) -> None:
#         super().__init__()


"""
 RL Agent Strategies for Monty Hall
1. Naive Q-Learner (Flat State)
State: Just the current number of doors, selected index, open doors

Actions: CHOOSE, STAND, SWITCH

Problem: Early versions might not realize that switching is better unless enough reward shaping or episodes are run

Lesson: Shows how RL agents can get stuck in local optima (e.g. sticking)

2. Two-Phase Agent (Learn Separately)
Phase 1: Learn which door to pick

Phase 2: Learn whether to switch

Reward: +1 for win, 0 for loss

Problem: Might mistakenly credit the initial pick for the win unless the phases are clearly split

Lesson: Shows credit assignment problem in multi-step tasks

3. Policy Gradient Agent
Learns a probability distribution over actions

Over time, it might converge toward always switching

Failure mode: If reward signal is noisy or the switching step isn’t clearly marked, it may fluctuate or never stabilize

4. Curiosity-Driven Agent
Explores novel action-state combinations regardless of reward

Might waste time opening already-known doors or exploring unhelpful switches

Lesson: Highlights when curiosity-based exploration can hurt (e.g. in simple games where strategy is subtle)

5. Belief-Based Agent (Bayesian RL style)
Tries to infer hidden state (where the prize is) using conditional probability

Could be hand-coded or learned via deep belief networks

Ideal outcome: Learns to treat Monty's reveals as informative evidence

Lesson: Captures how reasoning about unobserved state can help in structured environments

6. Meta-Learner / Recurrent Agent
Observes many Monty Hall games and learns the structure (like a human)

Uses memory (LSTM or GRU) to carry experience across episodes

Interesting: Could eventually "discover" Monty’s pattern — that he always reveals a goat

7. Wrong Reward Agent
Learns from a twisted reward function (e.g. rewarded for selecting Door 2 or penalized for switching)

Lesson: Useful for studying reward hacking and unintended optimization

🔄 Things to Try
Vary the number of doors (test generalization)

Randomize host behavior (sometimes open at random, sometimes not)

Add decoy hosts that lie

Limit memory / observation space (partially observable MDP)
"""