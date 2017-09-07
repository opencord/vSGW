from core.models.plcorebase import *
from models_decl import VSGWCService_decl
from models_decl import VSGWCVendor_decl
from models_decl import VSGWCTenant_decl

from django.db import models
from core.models import Service, PlCoreBase, Slice, Instance, Tenant, TenantWithContainer, Node, Image, User, Flavor, NetworkParameter, NetworkParameterType, Port, AddressPool
from core.models.plcorebase import StrippedCharField
import os
from django.db import models, transaction
from django.forms.models import model_to_dict
from django.db.models import *
from operator import itemgetter, attrgetter, methodcaller
from core.models import Tag
from core.models.service import LeastLoadedNodeScheduler
import traceback
from xos.exceptions import *
from xos.config import Config

class VSGWCService(VSGWCService_decl):
   class Meta:
        proxy = True 

   def create_tenant(self, **kwargs):
       t = VSGWCTenant(kind="vEPC", provider_service=self, connect_method="na", **kwargs)
       t.save()
       return t

class VSGWCVendor(VSGWCVendor_decl):
   class Meta:
        proxy = True

class VSGWCTenant(VSGWCTenant_decl):
   class Meta:
        proxy = True 
        
   def __init__(self, *args, **kwargs):
       vsgwcservice = VSGWCService.get_service_objects().all()
       if vsgwcservice:
           self._meta.get_field(
                   "provider_service").default = vsgwcservice[0].id
       super(VSGWCTenant, self).__init__(*args, **kwargs)

   @property
   def image(self):
       if not self.vsgwc_vendor:
           return super(VSGWCTenant, self).image
       return self.vsgwc_vendor.image
   
   def save_instance(self, instance):
       if self.vsgwc_vendor:
           instance.flavor = self.vsgwc_vendor.flavor
       super(VSGWCTenant, self).save_instance(instance)

   def save(self, *args, **kwargs):
       if not self.creator:
           if not getattr(self, "caller", None):
               raise XOSProgrammingError("VSGWCTenant's self.caller was not set")
           self.creator = self.caller
           if not self.creator:
               raise XOSProgrammingError("VSGWCTenant's self.creator was not set")

       super(VSGWCTenant, self).save(*args, **kwargs)
       # This call needs to happen so that an instance is created for this
       # tenant is created in the slice. One instance is created per tenant.
       model_policy_vsgwctenant(self.pk)

   def delete(self, *args, **kwargs):
       # Delete the instance that was created for this tenant
       self.cleanup_container()
       super(VSGWCTenant, self).delete(*args, **kwargs)

def model_policy_vsgwctenant(pk):
    # This section of code is atomic to prevent race conditions
    with transaction.atomic():
        # We find all of the tenants that are waiting to update
        tenant = VSGWCTenant.objects.select_for_update().filter(pk=pk)
        if not tenant:
            return
        # Since this code is atomic it is safe to always use the first tenant
        tenant = tenant[0]
        tenant.manage_container()

