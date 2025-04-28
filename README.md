# Agentic Systems & Long-Horizon Planning

Exploring the boundaries of autonomous AI agents through architectural constraints, persistent state, and explicit decision logic.

## 🚀 Overview

This project is a deep dive into building reliable multi-step agents. Most autonomous agents fail over long horizons due to "reasoning drift" and state corruption. We address this by:

1. **Explicit State Management**: SQLite-backed persistence ensures agents can recover from crashes.
2. **Circuit Breaker Retries**: Prevents "infinite loops" of failure when external tools or LLMs are down.
3. **Autonomy Envelopes**: Mathematically modeling confidence decay over execution chains.
4. **Decision Boundaries**: Forcing "escalation to human" when confidence or constraints are violated.

## 📁 Project Structure

- `src/core/`: Foundation classes (Agent, State, Retry, Decision).
- `src/planning/`: Logic for decomposing goals into task graphs and validating them.
- `src/autonomy/`: Monitoring systems for safety and stability.
- `src/failure/`: Research into how agents fail and how to recover.
- `examples/`: Guided walkthroughs of the system.

## 🛠 Installation

```bash
git clone https://github.com/thanhauco/pulsing-nova.git
cd pulsing-nova
pip install -r requirements.txt
```

## 🏗 Key Concepts

### Autonomy Envelope

The system monitors how far from the "initial plan" the agent has drifted. Every step adds a small amount of uncertainty. When uncertainty exceeds a threshold, the agent must pause for re-validation or human intervention.

### Decision Boundaries

Instead of letting the LLM decide everything, we define `DecisionPoints`. These are explicit gates in the code where the system checks:

- Confidence levels
- Authorization constraints
- Safety parameters

## 📈 Research Goals

- [ ] Quantify at which point "Full Autonomy" becomes dangerous in long execution chains.
- [ ] Evaluate the effectiveness of hierarchical task decomposition in reducing reasoning drift.
- [ ] Benchmark recovery strategies (Rollback vs. Replanning).

---

Developed by **Thanh Vu**
