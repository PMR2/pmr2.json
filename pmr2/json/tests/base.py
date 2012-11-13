from cStringIO import StringIO

from Zope2.App import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
from Products.PloneTestCase.layer import onteardown

from pmr2.testing import base


@onsetup
def setup():
    import pmr2.json
    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', pmr2.json)
    zcml.load_config('testing.zcml', pmr2.json.tests)
    fiveconfigure.debug_mode = False

@onteardown
def teardown():
    pass

setup()
teardown()
ptc.setupPloneSite()


class TestRequest(base.TestRequest):

    def __init__(self, *a, **kw):
        self.stdin = kw.pop('stdin', StringIO())
        super(TestRequest, self).__init__(*a, **kw)
        self.method = kw.pop('method', self.method)


class TestCase(ptc.PloneTestCase):
    pass
