import unittest
import json

from plone.testing.z2 import Browser

from pmr2.json.testing.layer import COLLECTION_JSON_LAYER


class PhysiomePmr2Json1VersioningTestCase(unittest.TestCase):
    """
    This set of test cases verifies the integration of the web services
    and the version it is supposed to provide for the Collection+JSON
    format (served with mimetype application/vnd.physiome.json.1).
    """

    layer = COLLECTION_JSON_LAYER

    def setUp(self):
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        self.testbrowser = Browser(self.layer['portal'])

    def tearDown(self):
        pass

    def test_base_render(self):
        self.testbrowser.open(self.portal_url + '/item_form')
        self.assertIn('<input', self.testbrowser.contents)

    def test_format_0_fail(self):
        self.testbrowser.addHeader('Accept',
            'application/vnd.physiome.pmr2.json.0')
        self.testbrowser.open(self.portal_url + '/item_form')
        # XXX The fallback behavior needs to be supported until all
        # forms have the .1 format implemented.
        # XXX uncomment below when ready.
        # self.assertRaises(ValueError, json.loads, self.testbrowser.contents)

    def test_format_0_base(self):
        self.testbrowser.addHeader('Accept',
            'application/vnd.physiome.pmr2.json.1')
        self.testbrowser.open(self.portal_url + '/item_form')
        results = json.loads(self.testbrowser.contents)
        self.assertTrue(isinstance(results, dict))
        self.assertEqual(self.testbrowser.headers['Content-Type'],
            'application/vnd.physiome.pmr2.json.1')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(PhysiomePmr2Json1VersioningTestCase))
    return suite
