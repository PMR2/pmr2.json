import json

from Products.CMFCore.utils import getToolByName

from pmr2.app.workspace.browser.browser import WorkspaceStorageCreateForm
from pmr2.app.workspace.browser.browser import WorkspacePage
from pmr2.app.workspace.browser.browser import WorkspaceEditForm

from pmr2.json.mixin import SimpleJsonFormMixin, SimpleJsonAddFormMixin
from pmr2.json.mixin import JsonPage, JsonListingBasePage
from pmr2.json.collection.mixin import JsonCollectionFormMixin
from pmr2.json.collection.mixin import JsonCollectionAddFormMixin
from pmr2.json.collection.mixin import JsonCollectionPage


class JsonWorkspaceStorageCreateForm(JsonCollectionAddFormMixin,
        WorkspaceStorageCreateForm):
    pass


class JsonWorkspaceContainerList(JsonListingBasePage):
    portal_type = 'Workspace'


class JsonWorkspacePage(JsonCollectionPage, WorkspacePage):

    def update(self):
        context_owner = self.context.getOwner()
        fullname = context_owner.getProperty('fullname', context_owner.getId())
        email = context_owner.getProperty('email', None)
        owner = fullname
        if email:
            owner += ' <%s>' % email

        # TODO use the interface populating method if/when that is
        # implemented.

        self._jc_items = [{
            'href': self.context.absolute_url(),
            'data': [
                {
                    'name': 'id',
                    'value': self.context.id,
                },
                {
                    'name': 'owner',
                    'value': owner,
                },
                {
                    'name': 'description',
                    'value': self.context.description,
                },
                {
                    'name': 'storage',
                    'value': self.context.storage,
                },
            ],
            # TODO links to revision and exposures.
            'links': [],
        }]


class JsonWorkspaceEditForm(JsonCollectionFormMixin,
        WorkspaceEditForm):
    pass
