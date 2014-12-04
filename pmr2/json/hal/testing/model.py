from zope.interface import implementer
from zope.schema import fieldproperty

from .interfaces import IItem
from .interfaces import IOption


@implementer(IItem)
class Item(object):

    item_id = fieldproperty.FieldProperty(IItem['item_id'])
    name = fieldproperty.FieldProperty(IItem['name'])
    description = fieldproperty.FieldProperty(IItem['description'])


@implementer(IOption)
class Option(object):

    item_id = fieldproperty.FieldProperty(IOption['item_id'])
    option = fieldproperty.FieldProperty(IOption['option'])
