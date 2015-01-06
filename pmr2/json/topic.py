from pmr2.json.mixin import SimpleJsonFormMixin, SimpleJsonAddFormMixin
from pmr2.json.mixin import JsonPage

from pmr2.json.hal.core import generate_hal


class ATCTTopicJsonPage(JsonPage):

    def render(self):
        siteprop = self.context.portal_properties.site_properties
        use_view_action = getattr(siteprop, 'typesUseViewActionInListings', ())

        def view_url(item):
            if item.portal_type in use_view_action:
                return item.getURL() + '/view'
            return item.getURL()

        results = self.context.queryCatalog()
        links = [{
            'href': view_url(i),
            'label': i.Title,
        } for i in results]

        return self.dumps(generate_hal(links))
