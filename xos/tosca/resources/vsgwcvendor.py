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

from xosresource import XOSResource
from core.models import ServiceInstance
from services.vsgwc.models import VSGWCVendor

class XOSVSGWCVendor(XOSResource):
    provides = "tosca.nodes.VSGWCVendor"
    xos_model = VSGWCVendor
    name_field = None
    copyin_props = ( "name",)

    def get_xos_args(self, throw_exception=True):
        args = super(XOSVSGWCVendor, self).get_xos_args()

        tenant_name = self.get_requirement("tosca.relationships.VendorOfTenant", throw_exception=throw_exception)
        if tenant_name:
            args["provider_tenant"] = self.get_xos_object(ServiceInstance, throw_exception=throw_exception, name=tenant_name)

        return args

    def get_existing_objs(self):
        args = self.get_xos_args(throw_exception=False)
        provider_tenant = args.get("provider", None)
        if provider_tenant:
            return [ self.get_xos_object(provider_tenant=provider_tenant) ]
        return []

    def postprocess(self, obj):
        pass

    def can_delete(self, obj):
        return super(XOSVSGWCVendor, self).can_delete(obj)

