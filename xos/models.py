
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


# models.py -  vSGW Models

from core.models import Service, TenantWithContainer, Image
from django.db import models, transaction

MCORD_KIND = 'EPC'

SERVICE_NAME = 'vsgw'
SERVICE_NAME_VERBOSE = 'Virtual SGW Service'
SERVICE_NAME_VERBOSE_PLURAL = 'Virtual SGW Services'
TENANT_NAME_VERBOSE = 'Virtual SGW Tenant'
TENANT_NAME_VERBOSE_PLURAL = 'Virtual SGW Tenants'

class VSGWService(Service):

    KIND = SERVICE_NAME

    class Meta:
        proxy = True
        app_label = SERVICE_NAME
        verbose_name = SERVICE_NAME_VERBOSE

class VSGWTenant(TenantWithContainer):

    KIND = SERVICE_NAME

    class Meta:
        verbose_name = TENANT_NAME_VERBOSE

    tenant_message = models.CharField(max_length=254, help_text="Tenant Message to Display")
    image_name = models.CharField(max_length=254, help_text="Name of VM image")

    def __init__(self, *args, **kwargs):
        vsgw_service = VSGWService.get_service_objects().all()
        if vsgw_service:
            self._meta.get_field('provider_service').default = vsgw_service[0].id
        super(VSGWTenant, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        super(VSGWTenant, self).save(*args, **kwargs)
        model_policy_vsgwtenant(self.pk)

    def delete(self, *args, **kwargs):
        self.cleanup_container()
        super(VSGWTenant, self).delete(*args, **kwargs)

    @property
    def image(self):
        img = self.image_name.strip()
        if img.lower() != "default":
            return Image.objects.get(name=img)
        else: 
            return super(VSGWTenant, self).image

def model_policy_vsgwtenant(pk):
    with transaction.atomic():
        tenant = VSGWTenant.objects.select_for_update().filter(pk=pk)
        if not tenant:
            return
        tenant = tenant[0]
        tenant.manage_container()
