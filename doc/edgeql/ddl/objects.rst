.. _ref_eql_ddl_object_types:

Object Types
============

.. eql:statement:: CREATE TYPE
    :haswith:

    Define a new :ref:`object type <ref_datamodel_object_types>`.

    .. eql:synopsis::

        [ WITH <with-item> [, ...] ]
        CREATE [ABSTRACT] TYPE <name> [ EXTENDING <base> [, ...] ]
        [ \{ <action>; [...] \} ];

    Description
    -----------

    ``CREATE TYPE`` defines a new object type for use in the current database.

    If *name* is qualified with a module name, then the type is created
    in that module, otherwise it is created in the current module.
    The type name must be distinct from that of any existing schema item
    in the module.

    If the ``ABSTRACT`` keyword is specified, the created type will be
    *abstract*.

    .. eql:clause:: EXTENDING: EXTENDING <base> [, ...]

        Optional clause specifying the *supertypes* of the new type.

        Use of ``EXTENDING`` creates a persistent type relationship
        between the new subtype and its supertype(s).  Schema modifications
        to the supertype(s) propagate to the subtype.

        References to supertypes in queries will also include objects of
        the subtype.

        If the same *link* name exists in more than one supertype, or
        is explicitly defined in the subtype and at least one supertype,
        then the data types of the link targets must be *compatible*.
        If there is no conflict, the links are merged to form a single
        link in the new type.

    .. eql:clause:: ACTION: action

        Optional sequence of subdefinitions related to the new object type.

        The following subdefinitions are allowed in the ``CREATE TYPE``
        block:

        :eql:inline-synopsis:`SET <attribute> := <value>;`
            Set link item's *attribute* to *value*.
            See :eql:stmt:`SET <SET ATTRIBUTE>` for details.

        :eql:inline-synopsis:`CREATE LINK`
            Define a concrete link on the object type.
            See :eql:stmt:`CREATE LINK` for details.
