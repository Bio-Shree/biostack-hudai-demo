"""
run_eval.py
-----------
BioStack x hud.ai — Drug-Target Reasoning Agent
Python runner for local evaluation and quick testing.

Usage:
    python run_eval.py                    # runs default single task
    python run_eval.py --task braf        # runs BRAF task
    python run_eval.py --all              # runs all tasks in tasks.json
"""

import asyncio
import argparse
import json
import os

import hud
from hud.agents import create_agent
from env import env

# ── Config ───────────────────────────────────────────────────────────────────

MODEL = "claude-sonnet-4-5"

# ── Predefined quick tasks ────────────────────────────────────────────────────

QUICK_TASKS = {
    "egfr": {
        "target": "EGFR",
        "candidates": ["Erlotinib", "Vemurafenib", "Metformin"],
        "correct": "Erlotinib",
    },
    "braf": {
        "target": "BRAF",
        "candidates": ["Erlotinib", "Vemurafenib", "Metformin"],
        "correct": "Vemurafenib",
    },
    "vegfr2": {
        "target": "VEGFR2",
        "candidates": ["Erlotinib", "Bevacizumab", "Metformin"],
        "correct": "Bevacizumab",
    },
}


def get_answer(result) -> str:
    """Safely extract the agent's final answer from the Trace object."""
    for attr in ("response", "answer", "output", "final_response"):
        val = getattr(result, attr, None)
        if val:
            return str(val).strip()
    # fallback: last message content
    messages = getattr(result, "messages", None)
    if messages:
        last = messages[-1]
        content = getattr(last, "content", None)
        if content:
            return str(content).strip()
    return "N/A"


# ── Single task runner ────────────────────────────────────────────────────────

async def run_single(task_args: dict):
    task = env(
        "match_drug_to_target",
        target=task_args["target"],
        candidates=task_args["candidates"],
        correct=task_args["correct"],
    )

    agent = create_agent(MODEL)

    print(f"\n{'─'*50}")
    print(f"  Target    : {task_args['target']}")
    print(f"  Candidates: {task_args['candidates']}")
    print(f"  Expected  : {task_args['correct']}")
    print(f"{'─'*50}")

    async with hud.eval(task) as ctx:
        result = await agent.run(ctx)

    answer = get_answer(result)
    status = "PASS ✅" if result.reward == 1.0 else "FAIL ❌"
    print(f"  Agent answer : {answer}")
    print(f"  Reward       : {result.reward}")
    print(f"  Status       : {status}")
    print(f"{'─'*50}\n")

    return result.reward


# ── Full tasks.json runner ────────────────────────────────────────────────────

async def run_all():
    tasks_path = os.path.join(os.path.dirname(__file__), "tasks.json")
    with open(tasks_path) as f:
        tasks = json.load(f)

    agent = create_agent(MODEL)

    rewards = []
    print(f"\nRunning {len(tasks)} tasks against {MODEL}\n")

    for i, t in enumerate(tasks, 1):
        args = t["args"]
        task = env(
            "match_drug_to_target",
            target=args["target"],
            candidates=args["candidates"],
            correct=args["correct"],
        )

        async with hud.eval(task) as ctx:
            result = await agent.run(ctx)

        answer = get_answer(result)
        reward = result.reward
        rewards.append(reward)
        status = "✅" if reward == 1.0 else "❌"
        print(
            f"  Task {i:02d} | {args['target']:<8} → "
            f"{answer:<15} | reward={reward:.1f} {status}"
        )

    score = sum(rewards)
    total = len(rewards)
    pct = (score / total) * 100
    print(f"\n{'─'*50}")
    print(f"  Score : {int(score)} / {total}  ({pct:.0f}%)")
    print(f"  Model : {MODEL}")
    print(f"{'─'*50}\n")


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="BioStack x hud.ai eval runner")
    parser.add_argument("--task", choices=QUICK_TASKS.keys(), default="egfr",
                        help="Quick task to run (default: egfr)")
    parser.add_argument("--all", action="store_true",
                        help="Run all tasks from tasks.json")
    args = parser.parse_args()

    if args.all:
        asyncio.run(run_all())
    else:
        asyncio.run(run_single(QUICK_TASKS[args.task]))


if __name__ == "__main__":
    main()