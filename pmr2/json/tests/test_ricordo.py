import unittest
import json

import zope.component

from Products.PloneTestCase import ptc

from pmr2.json.tests import base

try:
    from pmr2.json import ricordo
    _ricordo = True
except ImportError:
    _ricordo = False


@unittest.skipUnless(_ricordo, 'pmr2.ricordo is unavailable')
class RicordoTestCase(ptc.PloneTestCase):
    """
    Testing functionalities of forms that don't fit well into doctests.
    """

    def afterSetUp(self):
        pass

    def test_base_render(self):
        request = base.TestRequest()
        f = ricordo.QueryForm(self.portal, request)
        results = json.loads(f())
        self.assertEqual(results["actions"], {"search": {"title": "Search"}})


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(RicordoTestCase))
    return suite
