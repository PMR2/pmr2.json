import json

from pmr2.virtuoso.browser import workspace

from pmr2.json.mixin import JsonPage, SimpleJsonFormMixin


class WorkspaceRDFInfoEditForm(SimpleJsonFormMixin,
        workspace.WorkspaceRDFInfoEditForm):
    pass
