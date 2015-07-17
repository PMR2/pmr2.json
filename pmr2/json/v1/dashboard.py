import json
import zope.component

from pmr2.app.settings.interfaces import IDashboardOption
from pmr2.app.settings.browser import dashboard

from pmr2.json.collection.mixin import JsonCollectionPage


class Dashboard(JsonCollectionPage, dashboard.Dashboard):

    def update(self):
        options = zope.component.getAdapters(
            (self, self.request), IDashboardOption)

        self._jc_links = [
            {
                # XXX determine whether relation is the right one.
                'rel': 'bookmark',
                'name': name,
                'href': '/'.join([
                    self.context.absolute_url(), self.__name__, name]),
                'prompt': option.title,
            }
            for name, option in options
        ]

        self._jc_href = '/'.join([self.context.absolute_url(), self.__name__])
