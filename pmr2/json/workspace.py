import json

from Products.CMFCore.utils import getToolByName

from pmr2.json.mixin import SimpleJsonFormMixin, SimpleJsonAddFormMixin
from pmr2.app.workspace.browser.browser import WorkspaceStorageCreateForm
from pmr2.app.workspace.browser.browser import WorkspacePage

from pmr2.json.mixin import JsonPage


class JsonWorkspaceStorageCreateForm(SimpleJsonAddFormMixin,
        WorkspaceStorageCreateForm):
    pass


class JsonWorkspaceContainerList(JsonPage):

    def render(self):
        workspace = self.context
        catalog = getToolByName(workspace, 'portal_catalog')

        query = {
            'portal_type': 'Workspace',
            'path': [
                u'/'.join(workspace.getPhysicalPath()),
            ],
            'sort_on': 'sortable_title',
        }
        results = catalog(**query)

        keys = ['title', 'target']
        values = [dict(zip(keys, (i.Title, i.getURL(),))) for i in results]
        return json.dumps(values)


class JsonWorkspacePage(JsonPage, WorkspacePage):

    def render(self):
        obj = {
            'id': self.context.id,
            'url': self.context.absolute_url(),
            'description': self.context.description,
        }

        return json.dumps(obj)
