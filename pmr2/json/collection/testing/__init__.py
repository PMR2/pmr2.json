from cStringIO import StringIO
from zope.interface import implementer

from z3c.form import testing

from pmr2.json.interfaces import ISimpleJsonLayer1


@implementer(ISimpleJsonLayer1)
class TestRequest(testing.TestRequest):

    def __init__(self, *a, **kw):
        self.stdin = kw.pop('stdin', StringIO())
        super(testing.TestRequest, self).__init__(*a, **kw)
        self.method = kw.pop('method', self.method)

    @property
    def REQUEST_METHOD(self):
        return self.method
