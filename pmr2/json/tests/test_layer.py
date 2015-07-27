import unittest

from pmr2.json import layer
from pmr2.json import v0
from pmr2.json import v1
from pmr2.json import v2


class LayerTestCase(unittest.TestCase):

    def setUp(self):
        self.request = {'HTTP_ACCEPT': 'text/html'}
        self.applier = layer.SimpleJsonLayerApplier()
        # A typical default browser request.
        self.browser_request = {'HTTP_ACCEPT': 'text/html,'
            'application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
        # XML primary request
        self.xml_request = {
            'HTTP_ACCEPT': 'application/json;q=0.9,application/xml'}

    def tearDown(self):
        pass

    def test_basic(self):
        result = self.applier(self.request)
        self.assertIsNone(result)

    def test_apply_v0(self):
        result = self.applier({'HTTP_ACCEPT':
            'application/vnd.physiome.pmr2.json.0'})
        self.assertEqual(result, v0.interfaces.IJsonLayer)

    def test_apply_v1(self):
        result = self.applier({'HTTP_ACCEPT':
            'application/vnd.physiome.pmr2.json.1'})
        self.assertEqual(result, v1.interfaces.IJsonLayer)

    def test_apply_v2(self):
        result = self.applier({'HTTP_ACCEPT':
            'application/vnd.physiome.pmr2.json.2'})
        self.assertEqual(result, v2.interfaces.IJsonLayer)

    def test_apply_v1_version2(self):
        result = self.applier({'HTTP_ACCEPT':
            'application/vnd.physiome.pmr2.json.1;version=2'})
        self.assertEqual(result, v2.interfaces.IJsonLayer)
        result = self.applier({'HTTP_ACCEPT':
            'application/json;q=0.1,'
            'application/vnd.physiome.pmr2.json.1;version=2'})
        self.assertEqual(result, v2.interfaces.IJsonLayer)

    def test_apply_json(self):
        result = self.applier({'HTTP_ACCEPT': 'application/json'})
        self.assertEqual(result, v1.interfaces.IJsonLayer)
        result = self.applier(
            {'HTTP_ACCEPT': 'application/vnd.collection+json'})
        self.assertEqual(result, v1.interfaces.IJsonLayer)

    def test_xml_prime(self):
        result = self.applier(self.xml_request)
        self.assertIsNone(result)
        result = self.applier(self.browser_request)
        self.assertIsNone(result)

    def test_apply_mix(self):
        result = self.applier({'HTTP_ACCEPT': 'application/json'})
        self.assertEqual(result, v1.interfaces.IJsonLayer)
        result = self.applier(
            {'HTTP_ACCEPT': 'application/vnd.collection+json'})
        self.assertEqual(result, v1.interfaces.IJsonLayer)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(LayerTestCase))
    return suite
