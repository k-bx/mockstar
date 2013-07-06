.. mockstar documentation master file, created by
   sphinx-quickstart on Wed May  9 16:32:05 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Mockstar -- Declarative Mocking Like a Rockstar!
================================================

Mockstar is a small enhance on top of `Mock
<http://www.voidspace.org.uk/python/mock/mock.html>`_ library that
gives you declarative way to write your unit-tests.

- author: `Konstantine Rybnikov <http://redhotchilipython.com/>`_.
- main repository on bitbucket: `https://bitbucket.org/k_bx/mockstar
<https://bitbucket.org/k_bx/mockstar>`_
- mirror on github: `https://github.com/k-bx/mockstar
<https://github.com/k-bx/mockstar>`_

Philosophy
----------

Usually, **unit under test** is something simple, like function or
method. It's result is dependent on it's arguments and calls to some
external dependencies (side-effects). For example, here:

.. literalinclude:: code/philosophy.py

Unit under test is ``PostForm`` class (more precicely, it's ``clean``
method here), it has one side-effect, which is ``is_post_exist``
function.

Usually, you create a single test module for single code module (well,
I do). So in this example **module under test** would be
``myapp.blog.forms``.

Minimal test-case example
-------------------------

Your minimal test case would look something like this:

.. literalinclude:: code/minimal_example.py

More detailed introduction
--------------------------

So, you want to implement and test your unit. Let's say it's a
function :func:`create_user` that will look like this when it is done:

.. literalinclude:: code/unit.py

This unit consists of input-parameters:

- email
- password
- full_name

and seven side-effects:

- ``User`` model
- ``not_md5_and_has_salt`` function
- ``count_score`` function
- ``choose_low_quality_avatar`` function
- ``choose_high_quality_avatar`` function
- ``mail`` business-logic
- ``discover_possible_friends`` function

So, to test this unit in isolation we would need to mock-out all
side-effects, on every test put some return-values so that they will
fit our if-else clauses, and finally, generate suitable
input-parameters.

With `Mock <http://www.voidspace.org.uk/python/mock/mock.html>`_
library, you would do something like this:

.. literalinclude:: code/unit_test_mock.py

Problems I see:

- need to repeat mocked names as test parameters
- need to write autospec=True again and again
- need to write module prefix ``app.bl.user`` on every patch call
- need to patch on every test case
- need to add common return_values and assign to some variables (like
  user) that we'll use later in asserts
- side_effects take a lot of space in our testing code, I want to
  separate them

With mockstar your test would look something like this:

.. literalinclude:: code/unit_test_mockstar.py

I hope you like mockstar's aspiration to get declarative way of
writing unit-tests and reduce of copypasta.

Installation
------------

To install mockstar, just type::

    pip install mockstar

..
   Contents:

   .. toctree::
      :maxdepth: 2

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

