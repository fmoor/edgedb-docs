For
---

A ``FOR`` statement is used where mathematically a universal qualifier
(∀) would be appropriate. It allows to compute a set based on the
elements of some other set.

The data flow of a ``FOR`` block that uses elements of a set to
iterate over can be conceptualized like this:

.. code-block:: pseudo-eql

    WITH MODULE example

    FOR <el>        # repeat for every element <el>
        IN <set>    # of the set literal <set>

    UNION
        <expr>  # map every element onto a result set,
                # merging them all with a UNION

    # optional clause
    FILTER
        <expr>  # filter the returned set of values

    # optional clause
    ORDER BY
        <expr>  # define ordering of the filtered set

    # optional clause
    OFFSET
        <expr>  # slice the filtered/ordered set

    # optional clause
    LIMIT
        <expr>  # slice the filtered/ordered set


Typically a simple iteration over set elements is used in conjunction
with an Insert_ or an Update_ statement. This mode is less useful with
a Select_ expression since a ``FILTER`` may accomplish the same end
result.

.. NOTE::

    Technically, a ``FOR`` statement can be viewed as a special case
    of ``GROUP``:

    .. code-block:: eql

        FOR X IN {Foo}
        UNION (INSERT Bar {foo := X});

        # can be equivalently rewritten as:
        GROUP Foo
        USING _ := Foo
        BY _
        INTO X
        UNION (INSERT Bar {foo := X});


Clause signatures
+++++++++++++++++

Here is a summary of clauses that can be used with ``FOR``:

- FOR *alias* IN ``SET OF`` *B*
- *A* UNION ``SET OF`` *B*
- *A* FILTER ``SET OF`` *B*
- *A* ORDER BY ``SET OF`` *B*
- ``SET OF`` *A* OFFSET ``SET OF`` *B*
- ``SET OF`` *A* LIMIT ``SET OF`` *B*


.. _ref_edgeql_forstatement:

Usage of FOR statement
++++++++++++++++++++++

``FOR`` statement has some powerful features that deserve to be
considered in detail separately. However, the common core is that
``FOR`` iterates over elements of some arbitrary expression. Then for
each element of the iterator some set is computed and combined via a
:eql:op:`UNION` with the other such computed sets.

The simplest use case is when the iterator is given by a set
expression and it follows the general form of ``FOR x IN A ...``:

.. code-block:: eql

    WITH MODULE example
    # the iterator is an explicit set of tuples, so x is an
    # element of this set, i.e. a single tuple
    FOR x IN {
        (name := 'Alice', theme := 'fire'),
        (name := 'Bob', theme := 'rain'),
        (name := 'Carol', theme := 'clouds'),
        (name := 'Dave', theme := 'forest')
    }
    # typically this is used with an INSERT, DELETE or UPDATE
    UNION (
        INSERT
            User {
                name := x.name,
                theme := x.theme,
            }
    );

Since ``x`` is an element of a set it is guaranteed to be a non-empty
singleton in all of the expressions used by the ``UNION OF`` and later
clauses of ``FOR``.

Another variation this usage of ``FOR`` is a bulk ``UPDATE``. There
are cases when a bulk update lots of external data, that cannot be
derived from the objects being updated. That is a good use-case when a
``FOR`` statement is appropriate.

.. code-block:: eql

    # Here's an example of an update that is awkward to
    # express without the use of FOR statement
    WITH MODULE example
    UPDATE User
    FILTER User.name IN {'Alice', 'Bob', 'Carol', 'Dave'}
    SET {
        theme := 'red'  IF .name = 'Alice' ELSE
                 'star' IF .name = 'Bob' ELSE
                 'dark' IF .name = 'Carol' ELSE
                 'strawberry'
    };

    # Using a FOR statement, the above update becomes simpler to
    # express or review for a human.
    WITH MODULE example
    FOR x IN {
        (name := 'Alice', theme := 'red'),
        (name := 'Bob', theme := 'star'),
        (name := 'Carol', theme := 'dark'),
        (name := 'Dave', theme := 'strawberry')
    }
    UNION (
        UPDATE User
        FILTER User.name = x.name
        SET {
            theme := x.theme
        }
    );

When updating data that mostly or completely depends on the objects
being updated there's no need to use the ``FOR`` statement and it is not
advised to use it for performance reasons.

.. code-block:: eql

    WITH MODULE example
    UPDATE User
    FILTER User.name IN {'Alice', 'Bob', 'Carol', 'Dave'}
    SET {
        theme := 'halloween'
    };

    # The above can be accomplished with a FOR statement,
    # but it is not recommended.
    WITH MODULE example
    FOR x IN {'Alice', 'Bob', 'Carol', 'Dave'}
    UNION (
        UPDATE User
        FILTER User.name = x
        SET {
            theme := 'halloween'
        }
    );

Another example of using a ``FOR`` statement is working with link
properties. Specifying the link properties either at creation time or
in a later step with an update is often simpler with a ``FOR``
statement helping to associate the link target to the link property in
an intuitive manner.

.. code-block:: eql

    # Expressing this without FOR statement is fairly tedious.
    WITH
        MODULE example,
        U2 := User
    FOR x IN {
        (
            name := 'Alice',
            friends := [('Bob', 'coffee buff'),
                        ('Carol', 'dog person')]
        ),
        (
            name := 'Bob',
            friends := [('Alice', 'movie buff'),
                        ('Dave', 'cat person')]
        )
    }
    UNION (
        UPDATE User
        FILTER User.name = x.name
        SET {
            friends := (
                FOR f in {unnest(x.friends)}
                UNION (
                    SELECT U2 {@nickname := f.1}
                    FILTER U2.name = f.0
                )
            )
        }
    );
