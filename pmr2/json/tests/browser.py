import json

from pmr2.app.exposure.browser.browser import ExposureFileViewBase

from pmr2.json.mixin import JsonPage


class JsonFilenameNote(ExposureFileViewBase, JsonPage):

    def update(self):
        self.obj = {'filename': self.note.filename}

    def render(self):
        return self.dumps(self.obj)
