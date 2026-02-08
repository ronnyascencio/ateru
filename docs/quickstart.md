# Quickstart Guide: Xolo Pipeline

This guide will help you configure your environment and launch your first DCC (Digital Content Creation) tool using the Xolo CLI.

---

## 1. Initial Configuration

Before launching any software, you must tell Xolo where your projects are located and where your software executables live.

### Set your Projects Root
Define the base directory where all your VFX projects will be stored:
```bash
ateru settings set "/path/to/your/projects_folder"
```
## Register your Software (DCCs)

You need to register the path and version of the tools you want to use. Example for Blender and Gaffer:


```bash
ateru settings set Blender 4.2 "/usr/bin/blender"
ateru settings set Gaffer 1.4.5.0 "/opt/gaffer/bin/gaffer"
```
## Verify Configuration

Check that everything is saved correctly in your config.yaml:
Bash
```bash
ateru settings show
```

## Creating a New Project

Xolo handles folder structures and technical metadata (Resolution, FPS) automatically via an interactive prompt.
Start the Wizard

```bash
ateru project create
```

The wizard will ask for:

   - Project Name: (e.g., my_short_film)

   - Resolution: (e.g., 1920x1080)

   - FPS: (e.g., 24)

What happens behind the scenes?

Xolo creates the following structure based on your ``` projects_root:```

```
my_short_film/
├── assets/         # Geometry, textures, rigs
├── shots/          # Sequences and animation frames
├── config/
│   └── pconfig.toml # Stores your Resolution and FPS
├── usd/  
└── ...
```
## Verify Project Info

To see the technical details of a created project:
```bash

ateru project show
```

## Launching your First Project

Xolo uses a specific command to launch software within a controlled environment. This ensures that plugins, color management (OCIO), and paths are correctly set.
Command Structure
```bash

ateru launch <software> <project_name>
```
Examples

   - Launch Blender:

```bash
ateru launch blender my_awesome_short
```
   - Launch Gaffer:
```bash

ateru launch gaffer my_awesome_short
```

## Environment Variables

Once the software is open, you can access these variables within Python or file paths to keep your scenes "project-agnostic":
Variable	Purpose
```
$PROJECT_ROOT	Absolute path to the active project.
$ASSETS_ROOT	Path to the /assets directory.
$SHOTS_ROOT	Path to the /shots directory.
$OCIO	Automatic path to the pipeline's ACES config.
```

##  Summary of Commands
Context	Command	Description
Setup	ateru settings show	View global paths and registered software.
Projects	ateru project create	Start the interactive project creator.
Projects	ateru project show	Check resolution/FPS of a project.
Launch	ateru launch [dcc] [project]	Open a tool with the correct environment.
Next Steps

   - Create your first project using xolo project create.

   - Launch Blender.

   - Check the Color Management settings; they should be automatically locked to the Xolo ACES config.

   - Happy Rendering!

Tip: If you need to remove a project, you can use xolo project delete, but be careful—this action is permanent!
