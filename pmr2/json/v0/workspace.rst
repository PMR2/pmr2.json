Workspace with JSON
===================

Let's try calling the workspace creation view.  We should get back a 
JSON object that describes what the fields and actions are for this 
form.
::

    >>> import json
    >>> from cStringIO import StringIO
    >>> from pmr2.json.v0.workspace import JsonWorkspaceStorageCreateForm
    >>> from pmr2.json.tests.base import TestRequest
    >>> context = self.portal.w.test_user_1_
    >>> request = TestRequest()
    >>> form = JsonWorkspaceStorageCreateForm(context, request)
    >>> result = json.loads(form())
    >>> sorted(result['fields'].keys())
    [u'description', u'id', u'storage', u'title']
    >>> sorted(result['actions'].keys())
    [u'add']

As the expected payload will be another JSON object, let's try to submit
some JSON to this form.
::

    >>> request = TestRequest(method='POST', 
    ...     stdin=StringIO('{"actions":{"add":1}}'))
    >>> form = JsonWorkspaceStorageCreateForm(context, request)
    >>> result = json.loads(form())
    >>> result['fields']['id']['error']
    u'Required input is missing.'
    >>> result['fields']['storage']['error']
    u'Required input is missing.'

So the form parses the input and the specified action triggered some
validation and the results are returned as a JSON string.

Now let's see how this works in practice.  As this view is registered to
the workspace container, we can try to access this normally using the
browser class.
::

    >>> tb = self.testbrowser
    >>> tb.addHeader('Accept', 'application/vnd.physiome.pmr2.json.0')
    >>> portal_url = self.portal.absolute_url()
    >>> tb.open(portal_url + '/w/test_user_1_/+/addWorkspace')
    >>> result = json.loads(tb.contents)
    >>> sorted(result['fields'].keys())
    [u'description', u'id', u'storage', u'title']
    >>> sorted(result['actions'].keys())
    [u'add']

Try to submit the same data.
::

    >>> tb.open(portal_url + '/w/test_user_1_/+/addWorkspace', data=
    ...     '{"actions":{"add":1}}')
    >>> result = json.loads(tb.contents)
    >>> result['fields']['id']['error']
    u'Required input is missing.'
    >>> result['fields']['storage']['error']
    u'Required input is missing.'

Now do this for real, apply the test data and see if the dummy workspace
can be created like this.
::

    >>> tb.open(portal_url + '/w/test_user_1_/+/addWorkspace', data=
    ...     '{"fields":{"id":"test", "storage":"dummy_storage", '
    ...     ' "description": "Test Dummy"}, "actions":{"add":1}}')
    >>> print tb.url
    http://nohost/plone/w/test_user_1_/test

Success - the redirection to the created object is done here.  Like the
standard html based forms, after successful creation the client will be
redirected to the created resource.  Check that the resource loads.
::

    >>> result = json.loads(tb.contents)
    >>> result['id']
    u'test'
    >>> result['description']
    u'Test Dummy'

Now see if it is possible to edit the workspace.
::

    >>> tb.open(portal_url + '/w/test_user_1_/test/edit', data=
    ...     '{"fields": {"description": "Edited"}, "actions": {"apply": 1}}')
    >>> tb.open(portal_url + '/w/test_user_1_/test')
    >>> result = json.loads(tb.contents)
    >>> result['id']
    u'test'
    >>> result['description']
    u'Edited'
    >>> result['storage']
    u'dummy_storage'
