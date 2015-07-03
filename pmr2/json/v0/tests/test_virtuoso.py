import unittest
import json
from cStringIO import StringIO

import zope.component

from Products.PloneTestCase import ptc

from pmr2.virtuoso.interfaces import IWorkspaceRDFInfo
from pmr2.virtuoso.testing.layer import PMR2_VIRTUOSO_INTEGRATION_LAYER
from pmr2.json.tests import base

try:
    from pmr2.json.v0 import virtuoso
    _virtuoso = True
except ImportError:
    _virtuoso = False


@unittest.skipUnless(_virtuoso, 'pmr2.virtuoso is unavailable')
class VirtuosoTestCase(unittest.TestCase):
    """
    Testing functionalities of forms that don't fit well into doctests.
    """

    layer = PMR2_VIRTUOSO_INTEGRATION_LAYER

    def test_base_render(self):
        request = base.TestRequest()
        context = self.layer['portal'].workspace['virtuoso_test']
        f = virtuoso.WorkspaceRDFInfoEditForm(context, request)
        results = json.loads(f())
        self.assertEqual(results["fields"].keys(), ['paths'])

    def test_workspace_rdf_edit_form_submit(self):
        context = self.layer['portal'].workspace['virtuoso_test']
        request = base.TestRequest(method='POST',
            stdin=StringIO('{"fields":{"paths":["simple.rdf"]},'
                '"actions":{"apply":1}}'))
        form = virtuoso.WorkspaceRDFInfoEditForm(context, request)
        result = json.loads(form())
        self.assertEqual(result['fields']['paths']['value'], ['simple.rdf'])
        rdfinfo = zope.component.getAdapter(context, IWorkspaceRDFInfo)

        self.assertEqual(rdfinfo.paths, ['simple.rdf'])


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(VirtuosoTestCase))
    return suite
