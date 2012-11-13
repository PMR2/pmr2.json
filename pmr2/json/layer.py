import zope.interface
from pmr2.layer.utility import ConditionalLayerApplierBase

from pmr2.json.interfaces import ISimpleJsonForm


class SimpleJsonFormLayerApplier(ConditionalLayerApplierBase):
    layer = ISimpleJsonForm
    def condition(self, request):
        # XXX This is very naive
        return 'application/vnd.physiome.pmr2.json.0' in request['HTTP_ACCEPT']

