from Products.CMFCore.utils import getToolByName

from pmr2.json.collection.mixin import JsonCollectionCatalogBase
from pmr2.json.collection.core import request_template_to_dict


def index_values(catalog, name, **kw):
    return [{
        "value": value
    } for value in catalog._catalog.getIndex(name).uniqueValues()]


class JsonSearchPage(JsonCollectionCatalogBase):

    valid_fields = (
        'SearchableText', 'Title', 'Description', 'Subject', 'portal_type',
    )
    # associated functions to resolve the choices in these fields.
    choice_fields = {
        'portal_type': index_values,
        'Subject': index_values,
    }

    def _build_template(self):
        data = []
        for field_name in self.valid_fields:
            item = {
                'name': field_name,
                'prompt': field_name,
                # 'description': f,
                'value': self.request.get(field_name, ''),
                # 'options': options,
            }
            f_options = self.choice_fields.get(field_name)
            if f_options:
                item['options'] = f_options(self._catalog, field_name)
            data.append(item)
        return data

    def update(self):
        super(JsonSearchPage, self).update()
        self._jc_template = self._build_template()

    def make_query(self):
        return request_template_to_dict(self.request)
