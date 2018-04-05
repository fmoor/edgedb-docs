.. _ref_edgeql_statements:


Statements
==========

Statements in EdgeQL are a kind of an *expression* that has one or
more ``clauses`` and is used to retrieve or modify data in a database.

Query statements:

* Select_

    Retrieve data from a database and compute arbitrary expressions

* For_

    Compute an expression for every element of an input set and
    concatenate the results

Data modification statements:

* Insert_

    Create new data in a database

* Update_

    Update data in a database

* Delete_

    Remove data from a database


Statements in EdgeQL represent an atomic interaction with the DB. From
the point of view of a statement all side-effects (such as DB updates)
happen after the statement is executed. So as far as each statement is
concerned, it is some purely functional expression evaluated on some
specific input (DB state).

Statements consist of building blocks called `clauses`. Each `clause`
can be represented as an equivalent set function of a certain
signature. Understanding :ref:`how functions
work<ref_edgeql_fundamentals_function>` helps in understanding
`clauses`. A statement is effectively a data pipeline made out of
`clauses`. Unlike functions and operators `clauses` cannot be
arbitrarily mixed, but must follow specific patterns. EdgeQL has
Select_, Group_, For_, Insert_, Update_, and Delete_ statements for
managing the data in the DB. Each of these statements can also be used
as an *expression* if it is enclosed in parentheses, in which case
they also return a value.

.. note::

    Running ``INSERT`` and other DML statements bare in repl yields
    the cardinality of the affected set.

Every statement starts with an optional :ref:`with block<ref_edgeql_with>`.
A ``WITH`` block defines symbols that can be used in the rest of the
statement. To keep things simple, in the examples below ``WITH`` block
is only used to define a default ``MODULE``. It is not necessary
because every ``concept`` can be referred to by a fully qualified name
(e.g. ``example::User``), but specifying a default ``MODULE`` makes it
possible to just use short names (e.g. ``User``).
