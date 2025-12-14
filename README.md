# Xolo Pipeline

Xolo Pipeline is a lightweight, modular pipeline framework for VFX and animation projects, designed primarily for freelancers, solo artists, and small studios.

The goal of Xolo is **not** to replicate large studio pipelines, but to provide a clean, practical foundation that grows with your project: from a single artist working locally, to a small team sharing consistent tools, structure, and environments.

This project is still **early-stage** and evolving, but the core ideas and direction are already in place.

---

## Philosophy

Xolo is built around a few simple principles:

* **Simple over clever** – clear structure beats over-engineering
* **Pipeline as glue** – the pipeline connects tools, it does not fight them
* **Artist-friendly** – minimal setup, predictable behavior
* **Modular by design** – features can be added or removed without breaking everything
* **Open and inspectable** – no black boxes

The pipeline is inspired by real production constraints and lessons from books like *Practical Python for Production under Pressure*, as well as tools such as Prism, TikManager, ShotGrid, AYON, and Kitsu — but intentionally much lighter.

---

## Current State

At the moment, Xolo Pipeline focuses on:

* A **Python-based CLI** to launch DCCs in a controlled environment
* A **clear project structure** (projects, assets, shots)
* **Environment management using `uv` only** (no Rez)
* Centralized **OCIO / ACES configuration**
* Early **DCC integrations** (Blender, Gaffer, Nuke planned)

This is not yet a production-ready pipeline, but a solid technical foundation.

---

## Dependency Management

Xolo uses **[`uv`](https://github.com/astral-sh/uv)** as its primary dependency and environment manager.

Reasons for choosing `uv`:

* Fast and simple virtual environments
* Lockfile-based dependency resolution
* Easy installation for artists
* No heavy configuration or package authoring overhead

Each pipeline environment runs inside a controlled Python context, while DCCs are launched with explicit environment variables set by the CLI.

---

## CLI

The pipeline is driven by a custom command-line interface:

```bash
xolo <command> [options]
```

The CLI is built with `typer` and organized using **subcommands**, for example:

* `xolo launch blender <project>`
* `xolo launch gaffer <project>`
* `xolo settings show`

Configuration is stored in a global `config.yaml` and resolved at runtime.

The CLI is intentionally explicit: launching a DCC always goes through the pipeline.

---

## Project Structure

A typical project looks like this:

```text
projects/
  my_project/
    assets/
    shots/
    config/
```

The pipeline sets environment variables such as:

* `PROJECT_ROOT`
* `ASSETS_ROOT`
* `SHOTS_ROOT`

This allows DCC startup scripts to remain clean and predictable.

---

## Color Management (OCIO)

Xolo uses a **centralized OCIO configuration**, currently based on ACES.

The OCIO path is **absolute and pipeline-owned**, meaning:

* The same OCIO config is used regardless of project location
* Artists do not need to configure OCIO manually
* DCCs are launched with `OCIO` already set

This avoids one of the most common sources of inconsistency in small teams.

---

## DCC Integrations

### Blender

* Custom startup scripts
* Pipeline environment variables available at launch
* UI panels and tools are loaded from the pipeline
* Early work on templates and asset/shot workflows

### Gaffer

* Launched through the pipeline
* Startup path injected by the CLI
* Designed to run independently of where Gaffer is installed
* Renderman as a render engine 

### Nuke (planned)

* Support for Non-Commercial and Commercial versions
* Shared startup logic with Gaffer where possible

some of the features are already implemented.

## What Xolo Is *Not*

Xolo is **not**:

* A full production tracker (yet)
* A ShotGrid replacement
* A heavy Rez-based studio pipeline
* A locked, opinionated system

Instead, it is meant to be **a strong starting point**.

---

## Roadmap (High Level)

Planned directions:

* Asset and shot templates
* Publish system (very lightweight)
* Better Blender ↔ Gaffer interoperability (USD-first)
* Optional database / backend layer
* Optional UI frontend in the future

Everything is intentionally incremental.

---

## Installation (Linux only)

This pipeline currently supports installation only on **Linux**. There are two main ways to set up Xolo:

### Recommended: Run the install script

The repository includes a full installer script `setup_env.sh` that:

* Sets up key environment variables
* Persists them in your shell rc (`.bashrc`/`.zshrc`)
* Installs `uv` if missing
* Syncs pipeline dependencies
* Installs a global `xolo` command wrapper

```bash
chmod +x scripts/setup_env.sh
./scripts/setup_env.sh
```

Restart your terminal (or run `source ~/.bashrc` / `source ~/.zshrc`) so the new environment variables and PATH changes take effect.

Verify the installation with:

```bash
xolo --help
```

### 🐍 Alternative: Manual with `uv`

If you prefer to manage environments manually:

1. Create and sync the virtual environment:

```bash
uv venv
uv sync
```

2. Register environment variables:

```bash
source scripts/setup_env.sh
```

> This sets `PIPELINE_ROOT`, `SYSTEM_ROOT`, and modifies your shell rc so Xolo tools work as expected.

---

## Status

This project is under **active development**.

Expect breaking changes, refactors, and experimentation.

---

## License

MIT License

---

## Author

Xolo Pipeline is developed and maintained by **Ronny Ascencio**, with a strong focus on real-world VFX and animation workflows.
