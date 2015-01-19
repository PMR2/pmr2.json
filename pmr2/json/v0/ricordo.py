import json

from pmr2.ricordo.browser import form

from pmr2.json.mixin import JsonPage, SimpleJsonFormMixin


class QueryForm(SimpleJsonFormMixin, form.QueryForm):

    def render(self):
        if self._results:
            return json.dumps([{
                'label': v['label'],
                'label_src': v['label_src'],
                'items': [
                    {
                        'href': i['source'] or i['obj'].getURL(),
                        'title': i['obj'].Title or i['source'],
                        'value': i['value'],
                    } for i in v['items']
                ],
            } for v in self.results()])
        return super(QueryForm, self).render()
