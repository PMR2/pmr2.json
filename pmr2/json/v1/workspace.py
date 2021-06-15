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

    @property
    def exposures(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        query = {}
        query['portal_type'] = 'Exposure'
        query['review_state'] = 'published'
        query['pmr2_exposure_workspace'] = [
            u'/'.join(self.context.getPhysicalPath()),
        ]
        query['sort_on'] = 'modified'
        query['sort_order'] = 'reverse'
        results = catalog(**query)
        return results

    @property
    def latest_exposure(self):
        exposures = self.exposures
        if exposures:
            return exposures[0]

    def update(self):
        links = []
        context_owner = self.context.getOwner()
        fullname = context_owner.getProperty('fullname', context_owner.getId())
        email = context_owner.getProperty('email', None)
        owner = fullname
        if email:
            owner += ' <%s>' % email

        latest_exposure = self.latest_exposure
        if latest_exposure:
            links.append({
                'rel': 'bookmark',
                'href': self.latest_exposure.getURL(),
                'prompt': 'Latest Exposure',
            })

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
                    'name': 'title',
                    'value': self.context.title,
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
            'links': links,
        }]


class JsonWorkspaceEditForm(JsonCollectionFormMixin,
        WorkspaceEditForm):
    pass
