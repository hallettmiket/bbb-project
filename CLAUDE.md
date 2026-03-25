# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BBB Permeability Prediction — predicting blood-brain barrier permeability from molecular structure using the Shaker et al. (2021, Bioinformatics) dataset.

**Stack:** Python, RDKit, XGBoost, streamlit, matplotlib

**Dataset:** B3DB (Meng et al. 2021, Scientific Data) — NOT Shaker et al. Always attribute to B3DB/Meng et al.

**Branding:** Presentations and formal outputs should include Western University, Schulich School of Medicine, and Hallett Lab logos from `./assets/`. Place all three on the title slide.

## Demo Layout

`start_demo.sh` launches a tmux session (`bbb-demo`) with 5 named panes:
- **Conductor** (top) — orchestration pane
- **Blacksmith**, **Bookworm**, **Artist**, **Adversary** (bottom row) — worker panes

Run with: `./start_demo.sh`

## Agent Team Configuration
This project uses four specialist subagents:
- **BLACKSMITH**: data analysis, RDKit descriptors, classifier training, Dash GUI
- **BOOKWORM**: literature survey, PubChem/ChemDB queries, Slack reporting
- **ARTIST**: matplotlib figures, SHAP plots, PowerPoint generation
- **ADVERSARY**: validation, data leakage checks, cross-validation auditing

All agents write outputs to ./outputs/<agent-name>/
Enable agent teams with: export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1

You should always first go into planning mode and show their plan. This is a demonstration to a large audience so we want to showcase planning etc. Please show the plan and then execute it.

## Git Workflow
When asked to commit, stage all changed files (except those in .gitignore), create a descriptive commit, and push to origin/main.



## Agent Voice (TTS)
All agents use `./speak.sh` (OpenAI TTS HD) to speak aloud at key milestones and when answering questions. Each agent has a distinct voice matching their personality (onyx/nova/fable/echo). The conductor voice is alloy.

### Asking Subagents Questions
When the user says "ask the blacksmith ..." or "question for the adversary ...", the conductor must:
1. Spawn the named agent with the question as its prompt, prefixed with: "The conductor is relaying a question from the audience. Answer in 2-3 sentences in your personality voice, and speak your answer aloud using ./speak.sh <agent-name>."
2. The agent answers in character, speaks it via speak.sh, and returns the text.
3. The conductor displays the text response to the user.

**TTS chunking rule:** Each `./speak.sh` call must contain at most 2 sentences. For longer answers, agents must split into multiple sequential `./speak.sh` calls. Long text will get cut off otherwise.

This works for any agent: blacksmith, bookworm, artist, adversary.

## Cross-Agent Communication
Subagents cannot communicate with each other directly. As the conductor, you are responsible for relaying messages between agents. After each agent completes, immediately review its output for requests directed at other agents (e.g., the adversary may leave reading assignments for the bookworm, or the blacksmith may request the artist to visualize specific results). Do not wait — invoke the target agent right away with those requests included in the prompt. For example, if the adversary recommends papers for the bookworm, re-invoke the bookworm immediately with those reading assignments so it can acknowledge and act on them.

## Bookworm Parallelization Rule
When the bookworm has multiple independent tasks (e.g., looking up N molecules, summarizing N papers, querying N databases), the **conductor must split the work across multiple parallel bookworm agents** rather than giving everything to a single bookworm. Guidelines:
- **Molecule lookups**: ~5-10 molecules per bookworm agent (aim for 5+ agents)
- **Paper summaries**: 1 bookworm agent per paper
- **Database queries**: split by molecule or target, not by database
- Each sub-bookworm gets a unique library-themed name (Dewey, Gutenberg, Alexandria, Marginalia, Foxpage, Quarto, Colophon, Octavo) and introduces itself in `./outputs/bookworm/progress.log`
- After all parallel bookworms finish, spawn one final consolidation bookworm to merge results into the portal
- More parallelism is always preferred — err on the side of too many agents

## Chrome Tab Management
All subagents must close their previous portal Chrome tab before opening the updated one. Use AppleScript:
```
osascript -e 'tell application "Google Chrome" to repeat with w in windows
  repeat with t in tabs of w
    if title of t contains "AGENT_NAME" then close t
  end repeat
end repeat'
```
Then open the new portal. This prevents tab accumulation during the demo.
