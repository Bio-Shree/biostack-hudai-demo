# 🧬 BioStack × hud.ai — Toy Proof of Concept

> **Internal Founder Brief** | Drug-Target Reasoning Agent on hud.ai RL Platform

---

![BioStack Banner](./images/biostack_banner_placeholder.png)
*^ Replace with BioStack logo / banner image*

---

## 📌 What We Built

A toy **Reinforcement Learning environment** on [hud.ai](https://hud.ai) that teaches an AI agent to match drug compounds to protein targets — using tools and multi-step reasoning.

This is a minimal proof-of-concept that demonstrates how **BioStack's data pipelines** can be packaged as RL training environments for AI labs.

---

## 🎯 Why This Matters for BioStack

| Problem | BioStack's Answer | This Demo Shows |
|---|---|---|
| Biological data is fragmented & unstructured | We structure it into ML-ready pipelines | Structured drug/target data as agent-callable tools |
| Static datasets don't teach reasoning | We build workflow-aligned environments | Agent must reason step-by-step, not just pattern match |
| AI labs need post-training signal | We package data for RL fine-tuning | hud.ai traces every reward signal for training |

---

## 🏗️ Architecture Overview

![Architecture Diagram](./images/architecture_placeholder.png)
*^ Replace with: BioStack Data Pipeline → hud.ai Environment → Agent → Reward Loop diagram*

```
BioStack Structured Data
         ↓
  hud.ai Environment (env.py)
  ├── Tools  →  get_target_info()
  │             get_compound_profile()
  └── Scenario → match_drug_to_target()
         ↓
  AI Agent (Claude / GPT / Gemini)
  └── Reasons using tools → outputs answer
         ↓
  Reward Signal (1.0 correct / 0.0 wrong)
         ↓
  Successful traces → Fine-tune / GRPO Training
         ↓
  Better domain-specific BioStack AI
```

---

## 🧪 The Toy Use Case — Drug-Target Matching

### Scenario
The agent receives:
- A **protein target** (e.g., `EGFR` — a cancer-driving kinase)
- **3 candidate drug compounds** (e.g., Erlotinib, Vemurafenib, Metformin)

It must call our tools, reason through the biology, and output the **best therapeutic match**.

### Example Task

```json
{
  "target": "EGFR",
  "candidates": ["Erlotinib", "Vemurafenib", "Metformin"],
  "correct_answer": "Erlotinib"
}
```

### What the Agent Does

![Agent Reasoning Trace](./images/agent_trace_placeholder.png)
*^ Replace with: screenshot of hud.ai dashboard showing agent tool calls + reasoning chain*

1. Calls `get_target_info("EGFR")` → learns it's a tyrosine kinase in lung cancer
2. Calls `get_compound_profile("Erlotinib")` → learns it's a reversible EGFR inhibitor
3. Calls `get_compound_profile("Vemurafenib")` → learns it targets BRAF (different kinase)
4. Reasons: *"EGFR needs an EGFR inhibitor → Erlotinib"*
5. Outputs: `Erlotinib` ✅ → **Reward: 1.0**

---

## 📁 Project Structure

```
biostack-drug-env/
├── env.py          ← Environment: tools + evaluation scenarios
├── tasks.json      ← Dataset: drug-target task instances
├── run_eval.py     ← Python runner for local testing
├── hud.toml        ← hud.ai project config
└── README.md       ← This file
```

---

## 💻 Full Code

### `env.py` — The RL Environment

```python
from hud import Environment

env = Environment("biostack-drug-env")

# ── TOOLS ────────────────────────────────────────────────────────────────────

@env.tool
def get_target_info(target_name: str) -> dict:
    """Returns clinical context about a protein target."""
    targets = {
        "EGFR": {
            "full_name": "Epidermal Growth Factor Receptor",
            "role": "Tyrosine kinase driving cell proliferation",
            "disease": "Non-small cell lung cancer (NSCLC)",
            "binding_site": "ATP-binding pocket in kinase domain",
        },
        "BRAF": {
            "full_name": "B-Raf proto-oncogene serine/threonine-protein kinase",
            "role": "MAP kinase pathway regulator",
            "disease": "Melanoma (V600E mutation)",
            "binding_site": "Activation loop of kinase domain",
        },
    }
    return targets.get(target_name, {"error": "Target not found"})


@env.tool
def get_compound_profile(compound_name: str) -> dict:
    """Returns molecular profile of a drug candidate."""
    compounds = {
        "Erlotinib": {
            "type": "Small molecule",
            "mechanism": "Reversible EGFR inhibitor",
            "selectivity": "High for EGFR",
            "clinical_stage": "FDA approved",
        },
        "Vemurafenib": {
            "type": "Small molecule",
            "mechanism": "Selective BRAF V600E inhibitor",
            "selectivity": "High for mutant BRAF",
            "clinical_stage": "FDA approved",
        },
        "Metformin": {
            "type": "Biguanide",
            "mechanism": "AMPK activator, reduces gluconeogenesis",
            "selectivity": "Metabolic target (not kinase)",
            "clinical_stage": "FDA approved (diabetes)",
        },
    }
    return compounds.get(compound_name, {"error": "Compound not found"})


# ── SCENARIO ─────────────────────────────────────────────────────────────────

@env.scenario("match_drug_to_target")
async def match_drug_to_target(target: str, candidates: list[str], correct: str):
    """Agent must pick the best drug for the given protein target."""
    prompt = f"""
    You are a drug discovery assistant at BioStack.

    Protein target: {target}
    Candidate compounds: {candidates}

    Tools available:
    - get_target_info(target_name) → clinical & biological context
    - get_compound_profile(compound_name) → molecular mechanism & selectivity

    Use the tools, reason step by step, then output your answer as 
    exactly one compound name from the candidates list.
    """
    response = yield prompt
    reward = 1.0 if response.strip() == correct else 0.0
    yield reward
```

### `tasks.json` — Evaluation Tasks

```json
[
  {
    "scenario": "match_drug_to_target",
    "args": {
      "target": "EGFR",
      "candidates": ["Erlotinib", "Vemurafenib", "Metformin"],
      "correct": "Erlotinib"
    }
  },
  {
    "scenario": "match_drug_to_target",
    "args": {
      "target": "BRAF",
      "candidates": ["Erlotinib", "Vemurafenib", "Metformin"],
      "correct": "Vemurafenib"
    }
  },
  {
    "scenario": "match_drug_to_target",
    "args": {
      "target": "EGFR",
      "candidates": ["Vemurafenib", "Metformin", "Erlotinib"],
      "correct": "Erlotinib"
    }
  }
]
```

### `run_eval.py` — Python Runner

```python
import asyncio
import hud
from hud.agents import create_agent

env = hud.load_env("biostack-drug-env")

task = env(
    "match_drug_to_target",
    target="EGFR",
    candidates=["Erlotinib", "Vemurafenib", "Metformin"],
    correct="Erlotinib"
)

agent = create_agent("claude-sonnet-4-5")

async def main():
    async with hud.eval(task) as ctx:
        result = await agent.run(ctx)
        print(f"Agent answer : {result.response}")
        print(f"Reward       : {result.reward}")

asyncio.run(main())
```

---

## 🚀 Setup & Run (Step by Step)

### Prerequisites
- Python 3.11 or 3.12
- A [hud.ai](https://hud.ai) account + API key

### Install

```bash
# 1. Install uv (fast Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Install hud CLI
uv tool install hud-python --python 3.12

# 3. Set your API key
export HUD_API_KEY=your-key-here

# 4. Login
hud login
```

### Run

```bash
# 5. Create project
hud init biostack-drug-env
cd biostack-drug-env

# 6. Paste in env.py and tasks.json from above

# 7. Start local dev server (hot reload)
hud dev env:env -w env.py

# 8. Run evaluation
hud eval tasks.json claude-sonnet-4-5

# 9. Deploy to cloud
hud deploy
```

---

## 📊 Expected Results

![Eval Results Screenshot](./images/eval_results_placeholder.png)
*^ Replace with: screenshot of terminal showing reward scores per task*

```
Task 1 — EGFR  →  Erlotinib     ✅  reward = 1.0
Task 2 — BRAF  →  Vemurafenib   ✅  reward = 1.0
Task 3 — EGFR  →  Erlotinib     ✅  reward = 1.0

Score: 3 / 3  (100%)
Avg reward: 1.0
```

---

## 📈 Dashboard Traces

![hud.ai Dashboard](./images/dashboard_placeholder.png)
*^ Replace with: screenshot from hud.ai/home showing traces, tool calls, reward logs*

Every agent run is automatically traced at **hud.ai/home** — you can see:
- Every tool the agent called
- The full reasoning chain
- Reward scores per task
- Which traces to use for training

---

## 🗺️ What Comes Next (Real BioStack Roadmap)

| Toy Demo (Today) | Real BioStack Environment (Next) |
|---|---|
| 3 hardcoded compounds | Real compound library from CRO data |
| 2 protein targets | Full target panel across therapeutic areas |
| Simple string match reward | Multi-signal reward (binding affinity, ADMET, safety) |
| Single scenario | Multi-step workflows (screen → select → optimize) |
| Synthetic tool data | Live EHR + assay data from BioStack pipelines |

---

## 🔗 Resources

- [hud.ai Platform](https://hud.ai)
- [hud.ai Documentation](https://docs.hud.ai)
- [hud-python GitHub](https://github.com/hud-evals/hud-python)
- [BioStack Website](https://your-biostack-site.com) ← *update this*

---

## 👥 Team

| Role | Name | Contact |
|---|---|---|
| Founder | *[Founder Name]* | *[email]* |
| Built by | *[Your Name]* | *[email]* |

---

*Built as a learning demo to explore hud.ai for BioStack's RL data environment strategy.*
*Date: May 2026*
