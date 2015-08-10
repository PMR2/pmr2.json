import unittest
import json

import zope.component
from Products.CMFCore.utils import getToolByName

from zope.publisher.browser import TestRequest
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME

from pmr2.json.v1 import search
from pmr2.json.testing import layer


class SearchTestCase(unittest.TestCase):
    """
    Testing functionalities of forms that don't fit well into doctests.
    """

    layer = layer.COLLECTION_JSON_LAYER
    maxDiff = 10000

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
                    u'value': u'',
                },
                {
                    u'name': u'Title',
                    u'prompt': u'Title',
                    u'value': u'',
                },
                {
                    u'name': u'Description',
                    u'prompt': u'Description',
                    u'value': u'',
                },
                {
                    u'name': u'Subject',
                    u'prompt': u'Subject',
                    u'value': u'',
                    u'options': [],
                },
                {
                    u'name': u'portal_type',
                    u'prompt': u'portal_type',
                    u'value': u'',
                    u'options': [],
                },
            ],
        }})

    def test_options(self):
        portal = self.portal

        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        portal.invokeFactory('Document', 'testpage', title=u'Test Page')
        workflowTool = getToolByName(portal, 'portal_workflow')
        workflowTool.setDefaultChain("simple_publication_workflow")
        workflowTool.doActionFor(portal.testpage, 'publish')

        setRoles(portal, TEST_USER_ID, ['Member'])

        f = search.JsonSearchPage(self.portal, self.request)
        results = json.loads(f())
        self.assertEqual(results,  {'collection': {
            'version': '1.0',
            'template': [
                {
                    u'name': u'SearchableText',
                    u'prompt': u'SearchableText',
                    u'value': u'',
                },
                {
                    u'name': u'Title',
                    u'prompt': u'Title',
                    u'value': u'',
                },
                {
                    u'name': u'Description',
                    u'prompt': u'Description',
                    u'value': u'',
                },
                {
                    u'name': u'Subject',
                    u'prompt': u'Subject',
                    u'value': u'',
                    u'options': [],
                },
                {
                    u'name': u'portal_type',
                    u'prompt': u'portal_type',
                    u'value': u'',
                    u'options': [{u'value': u'Document'}],
                },
            ],
        }})


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(SearchTestCase))
    return suite
