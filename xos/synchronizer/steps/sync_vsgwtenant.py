import os
import sys
from django.db.models import Q, F
from services.vsgwservice.models import VSGWService, VSGWTenant
from synchronizers.base.SyncInstanceUsingAnsible import SyncInstanceUsingAnsible

parentdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, parentdir)

class SyncVSGWTenant(SyncInstanceUsingAnsible):

    provides = [VSGWTenant]

    observes = VSGWTenant

    requested_interval = 0

    template_name = "vsgwtenant_playbook.yaml"

    service_key_name = "/opt/xos/synchronizers/vsgwservice/vsgwservice_private_key"

    def __init__(self, *args, **kwargs):
        super(SyncVSGWTenant, self).__init__(*args, **kwargs)

    def fetch_pending(self, deleted):

        if (not deleted):
            objs = VSGWTenant.get_tenant_objects().filter(
                Q(enacted__lt=F('updated')) | Q(enacted=None), Q(lazy_blocked=False))
        else:
            # If this is a deletion we get all of the deleted tenants..
            objs = VSGWTenant.get_deleted_tenant_objects()

        return objs

    def get_exampleservice(self, o):
        if not o.provider_service:
            return None

        vsgwservice = VSGWService.get_service_objects().filter(id=o.provider_service.id)

        if not vsgwservice:
            return None

        return vsgwservice[0]

    # Gets the attributes that are used by the Ansible template but are not
    # part of the set of default attributes.
    def get_extra_attributes(self, o):
        fields = {}
        fields['tenant_message'] = o.tenant_message
        vsgwservice = self.get_vsgwservice(o)
        fields['service_message'] = vsgwservice.service_message
        return fields

