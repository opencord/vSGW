# models.py -  vSGW Models

SERVICE_NAME = 'vsgw'
SERVICE_NAME_VERBOSE = 'Virtual SGW Service'
SERVICE_NAME_VERBOSE_PLURAL = 'Virtual SGW Services'
TENANT_NAME_VERBOSE = 'Virtual SGW Tenant'
TENANT_NAME_VERBOSE_PLURAL = 'Virtual SGW Tenants'

class VSGWService(Service):

    KIND = SERVICE_NAME

    class Meta:
        app_label = SERVICE_NAME
        verbose_name = SERVICE_NAME_VERBOSE

    service_message = models.CharField(max_length=254, help_text="Service Message to Display")

class VSGWTenant(TenantWithContainer):

    KIND = SERVICE_NAME

    class Meta:
        verbose_name = TENANT_NAME_VERBOSE

    tenant_message = models.CharField(max_length=254, help_text="Tenant Message to Display")

    def __init__(self, *args, **kwargs):
        vsgw_service = VSGWService.get_service_objects().all()
        if vsgw_service:
            self._meta.get_field('provider_service').default = vsgw_service[0].id
        super(ExampleTenant, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        super(VSGWTenant, self).save(*args, **kwargs)
        model_policy_exampletenant(self.pk)

    def delete(self, *args, **kwargs):
        self.cleanup_container()
        super(VSGWTenant, self).delete(*args, **kwargs)


def model_policy_exampletenant(pk):
    with transaction.atomic():
        tenant = VSGWTenant.objects.select_for_update().filter(pk=pk)
        if not tenant:
            return
        tenant = tenant[0]
        tenant.manage_container()