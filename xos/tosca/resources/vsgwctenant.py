from xosresource import XOSResource
from core.models import Service, Tenant
from services.vsgwc.models import VSGWCTenant

class XOSVSGWCTenant(XOSResource):
    provides = "tosca.nodes.VSGWCTenant"
    xos_model = VSGWCTenant
    name_field = "service_specific_id"
    copyin_props = ()

    def get_xos_args(self, throw_exception=True):
        args = super(XOSVSGWCTenant, self).get_xos_args()

        # ExampleTenant must always have a provider_service
        provider_name = self.get_requirement("tosca.relationships.TenantOfService", throw_exception=throw_exception)
        if provider_name:
            args["provider_service"] = self.get_xos_object(Service, throw_exception=throw_exception, name=provider_name)

        return args

    def get_existing_objs(self):
        args = self.get_xos_args(throw_exception=False)
        return VSGWCTenant.get_tenant_objects().filter(provider_service=args["provider_service"], service_specific_id=args["service_specific_id"])
        return []

    def can_delete(self, obj):
        return super(XOSVSGWCTenant, self).can_delete(obj)

