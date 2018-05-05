Tutorial
========

This tutorial covers the setup and a few use case for an issue
management platform.

Setup the database
------------------

Install. Run the server.

Once the EdgeDB server is up and running the first thing to do is to
add a schema that we will be using. To do that, let's consider which
objects we will need in our system. Obviously we want a ``User`` and
an ``Issue``. We probably want a ``Status``, too. In order to provide
feedback on issues a ``Comment`` type seems like a good idea. So
let's start with defining the schema with these 4 types. Later on,
if we need more, we can amend the schema.

The original schema would be something like this:

.. code-block:: eschema

    type User:
        required property name -> str

    type Issue:
        required property text -> str
        required link status -> Status
        required link owner -> User

    type Status:
        required property name -> str:
            # the status names should be unique
            constraint unique

    type Comment:
        required property text -> str
        # It makes more sense to link comments to issues rather than
        # vice-versa, since that makes their coupling in the schema
        # less tight. This is a good practice for relationships that
        # don't represent inherent properties.
        required link issue -> Issue:
            cardinality := '*1'
        property timestamp -> datetime:
            default := SELECT datetime::current_datetime()
            # the timestap will be automatically set to the current
            # time if it is not specified at the point of comment
            # creation

The schema can be applied either via a migration tool or directly
using ``CREATE MIGRATION`` and ``COMMIT MIGRATION`` commands. Let's do it in
the interactive console via the low level EdgeQL commands.

.. eql:migration:: d1

    type User:
        required property name -> str

    type Issue:
        required property text -> str
        required link status -> Status
        required link owner -> User

    type Status:
        required property name -> str:
            # the status names should be unique
            constraint unique

    type Comment:
        required property text -> str
        # It makes more sense to link comments to issues rather than
        # vice-versa, since that makes their coupling in the schema
        # less tight. This is a good practice for relationships that
        # don't represent inherent properties.
        required link issue -> Issue:
            cardinality := '*1'
        property timestamp -> datetime:
            default := SELECT datetime::current_datetime()
            # the timestap will be automatically set to the current
            # time if it is not specified at the point of comment
            # creation

Now we can start populating the DB with actual objects. For
consistency with examples in other parts of the documentation let's
name the module "example".

Let's start with a few users and status objects:

.. code-block:: edgeql

    INSERT example::User {
        name := 'Alice Smith'
    };

    INSERT example::User {
        name := 'Bob Johnson'
    };

    INSERT example::Status {
        name := 'Open'
    };

    INSERT example::Status {
        name := 'Closed'
    };

Note that alternatively, the users and statuses could have been created using
:ref:`GraphQL queries <ref_graphql_overview>`.

Now that we have the basics set up, we can log the first issue:

.. code-block:: edgeql

    WITH MODULE example
    INSERT Issue {
        text :=
            'The issue system needs more status values and maybe priority.',
        status := (SELECT Status FILTER Status.name = 'Open'),
        owner := (SELECT User FILTER User.name = 'Bob Johnson')
    };

Let's add priority to the schema, first. We'll have one new
``type`` and a change to the existing ``Issue``:

.. code-block:: eschema

    type User:
        required property name -> str

    type Status:
        required property name -> str:
            # the status names should be unique
            constraint unique

    type Comment:
        required property text -> str
        # It makes more sense to link comments to issues rather than
        # vice-versa, since that makes their coupling in the schema
        # less tight. This is a good practice for relationships that
        # don't represent inherent properties.
        required link issue -> Issue:
            cardinality := '*1'
        property timestamp -> datetime:
            default := SELECT datetime::current_datetime()
            # the timestap will be automatically set to the current
            # time if it is not specified at the point of comment
            # creation

    #
    # no changes to the above types
    #

    type Issue:
        required property text -> str
        required link status -> Status
        required link owner -> User
        link priority -> Priority
        # let's make priority optional

    type Priority:
        required property name -> str:
            constraint unique

.. code-block:: edgeql

    CREATE MIGRATION example::d2
    FROM example::d1
    TO eschema $$
        # ... new schema goes here
    $$;

    COMMIT MIGRATION example::d2;

Given the new schema we can use the migration tools to apply the
changes to our existing EdgeDB data. After that we can create
``Status`` and ``Priority`` objects.

.. code-block:: edgeql

    INSERT example::Priority {
        name := 'High'
    };

    INSERT example::Priority {
        name := 'Low'
    };

    INSERT example::Status {
        name := 'New'
    };

    INSERT example::Status {
        name := 'Rejected'
    };

With the priority objects all set up we can now update the ``Issue``
to have "High" priority.

.. code-block:: edgeql

    WITH MODULE example
    UPDATE Issue
    FILTER Issue.id = 'd54f6472-8f07-44d9-909e-22864dc6f811'
    SET {
        priority := (SELECT Priority FILTER Priority.name = 'High')
    };

    # The id used above is something that would have been returned by
    # the 'INSERT Issue ...' query or we could simply query it
    # separately.

It seems though that the issue has actually been resolved, so let's
make a comment about that and close the issue.

.. code-block:: edgeql

    WITH MODULE example
    INSERT Comment {
        issue := (
            SELECT Issue
            FILTER Issue.id = 'd54f6472-8f07-44d9-909e-22864dc6f811'
        ),
        text := "I've added more statuses and created priorities."
    };

    WITH MODULE example
    UPDATE Issue
    SET {
        status := (SELECT Status FILTER Status.name = 'Closed')
    };

At this point we may have realized that ``Issue`` and ``Comment`` have
some underlying similarity, they are both pieces of text written by
some user. Moreover, we could envision that as the system grows we
could have other types that are owned by users as well as other
kinds of text objects that record messages and such. While we're at
it, we might as well also create an abstract type for things with a
``name``. So let's update the schema again, this time mostly
refactoring.

.. code-block:: eschema

    abstract type Named:
        required property name -> str

    # Dictionary is a NamedObject variant, that enforces
    # name uniqueness across all instances if its subclass.
    abstract type Dictionary extending Named:
        required property name -> str:
            delegated constraint unique

    abstract type Text:
        # This is an abstract object containing text.
        required property text -> str:
            # let's limit the maximum length of text to 10000
            # characters.
            constraint maxlength(10000)

    abstract type Owned:
        # don't make the link owner required so that we can first
        # assign an owner to Comment objects already in the DB
        link owner -> User:
            cardinality := '*1'

    type User extending Named
    # no need to specify 'link name' here anymore as it's inherited

    type Issue extending Text, Owned:
        required link status -> Status
        link priority -> Priority
        required link owner -> User:
            cardinality := '*1'
        # because we override the link owner to be required,
        # we need to keep this definition

    type Priority extending Dictionary

    type Status extending Dictionary

    type Comment extending Text, Owned:
        required link issue -> Issue:
            cardinality := '*1'
        property timestamp -> datetime:
            default := SELECT datetime::current_datetime()
            # the timestap will be automatically set to the current
            # time if it is not specified at the point of comment
            # creation

.. code-block:: edgeql

    CREATE MIGRATION example::d3
    FROM example::d2 TO eschema $$
        # ... new schema goes here
    $$;
    COMMIT MIGRATION example::d3;

After the migration we still need to fix all comments in our system to
have some owner. In the example so far there was only comment but
let's treat it as if we have several comments made by the same person.

.. code-block:: edgeql

    WITH MODULE example
    UPDATE Comment
    SET {
        owner := (SELECT User FILTER User.name = 'Alice Smith')
    };

Now that all of the comments have an owner we can further update the
schema to make owner a required field for all ``Owned`` objects.

.. code-block:: eschema

    abstract type Named:
        required property name -> str

    # Dictionary is a NamedObject variant, that enforces
    # name uniqueness across all instances if its subclass.
    abstract type Dictionary extending Named:
        required property name -> str:
            delegated constraint unique

    abstract type Text:
        # This is an abstract object containing text.
        required property text -> str:
            # let's limit the maximum length of text to 10000
            # characters.
            constraint maxlength(10000)

    type User extending Named
    # no need to specify 'link name' here anymore as it's inherited

    type Priority extending Dictionary

    type Status extending Dictionary

    type Comment extending Text, Owned:
        required link issue -> Issue:
            cardinality := '*1'
        property timestamp -> datetime:
            default := SELECT datetime::current_datetime()
            # the timestap will be automatically set to the current
            # time if it is not specified at the point of comment
            # creation

    #
    # just as before, no changes to the above types
    #

    abstract type Owned:
        # don't make the link owner required so that we can first
        # assign an owner to Comment objects already in the DB
        required link owner -> User:
            cardinality := '*1'

    type Issue extending Text, Owned:
        required link status -> Status
        link priority -> Priority
        # notice we no longer need to override the owner link

.. code-block:: edgeql

    CREATE MIGRATION example::d4
    FROM example::d3
    TO eschema $$
        # ... new schema goes here
    $$;
    COMMIT MIGRATION example::d4;

After several schema migrations and even a data migration we have
arrived at a state with reasonable amount of features for our issue
tracker EdgeDB backend. Now let's log a few more issues and run some
queries to analyze them.


Use cases
---------

Let's consider some of the possible interactions with the issue
tracker system, using both EdgeQL and GraphQL.

.. todo::

    needs more content

Analytics
---------

For running complex queries native EdgeQL is better suited than GraphQL.

.. todo::

    needs more content
