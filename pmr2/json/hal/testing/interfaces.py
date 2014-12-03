import zope.interface
import zope.schema


class IItem(zope.interface.Interface):

    item_id = zope.schema.TextLine(
        title=u'Item ID',
        description=u'The unique identifier for this item.',
    )

    name = zope.schema.TextLine(
        title=u'Name',
        description=u'Name of this item.',
    )

    description = zope.schema.TextLine(
        title=u'Description',
        description=u'The description of this item.',
        required=False,
    )
