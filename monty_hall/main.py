from datetime import datetime
from monty_hall.agents import non_ai_agents
from monty_hall.agents import reinforcement_agents
from monty_hall.env.monty import Monty, State, Result, StepResult
from monty_hall.agents.base import BaseAgent, Action
import matplotlib.pyplot as plt

def _act(env: Monty, agent: BaseAgent, observation: State) -> StepResult:
    observation = env.get_state()
    action_setup = agent.act(observation)
    if action_setup. action_name == Action.STAY:
        return env.stand()
    elif action_setup.action_name == Action.SWITCH:
        return env.switch_door()
    elif action_setup.action_name == Action.CHOOSE:
        return env.select_door(action_setup.arguments[0])
    else:
        raise ValueError(f"Unknown action: {action_setup.action_name}")



def run_simulation(env: Monty, agent: BaseAgent) -> Result:
    env.reset()
    agent.reset()
    _act(env, agent, env.get_state())

    while not env.done():
        env.host_opens_door()
        step_result = _act(env, agent, env.get_state())
        agent.observe_step(step_result)
    result = Result(won=env.has_won())
    agent.observe_result(result)
    return result

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

def write_results_md(results_summary: dict[str, float], total_games: int | str, filename: str = "monty_hall/results.md", reset_file: bool = True, door_count: int = 3, prepend: str = ""):
    if reset_file:
        open_type = "w"
    else:
        open_type = "a"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ascii_chart = generate_ascii_bar_chart(results_summary)
    lines = [
        f"# Monty Hall Simulation Results",
        prepend,
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


def compare_agents(env: Monty, agent_classes: list[type[BaseAgent]], total_games: int, doors: int = 3):
    results_summary: dict[str, float] = {}
    for agent_class in agent_classes:
        agent = agent_class()
        results = repeat_simulation(env, agent, total_games)
        win_rate = report_results(results, agent_class.__name__)
        results_summary[agent_class.__name__] = win_rate

    reset_file = True
    write_results_md(results_summary, total_games, reset_file=reset_file, door_count=doors)
    return results_summary


def compare_accuracy_based_on_game_count(env: Monty, agent_classes: list[type[BaseAgent]], game_counts: list[int], doors: int = 3):
    for agent_class in agent_classes:
        summary_accuracy_over_game_count: dict[str, float] = {}
        for total_games in game_counts:
            agent = agent_class()
            results = repeat_simulation(env, agent, total_games)
            win_rate = report_results(results, agent_class.__name__)
            summary_accuracy_over_game_count[str(total_games)] = win_rate
        print(f"Agent: {agent_class.__name__}")
        reset_file = agent_class == agent_classes[0]
        write_results_md(summary_accuracy_over_game_count, "various", reset_file=reset_file, door_count=doors, prepend=f"## {agent_class.__name__} -")


if __name__ == "__main__":
    game_counts = list(range(200, 5000, 200))
    doors = 3
    agent_classes: list[type[BaseAgent]] = [
        non_ai_agents.Stander,
        # non_ai_agents.FirstSwitcher,
        # non_ai_agents.AlwaysSwitch,
        non_ai_agents.SmartSwitcher,
        non_ai_agents.Random,
        # Door2,
        reinforcement_agents.RLItsProbablyFine,
        reinforcement_agents.RLItsProbablyFineDecayingEpsilon,
    ]
    env = Monty(door_count=doors)

    # compare_agents(env, agent_classes, total_games=1000, doors=doors)
    compare_accuracy_based_on_game_count(env, agent_classes, game_counts, doors=doors)





    # results_summary: dict[str, float] = {}
    # results_summary_over_diff: dict[str, list[float]] = {agent_class.__name__: [] for agent_class in agent_classes}

    # for total_games in game_counts:
    #     for agent_class in agent_classes:
    #         agent = agent_class()
    #         results = repeat_simulation(env, agent, total_games)
    #         win_rate = report_results(results, agent_class.__name__)
    #         results_summary[agent_class.__name__] = win_rate
    #         results_summary_over_diff[agent_class.__name__].append(win_rate)

    #     chart = generate_ascii_bar_chart(results_summary)
    #     reset_file = total_games == game_counts[0]
    #     write_results_md(results_summary, total_games, reset_file=reset_file, door_count=doors)

