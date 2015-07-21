import json

import zope.component
from zope.schema.interfaces import IVocabulary

import z3c.form.interfaces
from z3c.form import button, field

from Products.CMFCore.utils import getToolByName

from pmr2.z3cform import form

from pmr2.app.exposure.interfaces import IExposureSourceAdapter
from pmr2.app.exposure.interfaces import IExposureWizard
from pmr2.app.exposure.browser import util
from pmr2.app.exposure.browser import wizard

from pmr2.json.collection.mixin import JsonCollectionItemCatalogPage
from pmr2.json.collection.mixin import JsonCollectionFormMixin
from pmr2.json.collection.mixin import JsonCollectionPage
from pmr2.json.collection.core import view_url


class JsonExposureContainerList(JsonCollectionItemCatalogPage):
    portal_type = 'Exposure'

    def update_jc(self, results):
        pt = getToolByName(self.context, 'portal_url')
        portal = pt.getPortalObject()
        portal_url = portal.absolute_url()
        portal_path = '/'.join(portal.getPhysicalPath())

        self._jc_items = []
        for i in results:
            item = {
                'href': view_url(self.context, i),
                'data': [{
                    'name': 'title',
                    'value': i.Title,
                    'prompt': 'Title',
                }],
            }
            item['links'] = [{
                'href': portal_url +
                    i.pmr2_exposure_workspace.replace(portal_path, ''),
                'rel': 'source',
                'prompt': 'Workspace',
            }]

            self._jc_items.append(item)


class JsonAllExposureContainerList(JsonExposureContainerList):
    """
    A version that list all exposures regardless of where it is.
    
    This works around how the production site si currently set up.
    """

    def make_query(self):
        return {
            'portal_type': self.portal_type,
            'sort_on': 'sortable_title',
            'pmr2_review_state': 'published',
        }
