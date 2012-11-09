import doctest
import unittest

from zope.component import testing
from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.PloneTestCase.layer import onsetup

from pmr2.json.tests import base


def test_suite():
    return unittest.TestSuite([

        ztc.ZopeDocFileSuite(
            'README.rst', package='pmr2.json',
            test_class=ptc.FunctionalTestCase,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
        ),

    ])
