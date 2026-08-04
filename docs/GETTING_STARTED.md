# Setup Guide

This guide gets you from a fresh Windows machine to a running simulation environment. Follow the steps in order.

---

## Step 1 — Install Ubuntu 24.04 (via WSL2)

We develop inside Ubuntu on Windows using WSL2. You can install it from the **Microsoft Store** or via the command line.

**Option A — Microsoft Store** *(easier)*:
Search for **Ubuntu 24.04.x LTS** in the Microsoft Store and click Install.

**Option B — Command line**:
Open **PowerShell as Administrator** and run:
```powershell
wsl --install -d Ubuntu-24.04
```
> Restart your computer if prompted.

Once installed, launch Ubuntu from the Start menu. You will be asked to create a **Linux username and password** — this is separate from your Windows account.

---

## Step 2 — Install Git and Clone the Repository

Inside your Ubuntu terminal:

1. Install Git:
   ```bash
   sudo apt update && sudo apt install -y git
   ```

2. Fork this repository to your own GitHub account.
   *(Not sure how? Ask ChatGPT: "how to fork a GitHub repository")*

3. Clone your fork inside your home directory (`~`) and switch to the task branch:
   ```bash
   cd ~
   git clone <your_forked_repo_url>
   cd probation_ws
   git checkout probation/task
   ```
   > **Note:** Always clone inside your Linux home directory (`~`), NOT inside `/mnt/c/` (the Windows filesystem), to ensure good performance.

---

## Step 3 — Install Docker

Install Docker using `apt` inside Ubuntu — **do not use Docker Desktop**.

1. [Uninstall any older Docker Engine](https://docs.docker.com/engine/install/ubuntu/#uninstall-docker-engine).
2. [Install Docker Engine](https://docs.docker.com/engine/install/ubuntu/).
3. Add your user to the Docker group:
   ```bash
   sudo usermod -aG docker $USER
   ```
4. Close and reopen your Ubuntu terminal (or run `wsl --shutdown` in Windows PowerShell and reopen Ubuntu). Then `cd ~/probation_ws`.

---

## Step 4 — Build and Enter the Container

Inside the `probation_ws` directory:

1. Build the development image *(one-time, ~5 minutes)*:
   ```bash
   docker compose build dev-core
   ```

2. Start the container:
   ```bash
   docker compose run --rm dev-core bash
   ```

3. Inside the container, build the ROS2 workspace:
   ```bash
   colcon build --symlink-install
   ```

> **What `colcon build` does:** Compiles your ROS2 packages in `src/` and generates the `build/`, `install/`, and `log/` workspace directories.
> 
> The container entrypoint automatically sources ROS2 and the workspace on every new shell — no manual `source` needed after the first build.

---

You're ready. Go to [Section 4 of the README](../README.md#4-running-the-simulation) to run the simulation.
