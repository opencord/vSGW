
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


from services.vsgw.models import *
from xosresource import XOSResource

class XOSVSGWTenant(XOSResource):
    provides = "tosca.nodes.VSGWTenant"
    xos_model = VSGWTenant
    name_field = "service_specific_id"
    copyin_props = ("tenant_message", "image_name")

    def get_xos_args(self, throw_exception=True):
        args = super(XOSVSGWTenant, self).get_xos_args()

        # ExampleTenant must always have a provider_service
        provider_name = self.get_requirement("tosca.relationships.MemberOfService", throw_exception=throw_exception)
        if provider_name:
            args["provider_service"] = self.get_xos_object(VSGWService, throw_exception=throw_exception, name=provider_name)

        return args

    def get_existing_objs(self):
        args = self.get_xos_args(throw_exception=False)
        return VSGWTenant.get_tenant_objects().filter(provider_service=args["provider_service"], service_specific_id=args["service_specific_id"])
        return []

    def can_delete(self, obj):
        return super(XOSVSGWTenant, self).can_delete(obj)

