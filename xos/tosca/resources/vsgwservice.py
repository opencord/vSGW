
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


from services.vsgw.models import VSGWService
from xosresource import XOSResource
from service import XOSService

class XOSVSGWService(XOSResource):
    provides = "tosca.nodes.VSGWService"
    xos_model = VSGWService
    copyin_props = ["view_url", "icon_url", "enabled", "published", "public_key", "private_key_fn", "versionNumber", "service_message"]

    def postprocess(self, obj):
        for provider_service_name in self.get_requirements("tosca.relationships.TenantOfService"):
            provider_service = self.get_xos_object(VSGWService, name=provider_service_name)

            existing_tenancy = CoarseTenant.get_tenant_objects().filter(provider_service = provider_service, subscriber_service = obj)
            if existing_tenancy:
                self.info("Tenancy relationship from %s to %s already exists" % (str(obj), str(provider_service)))
            else:
                tenancy = CoarseTenant(provider_service = provider_service,
                                       subscriber_service = obj)
                tenancy.save()

                self.info("Created Tenancy relationship  from %s to %s" % (str(obj), str(provider_service)))

    def can_delete(self, obj):
        if obj.slices.exists():
            self.info("Service %s has active slices; skipping delete" % obj.name)
            return False
        return super(XOSVSGWService, self).can_delete(obj)

