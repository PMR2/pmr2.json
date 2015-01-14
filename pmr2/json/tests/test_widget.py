import unittest
from zope.schema import List

from z3c.form.testing import setUp
from z3c.form.testing import setupFormDefaults
from z3c.form.testing import tearDown

from pmr2.json.widget import JsonListConverter


class JsonListConverterTestCase(unittest.TestCase):

    def setUp(self):
        setUp(self)
        setupFormDefaults()

    def tearDown(self):
        tearDown(self)

    def test_toWidgetValue(self):
        jlc = JsonListConverter(List(), None)
        self.assertEqual(jlc.toWidgetValue('test'), 'test')
        self.assertEqual(jlc.toWidgetValue(['test']), ['test'])

    def test_toFieldValue(self):
        jlc = JsonListConverter(List(missing_value=['nothing']), None)
        self.assertEqual(jlc.toFieldValue('test'), ['nothing'])
        self.assertEqual(jlc.toFieldValue(['test']), ['test'])


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(JsonListConverterTestCase))
    return suite
