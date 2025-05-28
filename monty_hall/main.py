from dataclasses import dataclass
from monty_hall.agents.non_ai_agents import Stander, Switcher, Random, Door2
from monty_hall.env.monty import Monty, State
from monty_hall.agents.base import BaseAgent, Action
import matplotlib.pyplot as plt

def _act(env: Monty, agent: BaseAgent, observation: State):
    observation = env.get_state()
    action_setup = agent.act(observation)
    if action_setup. action_name == Action.STAY:
        env.stand()
    elif action_setup.action_name == Action.SWITCH:
        env.switch_door()
    elif action_setup.action_name == Action.CHOOSE:
        env.select_door(action_setup.arguments[0])

@dataclass
class Result:
    won: bool

def run_simulation(env: Monty, agent: BaseAgent):
    env.reset()
    agent.reset()
    _act(env, agent, env.get_state())

    while not env.done():
        env.host_opens_door()
        _act(env, agent, env.get_state())
    return Result(won=env.has_won())

def repeat_simulation(env: Monty, agent: BaseAgent, n: int):
    results: list[Result] = []
    for _ in range(n):
        result = run_simulation(env, agent)
        results.append(result)
    return results

def report_results(results: list[Result], agent_name: str) -> float:
    total = len(results)
    won = sum(1 for result in results if result.won)
    print(f"{agent_name}: Total games: {total}, Wins: {won}, Win Rate: {won / total:.2%}")
    return won / total * 100


def plot_results(results: dict[str, float]):
    labels = list(results.keys())
    percentages = list(results.values())

    plt.bar(labels, percentages)  # type: ignore
    plt.ylabel('Win Rate (%)')  # type: ignore
    plt.title('Monty Hall Simulation Results')  # type: ignore
    plt.ylim(0, 100)  # type: ignore
    plt.show()  # type: ignore

if __name__ == "__main__":
    print("This is the main module for the Monty Hall problem simulation.")

    total_games = 1000
    agent_classes = [
        Stander,
        Switcher,
        Random,
        Door2,
    ]

    env = Monty()

    results_summary: dict[str, float] = {}

    for agent_class in agent_classes:
        agent = agent_class()
        results = repeat_simulation(env, agent, total_games)
        win_rate = report_results(results, agent_class.__name__)
        results_summary[agent_class.__name__] = win_rate

    plot_results(results_summary)