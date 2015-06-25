import boto.swf.layer2 as swf
import boto.sqs
import boto.ses
import boto.s3
import random
import yaml
import string


class NotificationWorker(swf.ActivityWorker):

    domain = 'btt-workflows'
    version = '1.0'
    task_list = 'default'

    def run(self):

        with open("config.yaml", 'r') as stream:
            config = yaml.load(stream)

        sender = config["sender"]
        recipients = config["recipients"]

        activity_task = self.poll()
        print activity_task

        if 'activityId' in activity_task and activity_task['activityId'] == 'send-notifications':
            # Connect to Amazon SQS
            sqs_conn = boto.sqs.connect_to_region('us-east-1')
            # Connect to Amazon SES
            ses_conn = boto.ses.connect_to_region('us-east-1')
            # Connect to Amazon S3
            s3_conn = boto.s3.connect_to_region('us-east-1')
            # Get the queue
            queue = sqs_conn.get_queue("Notification_service_ref_13")
            # Get the bucket
            bucket = s3_conn.get_bucket('btt-private-logs')
            # Get a list with all the messages
            rs = queue.get_messages()
            for message in rs:
                # Get the body of the message
                body = message.get_body()
                # Send a notification with that message
                ses_conn.send_email(sender,
                                    'BTT Notification Service',
                                    body,
                                    recipients)
                # Save the notification in s3
                key = boto.s3.key.Key(bucket)
                key.name = ''.join(random.choice(string.ascii_uppercase
                                                 + string.digits)
                                   for _ in range(5))
                key.set_contents_from_string(body)
                # Remove the message from the queue
                queue.delete_message(message)
            # Finish the activity
            self.complete()
            return True
