#!/bin/bash

python3 -m venv .venv

source .venv/bin/activate

sudo apt update && sudo apt install build-essential python3-dev libgmp3-dev -y

pip install -r requirements.txt

python3 main.py
