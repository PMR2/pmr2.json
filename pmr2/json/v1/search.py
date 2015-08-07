from Products.CMFCore.utils import getToolByName

from pmr2.json.collection.mixin import JsonCollectionPage
from pmr2.json.mixin import extractRequestObj


class JsonSearchPage(JsonCollectionPage):

    valid_fields = ('SearchableText',)

    def _build_template(self):
        data = []
        for f in self.valid_fields:
            data.append({
                'name': f,
                'prompt': f,
                # 'description': f,
                'value': self.request.get(f, ''),
                # 'options': options,
            })
        return data

    def update(self):
        super(JsonSearchPage, self).update()
        query = extractRequestObj(self.request)
        if not query:
            # process this to collection items
            # self.results = self.catalog(**query)
            self.catalog = getToolByName(self.context, 'portal_catalog')
            self.results = []

        self._jc_template = self._build_template()
