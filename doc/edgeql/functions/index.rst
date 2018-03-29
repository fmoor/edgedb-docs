.. _ref_edgeql_functions:


Functions
=========

Many built-in functions and user-defined functions operate on
elements, so they are also element operations. This implies that if
any of the input sets are empty, the result of applying an element
function is also empty.

.. _ref_edgeql_functions_agg:

Aggregate functions are *set functions* mapping arbitrary sets onto
singletons. Examples of aggregate functions include built-ins such as
:eql:func:`count` and :eql:func:`array_agg`.

.. code-block:: eql

    # count maps a set to an integer, specifically it returns the
    # number of elements in a set
    SELECT count(example::Issue);

    # array_agg maps a set to an array of the same type, specifically
    # it returns the array made from all of the set elements (which
    # can also be ordered)
    WITH MODULE example
    SELECT array_agg(Issue ORDER BY Issue.number);

EdgeQL has a number of built-in functions in the ``std`` module. Like
everything else in ``std`` module it is not necessary to specify the
module name to refer to these functions.

.. toctree::
    :maxdepth: 3

    array
    datetime
    polymorphic
    random
    setagg
    string
