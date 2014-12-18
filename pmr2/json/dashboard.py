import json
import zope.component

from pmr2.app.settings.interfaces import IDashboardOption
from pmr2.app.settings.browser import dashboard

from pmr2.json.mixin import JsonPage


class Dashboard(JsonPage, dashboard.Dashboard):

    json_mimetype = 'application/vnd.physiome.pmr2.json.1'

    def render(self):
        options = zope.component.getAdapters(
            (self, self.request), IDashboardOption)

        result = {
            '_links': {
                name: {
                    'href': '/'.join([
                        self.context.absolute_url(), self.__name__, name]),
                    'label': option.title,
                }
                for name, option in options
            }
        }

        # inject the recommended self link.
        result['_links']['self'] = {
            'href': '/'.join([self.context.absolute_url(), self.__name__]),
            'label': 'self'
        }

        return json.dumps(result)
