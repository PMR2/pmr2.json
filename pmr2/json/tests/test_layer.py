import unittest

from pmr2.json import layer
from pmr2.json import v0
from pmr2.json import v1
from pmr2.json import v2

from zope.publisher.browser import TestRequest


def make_request(d):
    return TestRequest(**d)


class LayerTestCase(unittest.TestCase):

    def setUp(self):
        self.request = TestRequest(HTTP_ACCEPT='text/html')
        self.applier = layer.SimpleJsonLayerApplier()
        # A typical default browser request.
        self.browser_request = TestRequest(HTTP_ACCEPT='text/html,'
            'application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        # XML primary request
        self.xml_request = TestRequest(
            HTTP_ACCEPT='application/json;q=0.9,application/xml')

    def tearDown(self):
        pass

    def test_basic(self):
        result = self.applier(self.request)
        self.assertIsNone(result)

    def test_apply_v0(self):
        request = make_request({'HTTP_ACCEPT':
            'application/vnd.physiome.pmr2.json.0'})
        result = self.applier(request)
        self.assertEqual(result, v0.interfaces.IJsonLayer)
        self.assertEqual(request._pmr2_json_layer_content_type_,
            'application/vnd.physiome.pmr2.json.0')

    def test_apply_v1(self):
        request = make_request({'HTTP_ACCEPT':
            'application/vnd.physiome.pmr2.json.1'})
        result = self.applier(request)
        self.assertEqual(result, v1.interfaces.IJsonLayer)
        self.assertEqual(request._pmr2_json_layer_content_type_,
            'application/vnd.physiome.pmr2.json.1')

    def test_apply_v2(self):
        # XXX to be removed
        request = make_request({'HTTP_ACCEPT':
            'application/vnd.physiome.pmr2.json.2'})
        result = self.applier(request)
        self.assertEqual(result, v2.interfaces.IJsonLayer)
        self.assertEqual(request._pmr2_json_layer_content_type_,
            'application/vnd.physiome.pmr2.json.2')

    def test_apply_v1_version2(self):
        request = make_request({'HTTP_ACCEPT':
            'application/vnd.physiome.pmr2.json.1;version=2'})
        result = self.applier(request)
        self.assertEqual(result, v2.interfaces.IJsonLayer)
        self.assertEqual(request._pmr2_json_layer_content_type_,
            'application/vnd.physiome.pmr2.json.1; version=2')

        request = make_request({'HTTP_ACCEPT':
            'application/json;q=0.1,'
            'application/vnd.physiome.pmr2.json.1;version=2'})
        result = self.applier(request)
        self.assertEqual(result, v2.interfaces.IJsonLayer)
        self.assertEqual(request._pmr2_json_layer_content_type_,
            'application/vnd.physiome.pmr2.json.1; version=2')

    def test_apply_v1_version3(self):
        request = make_request({'HTTP_ACCEPT':
            'application/vnd.physiome.pmr2.json.1;version=3'})
        result = self.applier(request)
        self.assertNotEqual(result, v2.interfaces.IJsonLayer)
        self.assertFalse(hasattr(request, '_pmr2_json_layer_content_type_'))
        self.assertEqual(request.response.getStatus(), 406)

    def test_apply_v1_version3_fallback(self):
        request = make_request({'HTTP_ACCEPT':
            'application/vnd.physiome.pmr2.json.1;version=3,'
            'application/vnd.physiome.pmr2.json.1;version=2;q=0.9'
            })
        result = self.applier(request)
        self.assertEqual(result, v2.interfaces.IJsonLayer)
        self.assertEqual(request._pmr2_json_layer_content_type_,
            'application/vnd.physiome.pmr2.json.1; version=2')

    def test_apply_json(self):
        request = make_request(
            {'HTTP_ACCEPT': 'application/json'})
        result = self.applier(request)
        self.assertEqual(result, v1.interfaces.IJsonLayer)
        self.assertEqual(request._pmr2_json_layer_content_type_,
            'application/json')
        request = make_request(
            {'HTTP_ACCEPT': 'application/vnd.collection+json'})
        result = self.applier(request)
        self.assertEqual(result, v1.interfaces.IJsonLayer)
        self.assertEqual(request._pmr2_json_layer_content_type_,
            'application/vnd.collection+json')

    def test_xml_prime(self):
        result = self.applier(self.xml_request)
        self.assertIsNone(result)
        result = self.applier(self.browser_request)
        self.assertIsNone(result)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(LayerTestCase))
    return suite
