import unittest
from zope.schema import List

from pmr2.json import http


class AcceptHeaderTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_basic(self):
        self.assertEqual(http.parse_accept(
            'text/plain'
        ), [
            ('text/plain', '1', {}),
        ])

    def test_14_1_audio(self):
        # RFC2616 14.1, audio example
        self.assertEqual(http.parse_accept(
            'audio/*; q=0.2, audio/basic'
        ), [
            ('audio/basic', '1', {}),
            ('audio/*', '0.2', {}),
        ])

    def test_14_1_text_elaborate(self):
        # RFC2616 14.1, elaborate text example
        self.assertEqual(http.parse_accept(
            'text/plain; q=0.5, text/html, text/x-dvi; q=0.8, text/x-c'
        ), [
            ('text/html', '1', {}),
            ('text/x-c', '1', {}),
            ('text/x-dvi', '0.8', {}),
            ('text/plain', '0.5', {}),
        ])

    def test_14_1_text_media_range(self):
        # RFC2616 14.1, media range example.
        self.assertEqual(http.parse_accept(
            'text/*, text/html, text/html;level=1, */*'
        ), [
            ('text/html', '1', {'level': '1'}),
            ('text/html', '1', {}),
            ('text/*', '1', {}),
            ('*/*', '1', {}),
        ])

    def test_14_1_mix_final(self):
        # RFC2616 14.1, final mixture example
        self.assertEqual(http.parse_accept(
            'text/*;q=0.3, text/html;q=0.7, text/html;level=1,'
            'text/html;level=2;q=0.4, */*;q=0.5'
        ), [
            ('text/html', '1', {'level': '1'}),
            ('text/html', '0.7', {}),
            ('*/*', '0.5', {}),
            ('text/html', '0.4', {'level': '2'}),
            ('text/*', '0.3', {}),
        ])


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(AcceptHeaderTestCase))
    return suite
