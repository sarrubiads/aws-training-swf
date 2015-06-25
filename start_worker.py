#!/usr/bin/env python

import send_notifications

while send_notifications.NotificationWorker().run():
    pass
