import zope.interface
from pmr2.layer.utility import ConditionalLayerApplierBase

from pmr2.json.interfaces import ISimpleJsonLayer
from pmr2.json.interfaces import ISimpleJsonLayer1

# ordered in precedence.

layer_table = (
    ('application/vnd.physiome.pmr2.json.1', ISimpleJsonLayer1),
    ('application/vnd.physiome.pmr2.json.0', ISimpleJsonLayer),

    # This is the default, fallback one onto the latest version.
    ('application/json', ISimpleJsonLayer1),
)


class SimpleJsonLayerApplier(ConditionalLayerApplierBase):

    def condition(self, request):
        # XXX This is still very naive
        for mt, layer in layer_table:
            if mt in request['HTTP_ACCEPT']:
                return layer
        return None

    def __call__(self, request):
        try:
            result = self.condition(request)
        except:
            return

        return result
