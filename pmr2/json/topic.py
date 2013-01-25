import json

from Products.CMFCore.utils import getToolByName

from pmr2.json.mixin import SimpleJsonFormMixin, SimpleJsonAddFormMixin
from pmr2.json.mixin import JsonPage


class ATCTTopicJsonPage(JsonPage):

    def render(self):
        results = self.context.queryCatalog()
        keys = ['title', 'target']
        values = [dict(zip(keys, (i.Title, i.getURL(),))) for i in results]
        return json.dumps(values)
