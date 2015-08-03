import unittest
import json
from urllib2 import HTTPError

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
        self.testbrowser.open(self.portal_url + '/item_form_html_only')
        self.assertIn('<input', self.testbrowser.contents)

    def test_assigned_but_html_only(self):
        self.testbrowser.addHeader('Accept',
            'application/vnd.physiome.pmr2.json.1')
        self.testbrowser.open(self.portal_url + '/item_form_html_only')
        self.assertIn('<input', self.testbrowser.contents)
        self.assertTrue(self.testbrowser.headers['Content-Type'].startswith(
            'text/html'))

    def test_format_0_fail(self):
        self.testbrowser.addHeader('Accept',
            'application/vnd.physiome.pmr2.json.0')
        self.testbrowser.open(self.portal_url + '/item_form')
        self.assertRaises(ValueError, json.loads, self.testbrowser.contents)

    def test_format_0_unassigned(self):
        self.testbrowser.open(self.portal_url + '/page_v0_only')
        results = json.loads(self.testbrowser.contents)
        self.assertTrue(isinstance(results, dict))
        self.assertEqual(self.testbrowser.headers['Content-Type'],
            'application/vnd.physiome.pmr2.json.0')

    def test_format_0_assigned(self):
        self.testbrowser.addHeader('Accept',
            'application/vnd.physiome.pmr2.json.0')
        self.testbrowser.open(self.portal_url + '/page_v0_only')
        results = json.loads(self.testbrowser.contents)
        self.assertTrue(isinstance(results, dict))
        self.assertEqual(self.testbrowser.headers['Content-Type'],
            'application/vnd.physiome.pmr2.json.0')

    def test_format_0_only_view_requested_as_1_fail(self):
        self.testbrowser.addHeader('Accept',
            'application/vnd.physiome.pmr2.json.1')
        self.assertRaises(HTTPError,
            self.testbrowser.open, self.portal_url + '/page_v0_only')

    def test_format_0_mix_view_request_as_0_success_attempt(self):
        self.testbrowser.addHeader('Accept',
            'application/vnd.physiome.pmr2.json.0')
        self.testbrowser.open(self.portal_url + '/page_v0_mix')
        results = json.loads(self.testbrowser.contents)
        self.assertTrue(isinstance(results, dict))
        self.assertEqual(self.testbrowser.headers['Content-Type'],
            'application/vnd.physiome.pmr2.json.0')

    def test_format_0_request_as_1_fail_attempt(self):
        self.testbrowser.addHeader('Accept',
            'application/vnd.physiome.pmr2.json.1')
        #self.testbrowser.open(self.portal_url + '/page_v0_mix')
        #import pdb;pdb.set_trace()
        self.assertRaises(HTTPError,
            self.testbrowser.open, self.portal_url + '/page_v0_only')

    def test_format_0_request_as_1_and_0_success(self):
        self.testbrowser.addHeader('Accept',
            'application/vnd.physiome.pmr2.json.0,'
            'application/vnd.physiome.pmr2.json.1')
        self.testbrowser.open(self.portal_url + '/page_v0_mix')
        results = json.loads(self.testbrowser.contents)
        self.assertTrue(isinstance(results, dict))
        self.assertEqual(self.testbrowser.headers['Content-Type'],
            'application/vnd.physiome.pmr2.json.0')

    def test_format_0_request_as_1_and_0_success_reversed(self):
        self.testbrowser.addHeader('Accept',
            'application/vnd.physiome.pmr2.json.1,'
            'application/vnd.physiome.pmr2.json.0')
        self.testbrowser.open(self.portal_url + '/page_v0_mix')
        results = json.loads(self.testbrowser.contents)
        self.assertTrue(isinstance(results, dict))
        self.assertEqual(self.testbrowser.headers['Content-Type'],
            'application/vnd.physiome.pmr2.json.0')

    def test_format_1_base(self):
        self.testbrowser.addHeader('Accept',
            'application/vnd.physiome.pmr2.json.1')
        self.testbrowser.open(self.portal_url + '/item_form')
        results = json.loads(self.testbrowser.contents)
        self.assertTrue(isinstance(results, dict))
        self.assertEqual(self.testbrowser.headers['Content-Type'],
            'application/vnd.physiome.pmr2.json.1')

    def test_format_1_base_as_json(self):
        self.testbrowser.addHeader('Accept', 'application/json')
        self.testbrowser.open(self.portal_url + '/item_form')
        results = json.loads(self.testbrowser.contents)
        self.assertTrue(isinstance(results, dict))
        self.assertEqual(self.testbrowser.headers['Content-Type'],
            'application/json')

    def test_format_1_version1(self):
        self.testbrowser.addHeader('Accept',
            'application/vnd.physiome.pmr2.json.1; version=1')
        self.testbrowser.open(self.portal_url + '/item_form')
        results = json.loads(self.testbrowser.contents)
        self.assertTrue(isinstance(results, dict))
        self.assertEqual(self.testbrowser.headers['Content-Type'],
            'application/vnd.physiome.pmr2.json.1; version=1')

    def test_format_1_version2(self):
        self.testbrowser.addHeader('Accept',
            'application/vnd.physiome.pmr2.json.1; version=2')
        self.testbrowser.open(self.portal_url + '/item_form')
        results = json.loads(self.testbrowser.contents)
        self.assertTrue(isinstance(results, dict))
        self.assertEqual(self.testbrowser.headers['Content-Type'],
            'application/vnd.physiome.pmr2.json.1; version=2')

    def test_format_1_version3(self):
        self.testbrowser.addHeader('Accept',
            'application/vnd.physiome.pmr2.json.1; version=3')
        self.assertRaises(HTTPError,
            self.testbrowser.open, self.portal_url + '/item_form')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(PhysiomePmr2Json1VersioningTestCase))
    return suite
