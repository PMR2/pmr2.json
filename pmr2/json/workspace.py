from pmr2.json.mixin import SimpleJsonFormMixin, SimpleJsonAddFormMixin
from pmr2.app.workspace.browser.browser import WorkspaceStorageCreateForm


class JsonWorkspaceStorageCreateForm(SimpleJsonAddFormMixin,
        WorkspaceStorageCreateForm):
    pass
