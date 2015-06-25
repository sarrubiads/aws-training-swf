# hello_decider.py
import boto.swf.layer2 as swf
import boto.sqs

class ShouldSendDecider(swf.Decider):

    domain = 'btt-workflows'
    task_list = 'default'
    version = "1.0"

    def run(self):

        # Get the event history
        history = self.poll()
        print history
        if 'events' in history:

            workflow_events = [e for e in history['events']
                               if not e['eventType'].startswith('Decision')]
            last_event = workflow_events[-1]

            decisions = swf.Layer1Decisions()

            # Connect to SQS
            sqs_conn = boto.sqs.connect_to_region('us-east-1')

            # Get the amount of elements in the queue
            queue = sqs_conn.get_queue("Notification_service_ref_13")
            count = queue.count()

            # If the workflow has just started, and the amount of elements in
            # the queue is greater than 0, schedule the "send-notifications"
            # task.
            if last_event['eventType'] == 'WorkflowExecutionStarted':
                if count:
                    print "\n\nSchedule notification-sending task\n\n"
                    decisions.schedule_activity_task('send-notifications',
                                                     "send-notifications",
                                                     self.version,
                                                     task_list=self.task_list)

            # Once the scheduled activity is complete, finish the workflow
            elif last_event['eventType'] == 'ActivityTaskCompleted':
                print "\n\nWorkflow complete\n\n"
                decisions.complete_workflow_execution()
            self.complete(decisions=decisions)
            return True
