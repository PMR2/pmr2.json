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

from pmr2.json.collection.mixin import JsonCollectionCatalogPage
from pmr2.json.collection.mixin import JsonCollectionFormMixin
from pmr2.json.collection.mixin import JsonCollectionPage


class JsonExposureWizardForm(JsonCollectionFormMixin, form.EditForm):

    fields = field.Fields(IExposureWizard)
    _doomed = False

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

    def update(self):
        result = super(JsonExposureWizardForm, self).update()
        # A rather hacky way to deal with the error message.
        if self._doomed:
            self._jc_error = {
                'title': 'Error',
                'code': 'error',
                'message': 'There were errors generating the exposure',
                'errors': [],
            }
        return result


class JsonExposureContainerList(JsonCollectionCatalogPage):
    portal_type = 'Exposure'


class JsonExposurePage(JsonCollectionCatalogPage):
    portal_type = 'ExposureFile'

    def update(self):
        super(JsonExposurePage, self).update()
        helper = zope.component.queryAdapter(self.context,
            IExposureSourceAdapter)

        if not helper:
            self._jc_error = {'error': 'could not acquire the workspace for '
                'this exposure.'}
            return False

        exposure, workspace, path = helper.source()
        self._jc_links.append({
            'rel': 'via',
            'href': workspace.absolute_url(),
            'prompt': 'Workspace URL',
        })

class JsonExposureFilePage(JsonCollectionPage):

    def update(self):
        helper = zope.component.queryAdapter(self.context,
            IExposureSourceAdapter)
        if not helper:
            # XXX should raise exception of some sort that hooks into
            # some error handling stack.
            self._jc_error = {'error': 'unable to adapt to exposure source'}
            return False

        exposure, workspace, path = helper.source()
        keys = ('source_uri', 'file_type', 'views',)

        source_uri = '%s/%s/%s/%s' % (workspace.absolute_url(),
            'rawfile', exposure.commit_id, path)

        self._jc_items = [{
            'href': self.context.absolute_url() + '/view',
            'data': [
                # TODO automate this via interface for simple case?
                {
                    'name': 'file_type',
                    'value': self.context.file_type,
                    'prompt': 'File type for this exposure',
                },
                {
                    'name': 'title',
                    'value': self.context.title,
                    'prompt': 'Title',
                },
            ],
            # it's for this thing...
            'links': [{
                'rel': 'via',
                'href': source_uri,
                'prompt': 'Source File'
            }]
        }]

        vocab = zope.component.getUtility(IVocabulary,
            name='pmr2.vocab.ExposureFileAnnotators')

        self._jc_links = [
            {
                'href': '/'.join([self.context.absolute_url(), v]),
                'rel': 'section',
                'prompt': vocab.getTerm(v).title,
            } for v in self.context.views
        ]
