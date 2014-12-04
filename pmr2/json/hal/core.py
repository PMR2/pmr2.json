import json


def formfields_to_collection_template(form):
    fields_keys = ['description', 'title']
    widget_keys = ['error', 'items', 'klass', 'value',]
    action_keys = ['description', 'title',]
    fields = {}
    widgets = {}
    actions = {}

    data = []

    # XXX based on current extraction code.

    def to_dict(keys, value):
        result = []
        for k in keys:
            v = getattr(value, k, None)
            # error is a view, get the raw message instead.
            if hasattr(v, 'message'):
                result.append((k, v.message))
                continue
            elif callable(v):
                result.append((k, v()))
            else:
                result.append((k, v))
        return dict(result)

    for id_, v in form.fields.items():
        fields[id_] = to_dict(fields_keys, v.field)

    for id_, v in form.widgets.items():
        widgets[id_] = to_dict(widget_keys, v)
        # we only care about fields that have a widget.
        field = fields.get(id_, {})
        widgets[id_].update(field)

        # this is gross.
        if widgets[id_]['items']:
            options = [{
                'text': i['content'],
                'value': i['value'],
            } for i in widgets[id_]['items']]
        else:
            options = None

        # first cut...
        data.append({
            'name': id_,
            'prompt': field.get('title'),
            'description': field.get('description'),
            'type': type(v.field).__name__,
            'required': v.required,
            'value': None,  # TODO populate this
            'options': options,
        })

    for id_, a in form.actions.items():
        action = actions[id_] = to_dict(action_keys, a)

        data.append({
            'name': id_,
            'prompt': action.get('title'),
            'description': action.get('description'),
            'type': type(a.field).__name__,
            'required': a.required,
            'value': None,  # what if button is selected?
        })

    results = {
        'data': data
    }
    return results
