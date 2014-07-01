import json

from pmr2.ricordo.browser import mapclient

from pmr2.json.mixin import JsonPage, SimpleJsonFormMixin


class QueryForm(SimpleJsonFormMixin, mapclient.QueryForm):

    def render(self):
        if self._searched:
            return json.dumps([{
                'data': v['data'],
                'source': v['source'],
                'obj': {
                    'href': v['source'] or v['obj'].getURL(),
                    'title': v['obj'].Title or v['source'],
                },
            } for v in self.results()])
        return super(QueryForm, self).render()
