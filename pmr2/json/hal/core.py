import json


def formfields_to_collection_template(form):
    fields_keys = ['description', 'title']
    widget_keys = ['error', 'items', 'klass', 'value',]
    action_keys = ['title',]
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

        # first cut...
        data.append({
            'name': id_,
            'prompt': field.get('title'),
            'description': field.get('description'),
            'value': None,  # TODO populate this
        })

    for id_, v in form.actions.items():
        actions[id_] = to_dict(action_keys, v)

    results = {
        'data': data
    }
    return results
