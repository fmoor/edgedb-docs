.. _ref_edgeql_expressions_tuple_constructor:

Tuple constructor
-----------------

.. TODO

Creating collections syntactically (e.g. using ``[...]`` or ``(...)``)
is an element-wise operation. One way of thinking about these syntax
constructs is to treat them exactly like functions that simply turn
their arguments into a set of collections.

This means that the following code will create a set of tuples with
the first element being ``Issue`` and the second a :eql:type:`str`
representing the ``Issue.priority.name``:

.. code-block:: eql

    WITH MODULE example
    SELECT (Issue, Issue.priority.name);

Since ``priority`` is not a required link, not every ``Issue`` will
have one. It is important to realize that the above query will *only*
contain Issues with non-empty priorities. If it is desirable to have
*all* Issues, then coalescing (:eql:op:`??<COALESCE>`) or a
:ref:`shape<ref_edgeql_shapes>` query should be used instead.

On the other hand the following query will include *all* Issues,
because the tuple elements are made from the set of Issues and the set
produced by the aggregate function :eql:func:`array_agg`, which is
never ``{}``:

.. code-block:: eql

    WITH MODULE example
    SELECT (Issue, array_agg(Issue.priority.name));


Tuple element reference
-----------------------

.. TODO
