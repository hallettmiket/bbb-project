# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BBB Permeability Prediction — predicting blood-brain barrier permeability from molecular structure using the Shaker et al. (2021, Bioinformatics) dataset.

**Stack:** Python, RDKit, XGBoost, Dash, matplotlib

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



## Cross-Agent Communication
Subagents cannot communicate with each other directly. As the conductor, you are responsible for relaying messages between agents. After each agent completes, immediately review its output for requests directed at other agents (e.g., the adversary may leave reading assignments for the bookworm, or the blacksmith may request the artist to visualize specific results). Do not wait — invoke the target agent right away with those requests included in the prompt. For example, if the adversary recommends papers for the bookworm, re-invoke the bookworm immediately with those reading assignments so it can acknowledge and act on them.
