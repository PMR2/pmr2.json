import json

import zope.component
from zope.schema.interfaces import IVocabulary
from zope.schema.interfaces import IVocabularyFactory

import z3c.form.interfaces
from z3c.form import button, field

from Products.CMFCore.utils import getToolByName

from pmr2.z3cform import form

from pmr2.app.annotation.interfaces import IExposureNoteTarget
from pmr2.app.exposure.interfaces import IExposureSourceAdapter
from pmr2.app.exposure.interfaces import IExposureWizard
from pmr2.app.exposure.browser import util
from pmr2.app.exposure.browser import wizard
from pmr2.app.exposure.browser.browser import ExposureFileTypeDisplayForm

from pmr2.json.collection.mixin import JsonCollectionCatalogPage
from pmr2.json.collection.mixin import JsonCollectionFormMixin
from pmr2.json.collection.mixin import JsonCollectionViewFormMixin
from pmr2.json.collection.mixin import JsonCollectionPage


# While the main version
# from pmr2.app.annotation.factory import default_note_url
# will do, there may be need to customize it here, especially for the
# removal of the `@@`.

def default_note_url(context):
    def default_url(view):
        return '%s/%s' % (context.absolute_url(), view)
    return default_url


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


class JsonExposureFileTypeView(JsonCollectionViewFormMixin,
        ExposureFileTypeDisplayForm):
    pass


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
        # since the parent class adds the context to the first item,
        # extend it with the additional fields.
        # TODO it will be better to establish the way to acquire the
        # required attributes by some attribute on the parent view class
        self._jc_items[0]['data'].append({
            'name': 'commit_id',
            'value': self.context.commit_id,
            'prompt': 'Changeset',
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

        file_type = self.context.file_type

        vocab_factory = zope.component.queryUtility(IVocabularyFactory,
            name='pmr2.vocab.eftype_uri')
        if vocab_factory:
            try:
                term = vocab_factory(self.context).getTerm(file_type)
                file_type = term.token
            except:
                pass

        source_uri = '%s/%s/%s/%s' % (workspace.absolute_url(),
            'rawfile', exposure.commit_id, path)

        self._jc_items = [{
            'href': self.context.absolute_url() + '/view',
            'data': [
                # TODO automate this via interface for simple case?
                {
                    'name': 'file_type',
                    'value': file_type,
                    'prompt': 'File type for this exposure',
                },
                {
                    'name': 'title',
                    'value': self.context.title,
                    'prompt': 'Title',
                },
                {
                    'name': 'commit_id',
                    'value': exposure.commit_id,
                    'prompt': 'Changeset',
                }
            ],
            # it's for this thing...
            'links': [{
                'rel': 'via',
                'href': source_uri,
                'prompt': 'Source File'
            }, {
                'rel': 'via',
                'href': workspace.absolute_url(),
                'prompt': 'Workspace URL',
            }]
        }]

        vocab = zope.component.getUtility(IVocabulary,
            name='pmr2.vocab.ExposureFileAnnotators')

        self._jc_links = [
            {
                'href': zope.component.queryAdapter(
                    self.context, IExposureNoteTarget, name=v,
                    default=default_note_url(self.context))(v),

                'rel': 'section',
                'prompt': vocab.getTerm(v).title,
            } for v in self.context.views
        ]
