:orphan:

.. _ref_eql_expr_paths:

Paths
-----

A *path expression* (or simply a *path*) represents a set of values that
can be reached from a given set of source nodes by navigating a specific
path in the data graph.  The form of a path is:

.. code-block:: pseudo-eql

    expression path-step [ path-step ... ]

Here *expression* is any expression and *path-step* is:

.. code-block:: pseudo-eql

    step-direction pointer-name [ step-target-filter ]

*step-direction* is one of the following:

- ``.`` or ``.>`` for an outgoing link reference
- ``.<`` for an incoming link reference
- ``@`` for a link property reference

*pointer-name* must be a valid link or link property name.

*step-target-filter* is an optional filter that narrows which *types* of
objects should be included in the result.  It has the following syntax:

.. code-block:: pseudo-eql

   [ IS type ]

The example below shows a path that represents the names of all friends
of all ``User`` objects in the database.

.. code-block:: edgeql

    User.friends.name

And this represents all users who are owners of at least one ``Issue``:

.. code-block:: edgeql

    Issue.<owners[IS User]

And this represents a set of all dates on which users became friends,
if ``since`` is defined as a link property on the ``User.friends`` link:

.. code-block:: edgeql

    User.friends@since

.. note::

    Link properties cannot point to objects, hence the ``@`` indirection
    will always be the last step in a path.



.. TODO old content below, extract useful examples to illustrate path
   behaviour.  Also, demonstrate path canonicalization (path prefix)



Path Expressions
----------------

Path expressions (typically referred to as simply `paths`) are
fundamental building blocks of EdgeQL. A path defines a set of data in
EdgeDB (just like any other expression) based on the data type and
relationship with other data.

A path always starts with some ``concept`` as its ``root`` and it may
have an arbitrary number of ``steps`` following various ``links``. The
simplest path consists only of a ``root`` and is interpreted to mean
'all objects of the type `root`'.

.. code-block:: edgeql

    WITH MODULE example
    SELECT Issue;

In the above example ``Issue`` is a path that represents all objects in
the database of type ``Issue``. That is the result of the above query.

.. code-block:: edgeql

    WITH MODULE example
    SELECT Issue.owner;

The path ``Issue.owner`` consists of the ``root`` ``Issue`` and a ``path
step`` ``.owner``. It specifies the set of all objects that can be
reached from any object of type ``Issue`` by following its link
``owner``. This means that the above query will only retrieve users
that actually have at least one issue. The ``.`` operator in the path
separates ``steps`` and each step corresponds to a ``link`` name that
must be followed. By default, links are followed in the ``outbound``
direction (the direction that is actually specified in the schema).
The direction of the link can be also specified explicitly by using
``>`` for ``outbound`` and ``<`` for `inbound`. Thus, the above query
can be rewritten more explicitly, but equivalently as:

.. code-block:: edgeql

    WITH MODULE example
    SELECT Issue.>owner;

To select all issues that actually have at least one watcher, it is
possible to construct a path using ``inbound`` link:

.. code-block:: edgeql

    WITH MODULE example
    SELECT User.<watchers;

The path in the above query specifies the set of all objects that can
be reached from ``User`` by following any ``link`` named ``watchers``
that has ``User`` as its target, back to the source of the ``link``.
In our case, there is only one link in the schema that is called
``watchers``. This link belongs to ``Issue`` and indeed it has
``User`` as its target, so the above query will get all the ``Issue``
objects that have at least one watcher. Only links that have a concept
as their target can be followed in the ``inbound`` direction. It is not
possible to follow inbound links on atoms.

Just like the direction of the step can be specified explicitly in a
path, so can the type of the link target. In order to retrieve all the
``SystemUsers`` that have actually created new ``Issues`` (as opposed
to ``Comments``) the following query could be made:

.. code-block:: edgeql

    WITH MODULE example
    SELECT Issue.owner[IS SystemUser];

In the above query the ``path step`` is expressed as ``owner[IS
SystemUser]``, where ``owner`` is the name of the link to follow, and
the qualifier ``[IS ...]`` specifies a restriction on the target's
type.

This is equivalent to:

.. code-block:: edgeql

    WITH MODULE example
    SELECT Issue.owner
    FILTER Issue.owner IS SystemUser;

The biggest difference between the two of the above representations is
that ``[IS SystemUser]`` allows to refer to links specific to
``SystemUser``.

Finally combining all of the above, it is possible to write a query to
retrieve all the ``Comments`` to ``Issues`` created by ``SystemUsers``:

.. code-block:: edgeql

    WITH MODULE example
    SELECT SystemUser.<owner[IS Issue].<issue;

    # or equivalently

    WITH MODULE example
    SELECT SystemUser
        # follow the link 'owner' to a source Issue
        .<owner[IS Issue]
        # follow the link 'issue' to a source Comment
        .<issue[IS Comment];

.. note::

    Links technically also belong to a module. Typically, the module
    doesn't need to be specified (because it is the default module or
    the link name is unambiguous), but sometimes it is necessary to
    specify the link module explicitly. The entire fully-qualified
    link name then needs to be enclosed in parentheses:

    .. code-block:: edgeql

        WITH MODULE some_module
        SELECT A.foo.bar;

Link properties
+++++++++++++++

It is possible to have a path that represents a set of link properties
as opposed to link target values. Since link properties have to be
atomic, the step pointing to the link property is always the last step
in a path. The link property is accessed by using ``@`` instead
of ``.``.

Consider the following schema:

.. code-block:: eschema

    link favorites:
        link property rank to int

    concept Post:
        required link body to str
        required link owner to User

    concept User extending std::Named:
        link favorites to Post:
            mapping := '**'

Then the query selecting all favorite Post sorted by their rank is:

.. code-block:: edgeql

    WITH MODULE example
    SELECT User.favorites
    ORDER BY User.favorites@rank;
