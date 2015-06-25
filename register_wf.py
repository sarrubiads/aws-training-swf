#!/usr/bin/env python

import boto.swf
import boto.swf.layer2 as swf
from boto.swf.exceptions import SWFTypeAlreadyExistsError
from boto.swf.exceptions import SWFDomainAlreadyExistsError

DOMAIN = 'btt-workflows'
VERSION = '1.0'

registerables = []
registerables.append(swf.Domain(name=DOMAIN))
registerables.append(swf.WorkflowType(domain=DOMAIN, name='notifications-wf',
                                      version=VERSION, task_list='default'))

registerables.append(swf.ActivityType(domain=DOMAIN, name='send-notifications',
                                      version=VERSION, task_list='default'))


for swf_entity in registerables:
    try:
        swf_entity.register()
        print swf_entity.name, 'registered successfully'
    except (SWFDomainAlreadyExistsError, SWFTypeAlreadyExistsError):
        print swf_entity.__class__.__name__, swf_entity.name, 'already exists'
