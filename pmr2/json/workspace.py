import json

from pmr2.json.mixin import SimpleJsonFormMixin, SimpleJsonAddFormMixin
from pmr2.app.workspace.browser.browser import WorkspaceStorageCreateForm
from pmr2.app.workspace.browser.browser import WorkspacePage

from pmr2.json.mixin import JsonPage


class JsonWorkspaceStorageCreateForm(SimpleJsonAddFormMixin,
        WorkspaceStorageCreateForm):
    pass


class JsonWorkspacePage(JsonPage, WorkspacePage):

    def render(self):
        obj = {
            'id': self.context.id,
            'url': self.context.absolute_url(),
            'description': self.context.description,
        }

        return json.dumps(obj)
