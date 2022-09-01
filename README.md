# my-movie-watchlist

A simple cli-based python application as a movie watchlist with SQL database.

## Requirements

This project has the following dependencies:

```txt
python>=3.8
PyPika==0.48.9
pytz==2022.2.1
```

## Installation

To be able to use and run this project, first we need to make a virtual environment, activate it and install depdendencies

```bash
# Creating virtual environment (venv)
python -m venv .venv

# Sourcing the created venv
source .venv/bin/activate      # If Running on Linux/MacOS
source .venv/Scripts/activate  # If Running on Windows

# Updating pip package manager for venv
python -m pip install --upgrade pip

# Installing dependencies
pip install -r requirements.txt
```

## How to Run

To run the application just execute the following:

```bash
python app.py
```
