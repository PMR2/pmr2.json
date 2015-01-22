from lxml import etree
from lxml import html

from pmr2.json.collection.mixin import JsonCollectionPage


class ATCTDocumentJsonPage(JsonCollectionPage):

    json_mimetype = 'application/vnd.physiome.pmr2.json.1'

    def update(self):
        text = self.context.getText()
        tree = html.fragment_fromstring(text, create_parent=True)
        elements = tree.xpath('//*[@href]')

        self._jc_links = [
            {
                # XXX determine whether relation is the right one.
                # For the default one, 'section' might be better.
                'rel': 'bookmark',
                'href': el.get('href'),
                'label': el.text,
            }
            for el in elements
        ]

        href = '/'.join([self.context.absolute_url(), self.__name__])
        self._jc_href = href

        self._jc_items = [{
            'href': href,
            'data': [
                {
                    'name': 'contents',
                    'value': text,
                },
            ]
        }]
