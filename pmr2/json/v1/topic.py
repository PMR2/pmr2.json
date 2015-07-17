from pmr2.json.mixin import SimpleJsonFormMixin, SimpleJsonAddFormMixin
from pmr2.json.mixin import JsonPage

from pmr2.json.collection.mixin import JsonCollectionPage
from pmr2.json.collection.core import view_url


class ATCTTopicJsonPage(JsonCollectionPage):

    def update(self):
        results = self.context.queryCatalog()
        self._jc_links = [
            {
                # XXX determine whether relation is the right one.
                # For the default one, 'section' might be better.
                'rel': 'bookmark',
                'href': view_url(self.context, i),
                'prompt': i.Title,
            }
            for i in results
        ]

        href = '/'.join([self.context.absolute_url(), self.__name__])
        self._jc_href = href
