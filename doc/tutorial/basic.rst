========
Tutorial
========

Starting the Server
===================

To begin, start the EdgeDB server and open an interactive shell to it.

If you are using a Docker image, run:

.. code-block:: bash

    $ docker run -it --rm -v edgedb_data:/data \
        edgedb/edgedb-preview

If you've installed EdgeDB on your system directly, run:

.. code-block:: bash

    $ edgedb --start-server

Once the EdgeDB server is up, an interactive shell session will open,
connected to the default database:

.. code-block:: edgedb-repl

    edgedb>


Defining the Schema
===================

For the purpose of this tutorial let's imagine we are building a
platform for collaborative development.

To manipulate and query data in EdgeDB we must first define a schema.
We will be working with three object types: ``User``, ``PullRequest``,
and ``Comment``.  Let's define the initial schema with a migration:

.. eql:migration:: m1

    type User:
      required property login -> str:
        constraint unique
      required property firstname -> str
      required property lastname -> str

    type PullRequest:
      required property number -> int64:
        constraint unique
      required property title -> str
      required property body -> str
      required property status -> str
      required property created_on -> datetime
      required link author -> User
      link assignees -> User:
        cardinality := '**'
      link comments -> Comment:
        cardinality := '1*'

    type Comment:
      required property body -> str
      required link author -> User
      required property created_on -> datetime

With the above snippet we defined and applied a migration to a schema
described using the :ref:`declarative schema language <ref_eschema>`.
We created the three main object types, each with a number of properties
and links to other objects.

Notice how the ``PullRequest`` and the ``Comment`` types have
common properties: ``body`` and ``created_on`` as well as the ``author``
link.  Let's remove this duplication by declaring an abstract parent type
``AuthoredText`` and :ref:`extending <ref_datamodel_inheritance>`
``Comment`` and ``PullRequest`` from it:

.. eql:migration:: m2

    type User:
      required property login -> str:
        constraint unique
      required property firstname -> str
      required property lastname -> str

    # <new>
    abstract type AuthoredText:
      required property body -> str
      required link author -> User
      required property created_on -> datetime
    # </new>

    # <changed>
    type PullRequest extending AuthoredText:
    # </changed>
      required property title -> str
      required property status -> str
      link assignees -> User:
        cardinality := '**'
      link comments -> Comment:
        cardinality := '1*'

    type Comment extending AuthoredText


Inserting Data
==============

Now that we've defined the schema, let's create some users:

.. code-block:: edgeql

    INSERT User {
      login := 'alice',
      firstname := 'Alice',
      lastname := 'Liddell',
    };

    INSERT User {
      login := 'bob',
      firstname := 'Bob',
      lastname := 'Sponge',
    };

    INSERT User {
      login := 'carol',
      firstname := 'Carol',
      lastname := 'Danvers',
    };

    INSERT User {
      login := 'dave',
      firstname := 'Dave',
      lastname := 'Bowman',
    };


Then, a ``PullRequest`` object:

.. code-block:: edgeql

    WITH
      Alice := (SELECT User FILTER .login = "alice"),
      Bob := (SELECT User FILTER .login = "bob")
    INSERT PullRequest {
      number := 1,
      title := "Avoid attaching multiple scopes at once",
      status := "Merged",
      author := Alice,
      assignees := Bob,
      body := "Sublime Text and Atom handles multiple " +
              "scopes differently.",
      created_on := <datetime>"Feb 1, 2016, 5:29PM",
    };

"PR #1" has been commented on, let's update it with ``Comment`` objects:

.. code-block:: edgeql

    WITH
      Alice := (SELECT User FILTER .login = 'alice'),
      Bob := (SELECT User FILTER .login = 'bob')
    UPDATE PullRequest
    FILTER PullRequest.number = 1
    SET {
      comments := {
        (INSERT Comment {
          author := Alice,
          body :=
            "Sublime Text handles whitespace-" +
            "separated scope list, but Atom would " +
            "fail to do that.",
          created_on :=
            <datetime>'Feb 1, 2016, 5:31 PM UTC',
        }),
        (INSERT Comment {
          author := Bob,
          body := "Thanks for catching that.",
          created_on :=
            <datetime>'Feb 2, 2016, 12:47 PM UTC',
        }),
        (INSERT Comment {
          author := Alice,
          body := "You're welcome. Thanks for the " +
                  "awesome package!",
          created_on :=
            <datetime>'Feb 2, 2016, 12:48 PM UTC',
        }),
      }
    };


Let's create another PR, together with the corresponding comments:

.. code-block:: edgeql

    WITH
      Bob := (SELECT User FILTER .login = 'bob'),
      Carol := (SELECT User FILTER .login = 'carol'),
      Dave := (SELECT User FILTER .login = 'dave')
    INSERT PullRequest {
      number := 2,
      title := 'Pyhton -> Python',
      status := 'Open',
      author := Carol,
      assignees := {Bob, Dave},
      body := "Several typos fixed.",
      created_on :=
        <datetime>'Apr 25, 2016, 6:57 PM UTC',
      comments := {
        (INSERT Comment {
          author := Carol,
          body := "Couple of typos are fixed. " +
                  "Updated VS count.",
          created_on :=
            <datetime>'Apr 25, 2016, 6:58 PM UTC',
        }),
        (INSERT Comment {
          author := Bob,
          body := "Thanks for catching the typo.",
          created_on :=
           <datetime>'Apr 25, 2016, 7:11 PM UTC',
        }),
        (INSERT Comment {
          author := Dave,
          body := "Thanks!",
            created_on :=
              <datetime>'Apr 25, 2016, 7:22 PM UTC',
        }),
      }
    };


Querying Data
=============

Now that we inserted some data, let’s run some queries!

Get all "Open" pull requests, their authors, and who they are
assigned to, in reverse chronological order:

.. code-block:: edgeql

    SELECT
      PullRequest {
        title,
        created_on,
        author: {
          login
        },
        assignees: {
          fullname
        }
      }
    FILTER
      .status = "Open"
    ORDER BY
      .created_on DESC;
