from core.models.plcorebase import *
from models_decl import VSGWService_decl
from models_decl import VSGWTenant_decl

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
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class VSGWService(VSGWService_decl):
   class Meta:
        proxy = True 

class VSGWTenant(VSGWTenant_decl):
   class Meta:
        proxy = True 
        
   def __init__(self, *args, **kwargs):
       vsgwservice = VSGWService.get_service_objects().all()
       if vsgwservice:
           self._meta.get_field(
                   "provider_service").default = vsgwservice[0].id
       super(VSGWTenant, self).__init__(*args, **kwargs)

   def save(self, *args, **kwargs):
       super(VSGWTenant, self).save(*args, **kwargs)
       # This call needs to happen so that an instance is created for this
       # tenant is created in the slice. One instance is created per tenant.
       model_policy_vsgwtenant(self.pk)

   def delete(self, *args, **kwargs):
       # Delete the instance that was created for this tenant
       self.cleanup_container()
       super(VSGWTenant, self).delete(*args, **kwargs)

def model_policy_vsgwtenant(pk):
    # This section of code is atomic to prevent race conditions
    with transaction.atomic():
        # We find all of the tenants that are waiting to update
        tenant = VSGWTenant.objects.select_for_update().filter(pk=pk)
        if not tenant:
            return
        # Since this code is atomic it is safe to always use the first tenant
        tenant = tenant[0]
        tenant.manage_container()

