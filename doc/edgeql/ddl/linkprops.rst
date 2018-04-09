.. _ref_eql_ddl_lprops:

Link Properties
===============

This section describes the DDL commands pertaining to
:ref:`link properties <ref_datamodel_linkprops>`.


CREATE ABSTRACT LINK PROPERTY
-----------------------------

.. eql:statement:: CREATE ABSTRACT LINK PROPERTY
    :haswith:

    Define a new :ref:`abstract link property <ref_datamodel_linkprops>`.

    .. eql:synopsis::

        [ WITH <with-item> [, ...] ]
        CREATE ABSTRACT LINK PROPERTY <name> [ EXTENDING <base> [, ...] ]
        [ \{ <action>; [...] \} ]
        ;

    Description
    -----------

    ``CREATE ABSTRACT LINK PROPERTY`` defines a new abstract link property
    item.

    If *name* is qualified with a module name, then the link property item
    is created in that module, otherwise it is created in the current module.
    The link property name must be distinct from that of any existing schema
    item in the module.

    .. eql:clause:: EXTENDING: EXTENDING <base> [, ...]

        Optional clause specifying the *parents* of the new link property item.

        Use of ``EXTENDING`` creates a persistent schema relationship
        between the new link property and its parents.  Schema modifications
        to the parent(s) propagate to the child.

    .. eql:clause:: ACTION: action

        The following actions are allowed in the
        ``CREATE ABSTRACT LINK PROPERTY`` block:

        ``SET <attribute> := <value>;``
            Set link item's *attribute* to *value*.
            See :eql:stmt:`SET <SET ATTRIBUTE>` for details.


ALTER ABSTRACT LINK PROPERTY
----------------------------

.. eql:statement:: ALTER ABSTRACT LINK PROPERTY
    :haswith:

    Change the definition of an
    :ref:`abstract link property <ref_datamodel_linkprops>`.

    .. eql:synopsis::

        [ WITH <with-item> [, ...] ]
        ALTER ABSTRACT LINK PROPERTY <name>
        \{ <action>; [...] \}
        ;

    .. eql:clause:: ACTION: action

        The following actions are allowed in the
        ``ALTER ABSTRACT LINK PROPERTY`` block:

        ``RENAME TO <newname>;``
            Change the name of the link property item to *newname*.  All
            concrete link properties inheriting from this link property are
            also renamed.

        ``EXTENDING <name> [, ...] [ FIRST | LAST | BEFORE <parent> | AFTER <parent> ]``
            This action makes the link property item a child of the specified
            list of parent link property items, *in addition* to the existing
            parents.  The requirements for the parent-child relationship are
            the same as when creating a link property.

            It is possible to specify the position in the parent list
            using the following optional keywords:

            * ``FIRST``: insert parent(s) at the beginning of the parent list,
            * ``LAST``: insert parent(s) at the end of the parent list,
            * ``BEFORE <parent>``: insert parent(s) before an existing *parent*,
            * ``AFTER <parent>``: insert parent(s) after an existing *parent*.

        ``SET <attribute> := <value>;``
            Set link item's *attribute* to *value*.
            See :eql:stmt:`SET <SET ATTRIBUTE>` for details.

        ``DROP ATTRIBUTE <attribute>;``
            Remove link item's *attribute* to *value*.
            See :eql:stmt:`DROP ATTRIBUTE <DROP ATTRIBUTE VALUE>` for details.

        ``CREATE LINK PROPERTY <property-name> [ \{ <subactions> \} ]``
            Define a new link property item for this link.  See
            :eql:stmt:`CREATE LINK PROPERTY` for details.

        ``ALTER LINK PROPERTY <property-name> \{ <subactions> \}``
            Alter the definition of a link property item for this link.  See
            :eql:stmt:`ALTER LINK PROPERTY` for details.

        ``DROP LINK PROPERTY <property-name> \{ <subactions> \}``
            Remove a link property item from this link.  See
            :eql:stmt:`DROP LINK PROPERTY` for details.

        ``CREATE CONSTRAINT <constraint-name> [ (<arguments>) ] [ \{ <subactions> \} ]``
            Define a new constraint for this link.  See
            :eql:stmt:`CREATE CONSTRAINT` for details.

        ``ALTER CONSTRAINT <constraint-name> \{ <subactions> \}``
            Alter the definition of a constraint for this link.  See
            :eql:stmt:`ALTER CONSTRAINT` for details.

        ``DROP CONSTRAINT <constraint-name>``
            Remove a constraint from this link.  See
            :eql:stmt:`DROP CONSTRAINT` for details.


CREATE LINK PROPERTY
--------------------

.. eql:statement:: CREATE LINK PROPERTY

    Define a concrete link property on the specified link.


ALTER LINK PROPERTY
-------------------

.. eql:statement:: ALTER LINK PROPERTY

    Alter the definition of a concrete link property on the specified link.


DROP LINK PROPERTY
------------------

.. eql:statement:: DROP LINK PROPERTY

    Remove a concrete link property from the specified link.
