.. _ref_eql_ddl_indexes:

=======
Indexes
=======

This section describes the DDL commands pertaining to
:ref:`indexes <ref_datamodel_indexes>`.


CREATE INDEX
============

.. eql:statement:: CREATE INDEX

    Define an new :ref:`index <ref_datamodel_indexes>` for a given object
    type or link.

    .. eql:synopsis::

        CREATE INDEX <index-name> := <index-expr>;

        CREATE INDEX <index-name> \{
            SET expr := <index-expr>;
            [ <action >; ... ]
        \};


    Description
    -----------

    ``CREATE INDEX`` constructs a new index *index-name* for a given object
    type or link using *index-expr*.


    Parameters
    ----------

    :eql:inline-synopsis:`<index-name>`
        The name of the index to be created.  No module name can be specified,
        indexes are always created in the same module as the parent type or
        link.


    Examples
    --------

    Create an object type ``User`` and set its ``title`` attribute to
    ``"User type"``.

    .. code-block:: edgeql

        CREATE TYPE User {
            SET title := 'User type';
        };


DROP INDEX
==========

.. eql:statement:: DROP INDEX

    Remove an attribute value from a given schema item.

    .. eql:synopsis::

        DROP ATTRIBUTE <attribute>;

    Description
    -----------

    ``DROP ATTRIBUTE`` removes an attribute value from a schema item.

    *attribute* refers to the name of a defined attribute.  The attribute
    value does not have to exist on a schema item.

    This statement can only be used as a subdefinition in another
    DDL statement.


    Examples
    --------

    Drop the ``title`` attribute from the ``User`` object type:

    .. code-block:: edgeql

        ALTER TYPE User {
            DROP ATTRIBUTE title;
        };
