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

    def fetch_pending(self, deleted):

        if (not deleted):
            objs = VSGWCTenant.get_tenant_objects().filter(
                Q(enacted__lt=F('updated')) | Q(enacted=None), Q(lazy_blocked=False))
        else:
            # If this is a deletion we get all of the deleted tenants..
            objs = VSGWCTenant.get_deleted_tenant_objects()

        return objs

    def get_extra_attributes(self, o):
        fields = {}
        fields['tenant_message'] = o.tenant_message
        return fields

