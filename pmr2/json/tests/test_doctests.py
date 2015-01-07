import doctest
import unittest

from zope.component import testing
from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.PloneTestCase.layer import onsetup

from pmr2.app.workspace.tests.base import WorkspaceDocTestCase
from pmr2.app.exposure.tests.base import CompleteDocTestCase
from pmr2.json.tests import base


def test_suite():
    return unittest.TestSuite([

        ztc.ZopeDocFileSuite(
            'README.rst', package='pmr2.json',
            test_class=ptc.FunctionalTestCase,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
        ),

        ztc.ZopeDocFileSuite(
            'dashboard.rst', package='pmr2.json.v0',
            test_class=WorkspaceDocTestCase,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
        ),

        ztc.ZopeDocFileSuite(
            'dashboard.rst', package='pmr2.json',
            test_class=WorkspaceDocTestCase,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
        ),

        ztc.ZopeDocFileSuite(
            'document.rst', package='pmr2.json',
            test_class=ptc.FunctionalTestCase,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
        ),

        ztc.ZopeDocFileSuite(
            'exposure.rst', package='pmr2.json.v0',
            test_class=CompleteDocTestCase,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
        ),

        ztc.ZopeDocFileSuite(
            'workspace.rst', package='pmr2.json',
            test_class=WorkspaceDocTestCase,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
        ),

        ztc.ZopeDocFileSuite(
            'topic.rst', package='pmr2.json',
            test_class=ptc.FunctionalTestCase,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
        ),

    ])
