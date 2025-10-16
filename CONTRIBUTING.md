# Contributing to Xolo Pipeline

Thanks for your interest in contributing to **Xolo Pipeline**!
This document outlines the workflow and conventions for development.

---

## 🧩 Branch Strategy

We follow a simple **Git branching model** inspired by GitFlow:

- **`main`** → Stable production-ready code.
- **`dev`** → Integration branch for new features.
- **`feature/<short-desc>`** → Feature branches off `dev`.
  - Example: `feature/ocio-support`
- **`release/vX.Y.Z`** → Prepares a version release.
  - Example: `release/v1.2.0`
- **`hotfix/<short-desc>`** → Urgent fixes off `main`.

### Typical flow
1. Create a new branch from `dev`:
   `git checkout -b feature/my-new-feature dev`
2. Implement your feature.
3. Push and create a PR into `dev`.
4. Once approved and merged → included in next release.

---

## 🧮 Versioning

We use **Semantic Versioning (SemVer)**:
`vMAJOR.MINOR.PATCH`

- **MAJOR** → Breaking changes.
- **MINOR** → New features (backward compatible).
- **PATCH** → Bug fixes and small improvements.

Example: `v1.3.2`

---

## 🧱 Code Style

- Python code follows **PEP8**.
- Use **black** for formatting.
- Use **ruff** for linting.
- Type hints required for all functions.

---

## ✅ Pull Requests

- PRs must target `dev`, never `main`.
- Include a clear title and description.
- Link related issues (e.g., `Closes #42`).
- At least one approval required before merge.

---

## 🧪 Testing

- All code must include basic tests (pytest).
- Run tests locally before submitting PRs:
  ```bash
  uv run pytest
