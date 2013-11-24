CrashPlan API
=============
This project aims to provide a simple interface to the public resources
of the CrashPlan API with support for the new versioned API.

Examples
========
***NOTE!!*** The current state of the project isn't here yet but it's the goal.

    # Simple request to Computer resource (most recent version)
    >>> resp = Platform42Api.get("crashplan.com", Computer, APISession())
    >>> resp.data.computerId
    42

    # Same resource but older version
    >>> params = { 'some_old_api_param' : 'foo' }
    >>> resp = Platform42Api.get("crashplan.com", Computer, APISession(maxVersion=0), data=params) # Use an old api
    >>> resp.data.oldApiValue
    'bar'

    # Authentication. It was transparently handled in the APISession above but here is how you can change
    # it yourself. Don't be alarmed about the dynamic type creation, I just don't want to put a regular object
    # definition here.
    >>> s = APISession(auth_provider= type('provider' , (object, ), {'getAuth' : lambda: ('user', 'password')}))
    >>> resp = Platform42Api.put("crashplan.com", Computer, s)
    >>> resp.status_code
    200

Requirements
============
**For the app:**

 - [requests][1]


**To run tests:**

- [nose][2]
- [nose-exclude][3]
- [coverage][4]
- [doctest][5]

Recommended Development Setup
=============================
* Install virtualenvwrapper. Follow additional setup here [readthedocs][6]

> pip install virtualenvwrapper

* Create a project to work on

> mkvirtualenv --no-site-packages platform42

* Setup IDE of your choice. I recommend [Eclipse][7] + [PyDev][8] or [LiClipse][9]. Setup the project in your IDE to use your virtualenv's interpreter and libraries
In the editors I listed this can be accomplished by manually setting up an interpreter and pointing it at [your virtualenv path]/bin/python.

* Install the requirements listed above. Execute the following while in the virtualenv created earlier. This script sits in the bin directory of the project.

> ./bin/project_manage.sh -i


  [1]: http://www.python-requests.org/en/latest/
  [2]: http://nose.readthedocs.org/en/latest/
  [3]: https://pypi.python.org/pypi/nose-exclude
  [4]: https://pypi.python.org/pypi/coverage
  [5]: http://docs.python.org/2/library/doctest.html
  [6]: http://virtualenvwrapper.readthedocs.org/en/latest/install.html
  [7]: http://www.eclipse.org/
  [8]: http://pydev.org/download.html
  [9]: http://liclipse.blogspot.com/
