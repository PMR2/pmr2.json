import json

from pmr2.json.utils import extractRequestObj
from pmr2.json.utils import objToRequest


def template_to_request(template, request, default_prefix='json.widgets.'):
    data = template['data']
    for d in data:
        prefix = d.get('prefix', default_prefix)
        request.form[prefix + d.get('name', '')] = d.get('value')

def update_json_collection_form(form):
    obj = extractRequestObj(form.request)

    if not isinstance(obj, dict):
        # Should probably just check whether the object is a valid
        # collection.
        return

    # XXX need to revisit this, for support multiple submissions?
    template = obj['template']

    # Widgets doesn't have the prefix initialized yet, so just hard-code
    # this...
    template_to_request(template, form.request, form.prefix + 'widgets.')

def _append_form_widgets(data, form):
    if not form.widgets:
        return

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
            'value': w.value,
            'options': options,
            'prefix': form.prefix + form.widgets.prefix,
        })

def _append_form_actions(data, form):
    if not form.actions:
        return

    for id_, a in form.actions.items():
        data.append({
            'name': id_,
            'prompt': a.title,
            'description': None,
            'type': type(a.field).__name__,
            'required': a.required,
            'value': None,  # what if button is selected?
            # ideal is this, but values are all wrong
            # 'prefix': form.prefix + form.buttons.prefix,
            'prefix': form.prefix + 'buttons.',
        })

def formfields_to_collection_template(form):
    """
    Turn the form fields into a collection template.
    """

    data = []

    _append_form_widgets(data, form)
    _append_form_actions(data, form)

    results = {
        'data': data
    }
    return results

