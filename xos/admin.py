# admin.py - VSGW Django Admin

from core.admin import ReadOnlyAwareAdmin, SliceInline
from core.middleware import get_request
from core.models import User
from django import forms
from django.contrib import admin
from services.vsgw.models import *

class VSGWServiceForm(forms.ModelForm):

    class Meta:
        model = VSGWService
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(VSGWServiceForm, self).__init__(*args, **kwargs)

        if self.instance:
            self.fields['service_message'].initial = self.instance.service_message

    def save(self, commit=True):
        self.instance.service_message = self.cleaned_data.get('service_message')
        return super(VSGWServiceForm, self).save(commit=commit)

class VSGWServiceAdmin(ReadOnlyAwareAdmin):

    model = VSGWService
    verbose_name = SERVICE_NAME_VERBOSE
    verbose_name_plural = SERVICE_NAME_VERBOSE_PLURAL
    form = VSGWServiceForm
    inlines = [SliceInline]

    list_display = ('backend_status_icon', 'name', 'service_message', 'enabled')
    list_display_links = ('backend_status_icon', 'name', 'service_message' )

    fieldsets = [(None, {
        'fields': ['backend_status_text', 'name', 'enabled', 'versionNumber', 'service_message', 'description',],
        'classes':['suit-tab suit-tab-general',],
        })]

    readonly_fields = ('backend_status_text', )
    user_readonly_fields = ['name', 'enabled', 'versionNumber', 'description',]

    extracontext_registered_admins = True

    suit_form_tabs = (
        ('general', 'Example Service Details', ),
        ('slices', 'Slices',),
        )

    suit_form_includes = ((
        'top',
        'administration'),
        )

    def get_queryset(self, request):
        return ExampleService.get_service_objects_by_user(request.user)

admin.site.register(VSGWService, VSGWServiceAdmin)

class VSGWTenantForm(forms.ModelForm):

    class Meta:
        model = VSGWTenant
        fields = '__all__'

    creator = forms.ModelChoiceField(queryset=User.objects.all())

    def __init__(self, *args, **kwargs):
        super(VSGWTenantForm, self).__init__(*args, **kwargs)

        self.fields['kind'].widget.attrs['readonly'] = True
        self.fields['kind'].initial = SERVICE_NAME

        self.fields['provider_service'].queryset = VSGWService.get_service_objects().all()

        if self.instance:
            self.fields['creator'].initial = self.instance.creator
            self.fields['tenant_message'].initial = self.instance.tenant_message
            self.fields['image_name'].initial = self.instance.image_name

        if (not self.instance) or (not self.instance.pk):
            self.fields['creator'].initial = get_request().user
            if VSGWService.get_service_objects().exists():
                self.fields['provider_service'].initial = VSGWService.get_service_objects().all()[0]

    def save(self, commit=True):
        self.instance.creator = self.cleaned_data.get('creator')
        self.instance.tenant_message = self.cleaned_data.get('tenant_message')
        self.instance.image_name = self.cleaned_data.get('image_name')
        return super(VSGWTenantForm, self).save(commit=commit)


class VSGWTenantAdmin(ReadOnlyAwareAdmin):

    verbose_name = TENANT_NAME_VERBOSE
    verbose_name_plural = TENANT_NAME_VERBOSE_PLURAL

    list_display = ('id', 'backend_status_icon', 'instance', 'tenant_message', 'image_name')
    list_display_links = ('backend_status_icon', 'instance', 'tenant_message', 'id', 'image_name')

    fieldsets = [(None, {
        'fields': ['backend_status_text', 'kind', 'provider_service', 'instance', 'creator', 'tenant_message', 'image_name'],
        'classes': ['suit-tab suit-tab-general'],
        })]

    readonly_fields = ('backend_status_text', 'instance',)

    form = VSGWTenantForm

    suit_form_tabs = (('general', 'Details'),)

    def get_queryset(self, request):
        return VSGWTenant.get_tenant_objects_by_user(request.user)

admin.site.register(VSGWTenant, VSGWTenantAdmin)
