# from services.vsgw.models import VSGWService
from service import XOSService
from services.vsgw.models import VSGWService

class XOSVSGWService(XOSService):
    provides = "tosca.nodes.VSGWService"
    xos_model = VSGWService
    copyin_props = ["view_url", "icon_url", "enabled", "published", "public_key", "private_key_fn", "versionNumber"]

