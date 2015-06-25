SWF - Training AWS
==================

This project registers a worklow and an activity in Amazon's SWF. And triggers an execution of such.
The workflow polls an SQS queue, extracts messages and sends them using SES to a list of email addresses
configurable in config.yaml

Execution
---------

1. Clone this repo
2. Make sure python 2.7 and virtualenv are installed
3. Create a virtual environment ``virtualenv venv``
4. Activate the virtual environment ``source venv/bin/activate``
5. Upgrade pip ``pip install -U pip``
6. Install dependencies ``pip install -r <PROJECT_FOLDER>/requirements.txt``
7. Change to the project folder  ``cd <PROJECT_FOLDER>``
8. Register the activities and run the worklflow ``./run.sh .``
