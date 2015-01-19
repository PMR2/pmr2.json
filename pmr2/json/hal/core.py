import json

from pmr2.json.utils import extractRequestObj
from pmr2.json.utils import objToRequest


def generate_hal(links, data=None):
    """
    Generates a HAL representation of the input and return as a dict.

    data must be a dict or None.
    """

    # validation for links could be useful?
    result = {
        '_links': links,
    }

    if data:
        if '_links' in data:
            raise ValueError('data cannot contain _links key')
        result.update(data)
    return result

def template_to_request(template, request):
    data = template['data']
    for d in data:
        request.form[d.get('name', '')] = d.get('value')

def generate_collection(version='1.0', href=None, links=None, items=None,
        queries=None, template=None, error=None):
    keys = (
        'version', 'href', 'links', 'items', 'queries', 'template', 'error',)
    kw = locals()
    return {
        'collection': {key: kw[key] for key in keys if kw.get(key) is not None}
    }

def json_collection_view_init(view):
    view._jc_links = None
    view._jc_items = None
    view._jc_queries = None
    view._jc_template = None
    view._jc_error = None

def json_collection_view_render(view):
    return view.dumps(generate_collection(
        href=view.context.absolute_url() + '/' + view.__name__,
        links=view._jc_links,
        items=view._jc_items,
        queries=view._jc_queries,
        template=view._jc_template,
        error=view._jc_error,
    ))

def update_json_collection_form(form):
    obj = extractRequestObj(form.request)

    if not isinstance(obj, dict):
        # Should probably just check whether the object is a valid
        # collection.
        return

    # XXX need to revisit this, for support multiple submissions?
    template = obj['template']

    template_to_request(template, form.request)

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
            'name': form.prefix + form.widgets.prefix + id_,
            'prompt': w.field.title,
            'description': w.field.description,
            'type': type(w.field).__name__,
            'required': w.required,
            'value': w.value,
            'options': options,
        })

def _append_form_actions(data, form):
    if not form.actions:
        return

    for id_, a in form.actions.items():
        data.append({
            # ideal is this, but values are wrong because where this
            # function is used (before form.buttons have been updated).
            # 'name': form.prefix + form.buttons.prefix + id_,
            'name': form.prefix + 'buttons.' + id_,
            'prompt': a.title,
            'description': None,
            'type': type(a.field).__name__,
            'required': a.required,
            'value': None,  # what if button is selected?
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

