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

MCORD_KIND = 'RAN'

SERVICE_NAME = 'vsgw'
SERVICE_NAME_VERBOSE = 'Virtual SGW Service'
SERVICE_NAME_VERBOSE_PLURAL = 'Virtual SGW Services'
TENANT_NAME_VERBOSE = 'Virtual SGW Tenant'
TENANT_NAME_VERBOSE_PLURAL = 'Virtual SGW Tenants'