# from services.vsgwc.models import VSGWService
from service import XOSService
from services.vsgwc.models import VSGWCService

class XOSVSGWCService(XOSService):
    provides = "tosca.nodes.VSGWCService"
    xos_model = VSGWCService
    copyin_props = ["view_url", "icon_url", "enabled", "published", "public_key", "private_key_fn", "versionNumber"]

