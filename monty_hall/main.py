from dataclasses import dataclass
from datetime import datetime
from monty_hall.agents.non_ai_agents import Stander, AlwaysSwitch, SmartSwitcher, Random, Door2, FirstSwitcher
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

def generate_ascii_bar_chart(results: dict[str, float]) -> str:
    lines: list[str] = []
    max_label_len = max(len(label) for label in results)
    for label, value in results.items():
        bar = '█' * int(value // 2)  # Scale: 50 chars = 100%
        lines.append(f"{label.ljust(max_label_len)} | {bar} {value:.1f}%")
    return '\n'.join(lines)

def write_results_md(results_summary: dict[str, float], total_games: int, filename: str = "monty_hall/results.md", reset_file: bool = True, door_count: int = 3):
    if reset_file:
        open_type = "w"
    else:
        open_type = "a"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ascii_chart = generate_ascii_bar_chart(results_summary)
    lines = [
        f"# Monty Hall Simulation Results",
        f"**Date:** {timestamp}",
        f"**Doors:** {door_count}",
        f"**Total Games per Agent:** {total_games}",
        "",
        "## Win Rates",
        "",
        "```\n" + ascii_chart + "\n```",
        ""
    ]
    with open(filename, open_type) as f:
        f.write('\n'.join(lines))

if __name__ == "__main__":
    total_games = 1000
    doors = 3
    agent_classes = [
        Stander,
        FirstSwitcher,
        AlwaysSwitch,
        SmartSwitcher,
        Random,
        Door2,
    ]

    env = Monty(door_count=doors)

    results_summary: dict[str, float] = {}

    for agent_class in agent_classes:
        agent = agent_class()
        results = repeat_simulation(env, agent, total_games)
        win_rate = report_results(results, agent_class.__name__)
        results_summary[agent_class.__name__] = win_rate

    chart = generate_ascii_bar_chart(results_summary)
    write_results_md(results_summary, total_games, reset_file=True, door_count=doors)