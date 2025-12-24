# Limitations & Scope

To keep Xolo lightweight, we have made intentional choices about what this pipeline is **not**.

### Not a Production Tracker
Xolo does not replace tools like **ShotGrid, Kitsu, or Ayon**. It handles the technical execution (launching, paths, environment), not the production scheduling or status tracking.

### Linux First
Currently, the automation scripts are Bash-based. Windows support (PowerShell) is on the roadmap but not currently a priority.

### No "Black Boxes"
Xolo is designed for technical artists who want to see what's happening. If you need a "one-click" GUI that hides everything from the artist, Xolo might feel too exposed.

### Lightweight Asset Management
The "Publish" system is currently in its infancy. Do not expect complex versioning logic or automated dependency tracking out of the box yet.
