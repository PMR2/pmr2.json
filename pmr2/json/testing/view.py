from pmr2.json.mixin import JsonPage


class DummyJsonPage(JsonPage):

    def render(self):
        return self.dumps({'result': 1})
