# Copyright 2017-present Open Networking Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
from django.db.models import Q, F
from synchronizers.new_base.modelaccessor import *
from synchronizers.new_base.SyncInstanceUsingAnsible import SyncInstanceUsingAnsible

parentdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, parentdir)

class SyncVSGWCTenant(SyncInstanceUsingAnsible):
    provides = [VSGWCTenant]

    observes = VSGWCTenant

    requested_interval = 0

    template_name = "vsgwctenant_playbook.yaml"

    service_key_name = "/opt/xos/configurations/mcord/mcord_private_key"

    def __init__(self, *args, **kwargs):
        super(SyncVSGWCTenant, self).__init__(*args, **kwargs)

#    def fetch_pending(self, deleted):
#        if (not deleted):
#            objs = VSGWCTenant.get_tenant_objects().filter(
#                Q(enacted__lt=F('updated')) | Q(enacted=None), Q(lazy_blocked=False))
#        else:
#            # If this is a deletion we get all of the deleted tenants..
#            objs = VSGWCTenant.get_deleted_tenant_objects()
#
#        return objs

    # Gets the attributes that are used by the Ansible template but are not
    # part of the set of default attribtues.
    def get_extra_attributes(self, o):
        fields = {}
        shared_net_id = Network.objects.get(name='shared_network').id

	try:
            fields['sgwc_shared_ip'] = Port.objects.get(network_id=shared_net_id, instance_id=o.instance_id).ip
        except Exception:
            print '{} does not have an instance'.format(o.name)

        try:
            mme = TenantWithContainer.objects.get(provider_service_id=Service.objects.get(name='vmme').id, subscriber_tenant_id=o.subscriber_tenant_id)
            fields['mme_shared_ip'] = Port.objects.get(network_id=shared_net_id, instance_id=mme.instance_id).ip
	except Exception:
            print '{} does not have a VMME instance'.format(o.subscriber_tenant.name)

        try:
            sgwu = TenantWithContainer.objects.get(provider_service_id=Service.objects.get(name='vsgwu').id, subscriber_tenant_id=o.subscriber_tenant_id)
            fields['sgwu_shared_ip'] = Port.objects.get(network_id=shared_net_id, instance_id=sgwu.instance_id).ip
        except Exception:
            print '{} does not have a VSGWU instance'.format(o.subscriber_tenant.name)

        return fields
