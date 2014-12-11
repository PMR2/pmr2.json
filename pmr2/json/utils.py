import json

def extractRequestObj(request):
    stdin = getattr(request, 'stdin', None)
    if not stdin:
        # nothing
        return 

    stdin.seek(0)
    try:
        obj = json.load(stdin)
    except ValueError:
        return
    return obj

def objToRequest(obj, keys, prefix, request):
    for key, v in obj.iteritems():
        if key.startswith(prefix):
            fullkey = key
            # naively convert this back into a prefixless key to match.
            key = key[len(prefix):]
        else:
            fullkey = prefix + key
        if key in keys:
            request.form[fullkey] = v
