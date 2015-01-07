import json

import zope.component
import z3c.form.interfaces
from z3c.form import button, field

from Products.CMFCore.utils import getToolByName

from pmr2.z3cform import form

from pmr2.app.exposure.interfaces import IExposureSourceAdapter
from pmr2.app.exposure.interfaces import IExposureWizard
from pmr2.app.exposure.browser import util
from pmr2.app.exposure.browser import wizard

from pmr2.json.mixin import JsonPage, JsonListingBasePage
from pmr2.json.mixin import SimpleJsonFormMixin, SimpleJsonAddFormMixin


class JsonExposureWizardForm(SimpleJsonFormMixin, form.EditForm):

    fields = field.Fields(IExposureWizard)

    # Stealing buttons and handlers from edit form and the real wizard
    # form and merge them together.  Omit the add file function as it is
    # meaningless in this context.
    buttons = wizard.ExposureWizardForm.buttons.omit('add_file')
    handlers = form.EditForm.handlers.copy()
    for k in buttons.keys():
        b = buttons[k]
        handlers.addHandler(
            b, wizard.ExposureWizardForm.handlers.getHandler(b))
    buttons += form.EditForm.buttons
    # Groups are not provided or handled here, but some wizard form
    # hanlding methods attempts to process this.
    groups = []

    def getContent(self):
        return zope.component.getAdapter(self.context, IExposureWizard)


class JsonExposureContainerList(JsonListingBasePage):
    portal_type = 'Exposure'


class JsonExposurePage(JsonPage):

    def update(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        query = {
            'portal_type': 'ExposureFile',
            'path': [
                u'/'.join(self.context.getPhysicalPath()),
            ],
            'sort_on': 'sortable_title',
        }
        results = catalog(**query)

        keys = ['Title', 'URI']
        result = [dict(zip(keys, (i.Title, i.getURL() + '/view',)))
            for i in results]
        self.obj = result

    def render(self):
        return self.dumps(self.obj)


class JsonExposureFilePage(JsonPage):

    def update(self):
        helper = zope.component.queryAdapter(self.context,
            IExposureSourceAdapter)
        if not helper:
            # XXX should raise exception of some sort that hooks into
            # some error handling stack.
            self.obj = {'error': 'unable to adapt to exposure source'}
            return False

        exposure, workspace, path = helper.source()
        keys = ('source_uri', 'file_type', 'views',)

        source_uri = '%s/%s/%s/%s' % (workspace.absolute_url(),
            'rawfile', exposure.commit_id, path)
        file_type = self.context.file_type
        views = dict([(v, '/'.join((self.context.absolute_url(), v)))
            for v in self.context.views])

        values = (source_uri, file_type, views,)
        result = dict(zip(keys, values))
        self.obj = result

    def render(self):
        return self.dumps(self.obj)
