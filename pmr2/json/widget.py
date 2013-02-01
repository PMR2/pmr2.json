import zope.component
from zope.schema.interfaces import IList, IDict

from z3c.form.converter import BaseDataConverter  #, FormatterError
from z3c.form.interfaces import IWidget
from z3c.form.widget import FieldWidget
from z3c.form.browser.textarea import TextAreaWidget

from pmr2.json.interfaces import IJsonWidget


class JsonDataConverter(BaseDataConverter):
    zope.component.adapts(IList, IJsonWidget)

    def toWidgetvalue(self, value):
        return value

    def toFieldValue(self, value):
        if isinstance(value, list):
            return value
        # raise FormatterError?
        return self.field.missing_value


class JsonDataWidget(TextAreaWidget):
    zope.interface.implements(IJsonWidget)


def JsonDataWidgetFactory(field, request):
    return FieldWidget(field, JsonDataWidget(request))
