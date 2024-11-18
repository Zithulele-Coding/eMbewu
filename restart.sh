#!/bin/bash

# Start a new tmux session (or one could exist)
tmux new-session -d -s eMbewu

# Kill existing process
tmux send-keys -t eMbewu:0 C-c

# Start new process
tmux send-keys -t eMbewu:0 "\
source ./venv/bin/activate && \
git pull && \
pip install -r requirements.txt && \
reflex run --env prod" C-m

exit
