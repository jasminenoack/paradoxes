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
