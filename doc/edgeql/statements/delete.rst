Delete
------

``DELETE`` statement removes the specified set of objects from the
database. Therefore, a ``FILTER`` can be applied to the set being
removed, while the ``DELETE`` statement itself does not have a
``FILTER`` clause. Just like ``INSERT`` if used as an expression it
will return the set of removed objects.

The data flow of a ``DELETE`` block can be conceptualized like this:

.. code-block:: pseudo-eql

    WITH MODULE example

    DELETE
        <expr>  # delete the following objects

Here's a simple example of deleting a specific user:

.. code-block:: eql

    WITH MODULE example
    DELETE (SELECT User
            FILTER User.name = 'Alice Smith');

Notice that there are no other clauses in the ``DELETE`` statement.
This is because it is a mutation statement and not typically used to
query the DB.
