# Monty Hall problem

For whatever reason, the Monty Hall problem is one of my favorite paradoxes.
Maybe it was that one MythBusters episode.
Maybe it's the core math. I mean, I don't like MATH, but I like math.
And this gives us a very lovely example of that distinction.

The Monty Hall problem is based on a game show. Here's how it goes:

* You're shown 3 doors.
* You pick one.
* The host opens a different door, revealing a goat.
* You’re asked if you want to switch your choice.

The paradox? Statistically, you should always switch.

* Your original door has a 1/3 chance of hiding the prize.
* The remaining unopened door has a 2/3 chance.

----

# Classic Algorithms

## Win Rates

```
Stander  | ████████████████ 32.5%
Switcher | █████████████████████████████████ 67.9%
Random   | ██████████████████████████ 52.7%
Door2    | █████████████████ 34.9%
```

## Stander

The Stander will randomly choose a door and will always stick with that door.

## Switcher

The Switcher will randomly choose a door and then will always switch when offerred.

## Random

The Random agent will randomly choose a door and then will switch about half the time.

## Door 2

This agent really likes door 2, it's his favorite number, like his super favorite.

## Bringing it together

So what's generally going on here?

The high level of the math for this paradox is that when you randomly (or based on you dedication to the number 2) choose a door it has a 1/3 chance of winning and a 2/3 chance of losing. When the host reveals a door this probablity does not change it was locked in at the first choice. Your door still has a 2/3 chance of losing. But now there is only one other door. That door now has a 2/3 chance of winning.

So if you switch you will win 2/3 times.

This plays out. The switch agent wins the most, the random agent does okay because it switches sometimes. The standing and #2 agent work similarly because it doesn't really matter what the first door is it will always be 1/3.

This establishes a statistical baseline for how well different strategies perform under classic Monty Hall conditions.

## What if we had MOAR doors?

**Doors:** 3

```
Stander       | ███████████████ 31.8%
FirstSwitcher | ████████████████████████████████ 65.2%
AlwaysSwitch  | █████████████████████████████████ 66.9%
SmartSwitcher | █████████████████████████████████ 66.1%
Random        | █████████████████████████ 51.3%
Door2         | ██████████████████ 36.7%
```

**Doors:** 10

```
Stander       | ████ 9.7%
FirstSwitcher | █████ 10.6%
AlwaysSwitch  | ███████████████████████████████ 63.9%
SmartSwitcher | █████████████████████████████████████████████ 91.0%
Random        | █████████████████████████ 51.9%
Door2         | ████ 9.2%
```

**Doors:** 20

```
Stander       | ██ 4.7%
FirstSwitcher | ██ 5.6%
AlwaysSwitch  | ███████████████████████████████ 63.1%
SmartSwitcher | ███████████████████████████████████████████████ 95.0%
Random        | █████████████████████████ 50.5%
Door2         | ██ 4.3%
```

**Doors:** 50

```
Stander       |  1.5%
FirstSwitcher | █ 2.4%
AlwaysSwitch  | ███████████████████████████████ 63.2%
SmartSwitcher | ████████████████████████████████████████████████ 97.6%
Random        | █████████████████████████ 50.6%
Door2         |  1.3%
```

**Doors:** 100

```
Stander       |  1.0%
FirstSwitcher |  0.9%
AlwaysSwitch  | ███████████████████████████████ 62.0%
SmartSwitcher | █████████████████████████████████████████████████ 98.8%
Random        | ████████████████████████ 49.7%
Door2         |  1.0%
```

We tweaked the "idea" of switching a bit here.
Instead of it being just "switch". We taught it a few strategies

- *FirstSwitcher* switches once the first time it's asked
- *AlwaysSwitch* switches every time it's asked
- *SmartSwitcher* switches only the last time it's asked

Why does this matter? The probability at each of those moments is drastically different.

Let's say you have 5 doors. And you have choosen one.

## switching first

If you choose a door after the host has revealed one door then the door you picked has a 1/5 chance of winning and the other doors combined have a 4/5 chance of winning. This means your door has about a 20% chance of winning and the rest have about a 80% chance of winning as a group. It's better but not a ton better, and this benefit loses significance the more doors you pick.

## switching every time

If you switch everytime that's actually a bit more interesting. The probablity does actually keep changing but it's not to you benefit overall, but it's better than only switching first.

The only meaningful change to the probability is really that you swap on the last door. The problem is that moving in between others resets the condensed probability gathered by Monty revealing a door. So the best you can hope for with this strategy is the same 2/3 that you got from the 3 doors.

## switching the last time

Because the host is always revealing losers those reveals will concentrate probability. The longer you wait to switch the more concentrated that probability is. But it is important to switch at the last possible moment to get the best option. If you had 10 doors and switched at 5 you are able to raise your probability from 10 -> 20%. but if you wait until there are only 2 doors. Your door has 10% probability and the other door has 90% probability.

----
----
----
----


### 🔹 **Reinforcement Learning (RL)**

Use an agent that learns through trial and error whether switching is better than staying.

* **Good for**: Showing that agents can converge on the optimal strategy (switching).
* **Interesting twists**:

  * Give misleading rewards early to see if the agent gets stuck.
  * Make the environment non-stationary (change probabilities).
  * See how quickly different RL algorithms learn (Q-learning, DQN, PPO).

---

### 🔹 **Bayesian Reasoning Agent**

Hardcode or learn the actual probabilities.

* **Good for**: Benchmarking rational behavior or testing symbolic vs. statistical reasoning.
* **Fun angle**: See if a naive Bayes-like system can "intuit" switching is better from conditional probability.

---

### 🔹 **LLMs (Language Models)**

Feed the scenario and ask if the model recommends switching.

* **Good for**: Seeing whether it parrots correct math or reflects human fallacies.
* **Bonus**: Try prompt engineering, fine-tuning, or few-shot learning to see if it improves.

---

### 🔹 **Evolutionary Algorithms**

Evolve strategies (e.g. always switch, never switch, random) and see what dominates.

* **Good for**: Exploring strategy space over time and watching convergence.
* **Visualize**: Fitness landscapes, diversity of strategies, mutation effects.

---

### 🔹 **Multi-Agent Simulations**

Have agents play against each other or against environments they think they understand.

* **Good for**: Studying social learning — do agents copy successful strategies?
* **Bonus**: Introduce trust, deception, or misinformation in the host’s behavior.

---

### 🔹 **Explainability-Focused Systems**

Use models designed to *explain* their reasoning.

* **Good for**: Seeing if explainable agents converge faster or avoid traps.
* **Fun test**: Ask for reasoning behind "stay" decisions and compare against ground truth.

---

### What you might discover:

* How fast different AIs converge on "switching"
* Which models fall for the human gut instinct fallacy
* Whether deception (a tricky host) breaks the learned behavior
* How prompt framing affects LLM accuracy
