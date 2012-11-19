import json
import zope.component

from pmr2.app.settings.interfaces import IDashboardOption
from pmr2.app.settings.browser import dashboard

from pmr2.json.mixin import JsonPage


class Dashboard(JsonPage, dashboard.Dashboard):

    def render(self):
        options = zope.component.getAdapters(
            (self, self.request), IDashboardOption)

        result = [(name, {
                'target': '/'.join([
                    self.context.absolute_url(), self.__name__, name]),
                'label': option.title,
            }) for name, option in options]

        result = dict(result)
        return json.dumps(result)
