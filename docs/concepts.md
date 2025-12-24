# Core Concepts

Xolo Pipeline is built on a specific set of architectural choices designed to keep development fast, the environment stable, and the artist's workflow predictable.

---

## 1. Pipeline as "Glue"

Xolo follows the philosophy that a pipeline should not be a "black box" that wraps around every software. Instead, it acts as the **glue** between them. 

The pipeline's primary job is to:
1. **Prepare the environment** (Variables, Paths, Dependencies).
2. **Launch the DCC** (Blender, Gaffer, Nuke).
3. **Step out of the way** so the artist can work.

By using the `xolo launch` command, we ensure that every artist on a team is seeing the same colors (OCIO) and looking at the same server paths without manual configuration.

---

## 2. Dependency Management with `uv`

Unlike traditional studio pipelines that use **Rez**, Xolo uses **[`uv`](https://github.com/astral-sh/uv)**.

* **Why `uv`?** It is an extremely fast Python package manager and resolver. It allows Xolo to maintain a "Single Source of Truth" for Python dependencies via a `uv.lock` file.
* **Performance:** `uv` creates and syncs virtual environments in milliseconds, ensuring that the pipeline CLI is always responsive.
* **Artist-Friendly:** It simplifies the installation process. Artists don't need to manage complex environment variables or package authoring; they just run the setup script, and `uv` handles the rest.

---

## 3. Environment Injection

Xolo does not modify your system's global Python or software installations. Instead, it uses **Environment Injection** at the moment of launch.

When you run `xolo launch blender my_project`:
1. Xolo identifies the **Project Root**.
2. It calculates the paths for **Assets** and **Shots**.
3. It sets the `OCIO` variable to the pipeline’s internal ACES config.
4. It starts the Blender process, inheriting only the variables necessary for that project.

This keeps your OS clean and allows you to work on Project A and Project B with completely different settings simultaneously.

---

## 4. The "Folder-as-Truth" Structure

While Xolo may support a database in the future, the current "Source of Truth" is the **File System**.

* **Predictability:** Any artist can browse the project folder and understand where things are without opening a specialized UI.
* **Portability:** Because we use variables like `$ASSETS_ROOT`, you can move an entire project to a different drive. As long as you update your `set-projects` path in Xolo, all your scenes will still find their textures and rigs.

### Standard Hierarchy:
* `assets/`: Incremental storage for models, rigs, and shaders.
* `shots/`: Organized by sequence (e.g., `s01`) and shot (e.g., `p010`).
* `config/`: Contains `project.yaml`, which stores metadata like **Resolution** and **FPS** that the DCCs read on startup.

---

## 5. Color Management (OCIO)

Consistency is the biggest challenge for small teams. Xolo solves this by owning the **OCIO configuration**.

Instead of asking artists to "Please load this ACES config in your Blender settings," Xolo sets the `OCIO` environment variable at the OS level before the DCC starts. Most modern VFX tools (Blender, Gaffer, Nuke, Krita) will automatically detect this variable and lock their color management to the pipeline-approved standard.

---

## 6. Lightweight Metadata

By using `xolo project create`, we store technical requirements (like `1920x1080` at `24fps`) inside a small YAML file in the project folder. 

The goal is to eventually have **DCC Startup Scripts** that read this YAML and automatically set the Blender/Gaffer scene settings to match, preventing human error during the rendering phase.
