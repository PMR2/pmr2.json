from pmr2.json.mixin import SimpleJsonFormMixin, SimpleJsonAddFormMixin
from pmr2.json.mixin import JsonPage

from pmr2.json.hal.core import generate_hal


class ATCTTopicJsonPage(JsonPage):

    def render(self):
        results = self.context.queryCatalog()
        links = [{
            'href': i.getURL(),
            'label': i.Title,
        } for i in results]

        return self.dumps(generate_hal(links))
