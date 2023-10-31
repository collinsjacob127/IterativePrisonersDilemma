[![Python application](https://github.com/collinsjacob127/IterativePrisonersDilemma/actions/workflows/python-app.yml/badge.svg)](https://github.com/collinsjacob127/IterativePrisonersDilemma/actions/workflows/python-app.yml)
# IterativePrisonersDilemma

<!-- ![](https://github.com/collinsjacob127/IterativePrisonersDilemma/blob/main/graphs/complete/test1/varying_prisoner_strat.gif) -->
<p align="center">
<img src="https://github.com/collinsjacob127/IterativePrisonersDilemma/blob/main/graphs/complete/test1/varying_prisoner_strat.gif" border="10"/>
</p>

## Authors

* Lucas Butler
* Jacob Collins
* Spencer Pollard
* Suneetha Tadi

## Goal

Simulate the [prisoner's dilemma](https://en.wikipedia.org/wiki/Prisoner's_dilemma) as a network and determine what factors influence prisoner's behavior over time as a community.

## Instructions

### Clone Repo + Making Changes (Linux/WSL)
[Instructions](https://learn.microsoft.com/en-us/windows/wsl/install) for setting up WSL, if needed.

Download the repo:
```
git clone https://github.com/collinsjacob127/IterativePrisonersDilemma.git
cd IterativePrisonersDilemma/
```
Make your own branch:
```
git checkout -b example_branch_name
```
Save and upload your changes:
```
git add -A
git commit -m "Added foo"
git push -u origin example_branch_name
```
Pull updates from main to your branch:
```
git pull origin main
```
(Sometimes ```git pull origin main --rebase``` can be helpful if there are conflicts)

Pull requests (from your branch to main) are made in the GitHub UI.

[This guide](https://www.digitalocean.com/community/tutorials/how-to-create-a-pull-request-on-github) describes some more in-depth features for working with remote repositories.

### Setting Up Python Venv (Linux/WSL)

Python virtual environments are great for separating your projects and keeping python lightweight. It essentially makes a container for you with your needed installed packages so that anything you do only affects the venv and not your base installation of python.

Creating a venv:
```
python -m venv ~/.venv/example_venv_name
```
Note: 
* ```python``` may be called ```python3``` depending on your installation.
* Do not create the venv in the same folder as your python files or it will run very slowly.

Activating a venv:
```
source ~/.venv/example_venv_name/bin/activate
```

Deactivating a venv:
```
deactivate
```

Installing required packages:
```
python3 -m ensurepip --upgrade
pip install -r requirements.txt -U
```

