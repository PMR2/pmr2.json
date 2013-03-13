from Products.CMFCore.utils import getToolByName

from pmr2.json.mixin import JsonPage
from pmr2.json.mixin import extractRequestObj


class JsonSearchPage(JsonPage):

    def update(self):
        query = extractRequestObj(self.request)
        if not query:
            self.results = []
            return

        self.catalog = getToolByName(self.context, 'portal_catalog')
        self.results = self.catalog(**query)

    def render(self):
        results = self.results
        keys = ['title', 'target']
        values = [dict(zip(keys, (i.Title, i.getURL(),))) for i in results]
        return self.dumps(values)
