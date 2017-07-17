# from services.vsgw.models import *
from synchronizers.new_base.modelaccessor import *
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

