# Setting up BIOMOD on another laptop

This repo holds the **dry-lab predator-prey simulator** (Fujii system) plus the
**Claude Code memory files** that give Claude full context on the project.

## 1. Install prerequisites
- **Git** — https://git-scm.com/download/win (or `winget install Git.Git`)
- **Python 3** with `numpy`, `scipy`, `matplotlib`:
  ```powershell
  pip install numpy scipy matplotlib
  ```

## 2. Clone the repo
```powershell
cd $HOME
git clone https://github.com/kpuchkov1-code/BIOMOD.git
cd BIOMOD
```

## 3. Restore Claude's project memory
This copies the memory files into Claude Code's local config so Claude on this
laptop knows the project background:
```powershell
./claude-memory/restore-memory.ps1
```

## 4. Launch Claude
Run `claude` from your **home directory** (`C:\Users\<you>`) — the same place the
memory was restored to — and it will load the BIOMOD context automatically.

## What's here
| Path | What it is |
|------|-----------|
| `fujii_pp_model.py` | Core predator-prey ODE model (paper-exact, SI eqs 3-4) |
| `stability_analysis.py` | Fixed points / linear stability |
| `sensitivity_analysis.py` | Parameter sensitivity sweeps |
| `sequence_check.py` | DNA sequence validation |
| `crowding_map.md` | Plan for the molecular-crowding layer (next step) |
| `*.png` | Reproduced figures (phase plane, bifurcation, sensitivity) |
| `claude-memory/` | Claude Code context files + restore script |
