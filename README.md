# Ateru Pipeline

**Ateru** is a lightweight, modular pipeline framework for VFX and animation projects, designed for freelancers, solo artists, and small studios who want structure without unnecessary complexity.

The goal of Ateru is simple:  
provide a **clear, predictable production environment** that scales from personal projects to small studio workflows — without locking users into heavy infrastructure or opaque tooling.

> *Explicit structure beats hidden magic.*

---

## What does “Ateru” mean?

**Ateru (当てる / アテル)** is a Japanese verb meaning *to hit the mark*, *to align correctly*, or *to apply something with intention*.

In photography and cinema, it is commonly used when referring to:
- correctly exposing an image
- placing light precisely
- hitting focus
- aligning elements with purpose

This idea sits at the core of the project:  
**a pipeline that helps artists and developers hit the mark — technically and creatively.**

---

## Why Ateru?

Most pipelines fall into one of two extremes:

- overly simple scripts that break as soon as a project grows
- heavyweight systems that are hard to install, hard to maintain, and overkill for small teams

Ateru lives in the middle.

It focuses on:
- explicit configuration
- reproducible environments
- predictable project structure
- tooling that stays out of the artist’s way

No databases.  
No web services.  
No hidden state.  

**Supported systems:**  
- Windows 10/11  
- Ubuntu / Linux (tested with LTS distributions)

---

## Key Features

### 🎬 Standalone Launcher & Project Manager
Ateru includes a standalone **Project Manager** and **DCC Launcher**:

- launch Blender, Gaffer, and Nuke with a controlled environment  
- manage projects, assets, shots, and tasks from a single interface  
- automatically set environment variables, paths, and project configuration

---

### 🛠 Integrated Pipeline in DCCs
Each supported DCC includes pipeline functionality for everyday production tasks:

- **Blender:**  
- - open/save scripts  
  - read/write scenes using USD  
  - import/export assets and references  
  - manage tasks such as layout and modeling 

- **Gaffer:**  
- - open/save scripts  
  - read/write layouts and assets using USD  
  - render 

- **Nuke:**  
  - open/save scripts  
  - import assets, plates, renders, and stock footage  
  - render
  - maintain project consistency  

All DCCs maintain access to **scene files, scripts, and assets**, ensuring full round-trip integration.

---

### 🎨 Unified Color Management
Single source of truth for OCIO / ACES configuration:

- consistent color across all DCCs  
- project-level control  
- no per-application hacks

---

### 🧱 Project Standard
A clear and opinionated project structure for:

- assets  
- shots  
- publishes  
- caches  
- renders  

Designed to be:
- easy to understand  
- easy to extend  
- easy to automate  

---

### ⚡ Modern Tooling
Built using modern, production-oriented tools:

- **uv** for fast Python environment management  
- **Typer** for a clean and explicit CLI  
- optional **Rust** components for performance-critical tasks (experimental and in development)

---

### 🧩 Modular by Design
Ateru is not a monolith.

Each component is designed to be:
- replaceable  
- extendable  
- optional  



---

## Supported DCCs (current focus)

- **Blender**  
- **Gaffer**  
- **Foundry Nuke** (non-commercial and commercial)

The architecture is intentionally designed to support additional DCCs in the future.

---

## Project Philosophy

Ateru follows a few core principles:

- **Explicit is better than implicit**  
- **Configuration over convention**  
- **Local-first workflows**  
- **No hidden global state**  
- **Small, understandable components**  



---

## Status

Ateru is currently **in active development**.

It is:
- not a turnkey studio pipeline  
- not a replacement for ShotGrid, AYON, or similar systems  
- not intended for large, multi-site productions  

What it *is*:
- a solid technical foundation  
- a learning-focused but production-aware project  
- a practical pipeline for real-world use  

Breaking changes may occur while the core stabilizes.

---

## Documentation

Planned documentation includes:

- [Installation Guide](docs/installation.md)  
- [Quickstart Guide](docs/quickstart.md)  
- [Core Concepts](docs/concepts.md)  
- [Limitations & Scope](docs/limitations.md)  

Documentation will grow alongside the codebase.

---

## Who is this for?

Ateru is built for:
- freelancers  
- technical artists  
- pipeline developers  
- small studios  
- anyone who wants to understand *how* their pipeline works, not just use it  

If you value clarity over convenience, Ateru is for you.

---

## License

Ateru is released as an open-source project.  
See the `LICENSE` file for details.

---

## Explore the Code

If you’re curious, start with:
[Explore the Code](https://gitlab.com/ronnyascencio/ateru)  

Everything is meant to be readable.
