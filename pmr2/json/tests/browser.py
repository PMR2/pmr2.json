import json

from pmr2.app.exposure.browser.browser import ExposureFileViewBase

from pmr2.json.mixin import JsonPage
from pmr2.json.collection.mixin import JsonCollectionPage


class JsonFilenameNote(ExposureFileViewBase, JsonPage):

    def update(self):
        self.obj = {'filename': self.note.filename}

    def render(self):
        return self.dumps(self.obj)


class JsonCollectionFilenameNote(ExposureFileViewBase, JsonCollectionPage):

    def update(self):
        self._jc_items = [{'name': 'filename', 'value': self.note.filename}]
