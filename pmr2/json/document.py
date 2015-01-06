from lxml import etree
from lxml import html

from pmr2.json.mixin import JsonPage
from pmr2.json.hal.core import generate_hal


class ATCTDocumentJsonPage(JsonPage):

    json_mimetype = 'application/vnd.physiome.pmr2.json.1'

    def render(self):
        text = self.context.getText()
        tree = html.fragment_fromstring(text, create_parent=True)
        elements = tree.xpath('//*[@href]')

        links = [{
            'href': el.get('href'),
            'label': el.text,
        } for el in elements]

        data = {
            'contents': text,
        }

        return self.dumps(generate_hal(links, data=data))
