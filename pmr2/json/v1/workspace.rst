Workspace with JSON
===================

Let's try calling the workspace creation view.  We should get back a 
JSON object that describes what the fields and actions are for this 
form::

    >>> import json
    >>> from cStringIO import StringIO
    >>> from pmr2.json.v1.workspace import JsonWorkspaceStorageCreateForm
    >>> from pmr2.json.tests.base import TestRequest
    >>> context = self.portal.w.test_user_1_
    >>> request = TestRequest()
    >>> form = JsonWorkspaceStorageCreateForm(context, request)
    >>> result = json.loads(form())
    >>> sorted([datum['name'] for datum in
    ...     result['collection']['template']['data']])
    [u'form.buttons.add', u'form.widgets.description', u'form.widgets.id',
     u'form.widgets.storage', u'form.widgets.title']


As the expected payload will be another JSON object, let's try to submit
some JSON to this form::

    >>> payload = {
    ...     'template': {
    ...         'data': [
    ...             {
    ...                 'name': 'form.buttons.add',
    ...                 'value': True,
    ...             }
    ...         ],
    ...     }
    ... }
    >>> stdin = StringIO()
    >>> json.dump(payload, stdin)
    >>> request = TestRequest(method='POST', stdin=stdin)
    >>> form = JsonWorkspaceStorageCreateForm(context, request)
    >>> form.update()
    >>> result = json.loads(form.render())
    >>> result['collection']['error']
    {u'message': u'There were some errors.', u'code': u'error', u'errors':
     [{u'message': u'Required input is missing.', u'name': u'form.widgets.id'},
      {u'message': u'Required input is missing.',
      u'name': u'form.widgets.storage'}], u'title': u'Error'}

So the form parses the input and the specified action triggered some
validation and the results are returned as a JSON string.

Now let's see how this works in practice.  As this view is registered to
the workspace container, we can try to access this normally using the
browser class.::

    >>> tb = self.testbrowser
    >>> tb.addHeader('Accept', 'application/vnd.physiome.pmr2.json.1')
    >>> portal_url = self.portal.absolute_url()
    >>> tb.open(portal_url + '/w/test_user_1_/+/addWorkspace')
    >>> result = json.loads(tb.contents)
    >>> sorted([datum['name'] for datum in
    ...     result['collection']['template']['data']])
    [u'form.buttons.add', u'form.widgets.description', u'form.widgets.id',
     u'form.widgets.storage', u'form.widgets.title']

Try to submit the same data.::

    >>> tb.open(portal_url + '/w/test_user_1_/+/addWorkspace',
    ...     data=json.dumps(payload))
    >>> result = json.loads(tb.contents)
    >>> result['collection']['error']
    {u'message': u'There were some errors.', u'code': u'error', u'errors':
     [{u'message': u'Required input is missing.', u'name': u'form.widgets.id'},
      {u'message': u'Required input is missing.',
      u'name': u'form.widgets.storage'}], u'title': u'Error'}

Now do this for real, apply the test data and see if the dummy workspace
can be created like this.::

    >>> payload = {
    ...     'template': {
    ...         'data': [
    ...             {
    ...                 'name': 'form.widgets.id',
    ...                 'value': 'test',
    ...             },
    ...             {
    ...                 'name': 'form.widgets.description',
    ...                 'value': 'Test Dummy',
    ...             },
    ...             {
    ...                 'name': 'form.widgets.storage',
    ...                 'value': 'dummy_storage',
    ...             },
    ...             {
    ...                 'name': 'form.buttons.add',
    ...                 'value': True,
    ...             },
    ...         ],
    ...     }
    ... }
    >>> tb.open(portal_url + '/w/test_user_1_/+/addWorkspace',
    ...     data=json.dumps(payload))
    >>> print tb.url
    http://nohost/plone/w/test_user_1_/test

Success - the redirection to the created object is done here.  Like the
standard html based forms, after successful creation the client will be
redirected to the created resource.  Check that the resource loads.::

    >>> result = json.loads(tb.contents)
    >>> result['collection']['items'][0]['data'][0]['name']
    u'id'
    >>> result['collection']['items'][0]['data'][0]['value']
    u'test'
    >>> result['collection']['items'][0]['data'][3]['name']
    u'description'
    >>> result['collection']['items'][0]['data'][3]['value']
    u'Test Dummy'

Now see if it is possible to edit the workspace.::

    >>> payload = {
    ...     'template': {
    ...         'data': [
    ...             {
    ...                 'name': 'form.widgets.description',
    ...                 'value': 'Edited',
    ...             },
    ...             {
    ...                 'name': 'form.buttons.apply',
    ...                 'value': True,
    ...             },
    ...         ],
    ...     }
    ... }
    >>> tb.open(portal_url + '/w/test_user_1_/test/edit',
    ...     data=json.dumps(payload))

    >>> tb.open(portal_url + '/w/test_user_1_/test')
    >>> result = json.loads(tb.contents)
    >>> result['collection']['items'][0]['data'][0]['name']
    u'id'
    >>> result['collection']['items'][0]['data'][0]['value']
    u'test'
    >>> result['collection']['items'][0]['data'][3]['name']
    u'description'
    >>> result['collection']['items'][0]['data'][3]['value']
    u'Edited'
