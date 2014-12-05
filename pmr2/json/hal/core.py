import json


def formfields_to_collection_template(form):
    fields_keys = ['description', 'title']
    widget_keys = ['error', 'items', 'klass', 'value',]
    action_keys = ['description', 'title',]

    data = []

    for id_, w in form.widgets.items():
        # this is gross.
        if hasattr(form.widgets[id_], 'items'):
            options = [{
                'text': i['content'],
                'value': i['value'],
            } for i in form.widgets[id_].items()]
        else:
            options = None

        data.append({
            'name': id_,
            'prompt': w.field.title,
            'description': w.field.description,
            'type': type(w.field).__name__,
            'required': w.required,
            'value': None,  # TODO populate this
            'options': options,
        })

    for id_, a in form.actions.items():
        data.append({
            'name': id_,
            'prompt': a.title,
            'description': None,
            'type': type(a.field).__name__,
            'required': a.required,
            'value': None,  # what if button is selected?
        })

    results = {
        'data': data
    }
    return results
