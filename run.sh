#!/bin/bash

# Enter python virtual environment
source "$1/venv/bin/activate"

# Register workflow and activities
python $1/register_wf.py

# Start workflow execution
LINE1="import boto.swf.layer2 as swf"
LINE2="execution = swf.WorkflowType(name='notifications-wf', domain='btt-workflows', version='1.0', task_list='default').start()"
python -c "$LINE1;$LINE2"

# Start decider
python $1/start_decider.py &

# Start worker
python $1/start_worker.py &

# Wait until everything finishes
wait

# Exit ther virtual environment
deactivate
