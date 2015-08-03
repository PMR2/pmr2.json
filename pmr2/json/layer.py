import zope.interface
from pmr2.layer.utility import LayerApplierBase

from pmr2.json.http import parse_accept
from pmr2.json import v0
from pmr2.json import v1
from pmr2.json import v2


MIMETYPE_CORE = 'application/vnd.physiome.pmr2.json.'
REQUEST_MARKER_KEY = '_pmr2_json_layer_marker_'

# ordered in precedence.

class NotAcceptableError(TypeError):
    """HTTP 406 Not Acceptable"""


def response_mime_type(media_type, params):
    """
    Reconstitute the media type
    """

    if media_type != 'application/vnd.physiome.pmr2.json.1':
        return media_type
    version = params.get('version')
    if not version:
        return media_type

    return '%s; version=%s' % (media_type, version)

def set_content_type(request, default=None):
    # XXX this only checks and sets a parameterless mimetype.

    content_mimetypes, count = getattr(request, REQUEST_MARKER_KEY, (None, 0))

    if not content_mimetypes:
        if default:
            request.response.setHeader('Content-Type', default)
        return True

    if not default:
        if content_mimetypes:
            request.response.setHeader('Content-Type', content_mimetypes[0])
            return True

    # This filters out anything that we cannot check but implied.
    provided = [mt for mt in content_mimetypes if mt.startswith(MIMETYPE_CORE)]
    if not provided:
        # we can't do the strict checking as the auxilary accepted types
        # are provided which we accept. Simply return that.
        request.response.setHeader('Content-Type', content_mimetypes[0])
        return True

    defaults = [mt for mt in provided if mt.startswith(default)]

    if defaults:
        # The default mimetype is accepted, return the requested one
        # via the accept header that closest match with default.
        request.response.setHeader('Content-Type', defaults[0])
        return True

    # We got nothing.
    request.response.setStatus(406, 'Not Acceptable')
    return False

def handle_ignore(params):
    # For types that should have matched other things
    # XXX probably this needs a common registry to properly work?
    return False

def handle_v0(params):
    return v0.interfaces.IJsonLayer

def handle_v1(params, default='1'):
    version_table = {
        '1': v1.interfaces.IJsonLayer,
        '2': v2.interfaces.IJsonLayer,
    }
    # default version is 1
    version = params.get('version', default)
    # If a version requested falls outside of requested range, default
    # to version 1 for now.
    result = version_table.get(version)
    if not result:
        raise NotAcceptableError
    return result

layer_functions = {
    '*/*': handle_ignore,
    'text/html': handle_ignore,
    'application/xhtml+xml': handle_ignore,
    'application/xml': handle_ignore,
    'application/vnd.physiome.pmr2.json.0': handle_v0,
    'application/vnd.physiome.pmr2.json.1': handle_v1,
    'application/json': handle_v1,
    'application/vnd.collection+json': handle_v1,
    # XXX this is VERY temporary while awaiting OpenCOR to migrate away
    # from the usage of this brief introduction.
    'application/vnd.physiome.pmr2.json.2':
        lambda params: handle_v1(params, '2'),
}


class SimpleJsonLayerApplier(LayerApplierBase):

    def __call__(self, request):
        accept = request['HTTP_ACCEPT']
        if 'json' not in accept:
            # If json wasn't even mention don't waste time.
            return

        media_types = parse_accept(accept)
        results = []
        response_mime_types = []
        for media_type in media_types:
            if not media_type.type in layer_functions:
                continue
            type_, q, params = media_type
            try:
                result = layer_functions[type_](params)
                if result:
                    # set content-type header
                    # XXX I am not sure whether setting that directly
                    # here will result in other side-effects (such as
                    # unintentionally overriding other processes/methods
                    # of doing so in other libraries).  So just in case,
                    # while it is possible we only just simply assign it
                    # to a "private" attribute which views will have to
                    # handle the actual setting sepearate.
                    # XXX this variable should only be used in this
                    # module.
                    response_mime_types.append(
                        response_mime_type(type_, params))
                    results.append(result)
                if result is False:
                    # We have a guaranteed ignore.
                    if not results:
                        # Really ignoring as the request has nothing
                        # we can handle with a higher precedence.
                        return
            except NotAcceptableError:
                if len(media_types) == 1:
                    # XXX if there are _any_ other media types this
                    # cannot assert that there are NO other possible
                    # handlers for content-type.  So only send this iff
                    # there is only one media_type specified.
                    request.response.setStatus(406, 'Not Acceptable')
                continue

        if response_mime_types:
            setattr(request, REQUEST_MARKER_KEY,
                (response_mime_types, len(media_types)))
        return results
