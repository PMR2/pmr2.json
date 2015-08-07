import unittest
import json

import zope.component

from zope.publisher.browser import TestRequest

from pmr2.json.v1 import search
from pmr2.json.testing import layer


class SearchTestCase(unittest.TestCase):
    """
    Testing functionalities of forms that don't fit well into doctests.
    """

    layer = layer.COLLECTION_JSON_LAYER

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = TestRequest()

    def test_base_render(self):
        f = search.JsonSearchPage(self.portal, self.request)
        results = json.loads(f())
        self.assertEqual(results,  {'collection': {
            'version': '1.0',
            'template': [
                {
                    u'name': u'SearchableText',
                    u'prompt': u'SearchableText',
                    u'value': u''
                },
            ],
        }})


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(SearchTestCase))
    return suite
