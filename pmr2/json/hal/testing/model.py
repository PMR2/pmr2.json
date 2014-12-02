from zope.interface import implementer
from zope.schema import fieldproperty

from .interfaces import IItem


@implementer(IItem)
class Item(object):

    item_id = fieldproperty.FieldProperty(IItem['item_id'])
    name = fieldproperty.FieldProperty(IItem['name'])
    description = fieldproperty.FieldProperty(IItem['description'])
