import unittest
import json
from cStringIO import StringIO

import zope.component
from Products.CMFCore.utils import getToolByName

from zope.publisher.browser import TestRequest
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.testing.z2 import Browser

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
        self.testbrowser = Browser(self.portal)

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

    def test_query(self):
        portal = self.portal

        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        portal.invokeFactory('News Item', 'testnews', title=u'Test News',
            subject=['Portal News'])
        portal.invokeFactory('Document', 'testpage', title=u'Test Page',
            text='This is a simple page')
        workflowTool = getToolByName(portal, 'portal_workflow')
        workflowTool.setDefaultChain("simple_publication_workflow")
        workflowTool.doActionFor(portal.testpage, 'publish')

        setRoles(portal, TEST_USER_ID, ['Member'])

        answer = {'collection': {
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
                    u'options': [{u'value': u'Portal News'}],
                },
                {
                    u'name': u'portal_type',
                    u'prompt': u'portal_type',
                    u'value': u'',
                    u'options': [
                        {u'value': u'Document'},
                        {u'value': u'News Item'}
                    ],
                },
            ],
        }}

        f = search.JsonSearchPage(self.portal, self.request)
        results = json.loads(f())
        self.assertEqual(results, answer)

        import transaction
        transaction.commit()

        answer['collection']['href'] = 'http://nohost/plone/search'

        self.testbrowser.addHeader('Accept',
            'application/vnd.physiome.pmr2.json.1')
        self.testbrowser.open('http://nohost/plone/search')
        self.assertEqual(json.loads(self.testbrowser.contents), answer)

        request = TestRequest()
        request.stdin = StringIO(json.dumps({'template': {
            'data': [
                {
                    'name': 'SearchableText',
                    'value': 'simple',
                }
            ]
        }}))
        f = search.JsonSearchPage(self.portal, request)
        results = json.loads(f())
        links = [{
            'href': u'http://nohost/plone/testpage',
            'prompt': u'Test Page',
            'rel': u'bookmark'
        }]
        self.assertEqual(results['collection']['links'], links)

        self.testbrowser.open('http://nohost/plone/search',
            data=request.stdin.getvalue())
        self.assertEqual(
            json.loads(self.testbrowser.contents)['collection']['links'],
            links)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(SearchTestCase))
    return suite
