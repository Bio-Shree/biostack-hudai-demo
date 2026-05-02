# Drug Discovery AI Demo — Complete Video Script
**Total runtime: ~3:30 | Record with Loom — screen + face bubble ON**


## BEFORE YOU HIT RECORD — SETUP CHECKLIST

- [ ] Terminal 1 open → `hud dev env:env -w env.py` already running
- [ ] Terminal 2 open → ready to type `python run_eval.py --all` 
- [ ] VS Code open → `env.py` loaded, scrolled to top
- [ ] Browser tab open → hud.ai/home (logged in, last trace visible)
- [ ] Browser tab open → GitHub repo README
- [ ] Loom set to: screen + face bubble ON



## INTRO — 0:00 to 0:30
**What's on screen:** Clean desktop, nothing open yet.

**You say:**
> "Hey — quick demo of something I built this week.
> Before I show you what I built, one quick thing on the platform I used — hud.ai.
>
> hud.ai lets you build environments where an AI agent can use tools,
> complete a task, and get a score for how well it did.
> Every run gets recorded automatically — what the agent did, why it did it,
> and whether it got it right.
>
> If you've heard of NVIDIA's NeMo Gym — that's a tool for actually training the model.
> hud.ai sits one step before that — it's where you create the situations
> the model learns from. Think of NeMo as the gym equipment,
> and hud.ai as the coach designing the workout.
>
> Now let me show you what I built with it."



## SCENE 1 — THE PROBLEM — 0:30 to 1:00
**What's on screen:** README open in browser. Show this line clearly:
> *"The bottleneck in biomedical AI isn't the model. It's the data."*

**You say:**
> "The problem I'm solving is this.
> Drug discovery researchers have huge amounts of biological data —
> which proteins cause which diseases, which drugs block which proteins.
> But that data is scattered, unstructured, and impossible for an AI to reason over.
>
> Models like Claude or GPT are incredibly capable.
> But without structured, domain-specific data to work with —
> they're guessing.
>
> What I built here is a small working proof of that idea:
> take structured biological data, package it as tools an AI can call,
> give it a task, and watch it reason its way to the right answer."


## SCENE 2 — THE CODE — 1:00 to 1:45
**What's on screen:** VS Code, `env.py` open. Scroll slowly — tools first, then scenario.

**You say:**
> "This is the environment file — `env.py`.
>
> Two tools here — think of these as two database lookups
> the AI agent is allowed to call.
>
> [point to get_target_info]
>
> The first one: give it a protein name, it tells you what disease that protein drives
> and where on the protein a drug could bind.
> In a real production system, this would be pulling from live lab data.
> Here it's a structured mock — but the shape is identical.
>
> [scroll to get_compound_profile]
>
> The second one: give it a drug name, it tells you what that drug does,
> what it targets, and whether it's FDA approved.
>
> [scroll to scenario]
>
> And here's the task — the scenario.
> The agent gets a protein target and three candidate drugs.
> It has to call those tools, think through the biology,
> and output exactly one answer — the right drug for that target.
> Score 1.0 if correct. Score 0.0 if wrong.
> Simple, clean, trainable."



## SCENE 3 — RUN THE EVAL LIVE — 1:45 to 2:30
**What's on screen:**
- Show Terminal 1 first — point at `hud dev` running
- Switch to Terminal 2 — type `python run_eval.py --all` and hit enter
- Let the output stream — DO NOT TALK while results are appearing
- PAUSE on the reward scores for 3 full seconds

**You say (before running):**
> "Two terminals.
> Terminal 1 — this is the environment running as a live server.
> Tools loaded, scenario ready, waiting for an agent.
>
> Terminal 2 — I'll kick off the evaluation now.
> Six tasks, all going to Claude. Watch the scores come in."

[HIT ENTER — stay quiet — let it run]

[Once all results show — pause — then speak]

**You say:**
> "Six for six. Every single task — reward 1.0.
>
> What's important here isn't just that it got them right.
> It's *how* it got them right.
> The agent didn't guess. It called the tools,
> read the data, and reasoned its way to the answer —
> the same way a trained human researcher would.
>
> That reasoning chain — that's the valuable thing.
> That's what becomes training data."



## SCENE 4 — THE hud.ai DASHBOARD — 2:30 to 3:00
**What's on screen:** Browser → hud.ai/home → click one trace → show tool calls + reasoning

**You say:**
> "This is what hud.ai captures for every single run.
>
> You can see exactly which tools the agent called and in what order.
> You can read the full chain of reasoning — step by step — before the final answer.
> And the reward score is right there attached to the trace.
>
> Here's why this matters.
> Every correct trace like this one — good reasoning, right answer —
> can be fed back into a model as training data.
> Run thousands of these over real biological data,
> and the model gets genuinely better at this specific kind of reasoning.
> Not just smarter in general — smarter at drug discovery.
> That's the loop."



## SCENE 5 — THE BIGGER PICTURE — 3:00 to 3:20
**What's on screen:** README — scroll to the roadmap table

**You say:**
> "What you just saw has 3 drugs, 3 protein targets, and toy data.
>
> The real version of this has a full compound library from lab data,
> a complete panel of disease targets,
> and reward signals that score on binding strength, safety, and drug-likeness —
> not just whether the name matches.
>
> But the architecture is exactly the same.
> Structured data as tools. Tasks with reward signals. Traces that train models.
>
> This is the proof the approach works."


## SCENE 6 — CLOSE — 3:20 to 3:30
**What's on screen:** GitHub repo open in browser

**You say:**
> "All the code is on GitHub — link in the description.
> The README has the full breakdown and where this is going.
> Happy to walk through any part of it in more detail."



## ONE PAGE CHEAT SHEET — hud.ai vs NeMo Gym

If anyone asks — here's how to explain it simply:

**NeMo Gym** = the training framework. You use it to actually update a model's weights.
It's powerful but complex — you need GPUs, infrastructure, a full ML team.

**hud.ai** = the environment layer. You use it to create situations where an agent
can practice a task and get scored. No GPU needed. Running in an hour.

**The analogy:** NeMo is the gym equipment. hud.ai is the coach
who designs the exercises and tracks your progress.
You need both — but hud.ai is where you start.



*The moment that matters most: when the terminal shows reward=1.0 six times.*
*Stop talking. Let it sit for three seconds. That's your proof of concept.*


## WHAT TO SEND

```
3 min demo — AI agent reasoning over drug discovery data.

Loom: [link]
GitHub: [link]
```
