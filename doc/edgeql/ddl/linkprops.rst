.. _ref_eql_ddl_lprops:

===============
Link Properties
===============

This section describes the DDL commands pertaining to
:ref:`link properties <ref_datamodel_linkprops>`.


CREATE ABSTRACT LINK PROPERTY
=============================

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
============================

.. eql:statement:: ALTER ABSTRACT LINK PROPERTY
    :haswith:

    Change the definition of an
    :ref:`abstract link property <ref_datamodel_linkprops>`.

    .. eql:synopsis::

        [ WITH <with-item> [, ...] ]
        ALTER ABSTRACT LINK PROPERTY <name>
        \{ <action>; [...] \};

    Description
    -----------

    ``ALTER ABSTRACT LINK PROPERTY`` changes the definition of an abstract
    link property item.  *name* must be a name of an existing abstract
    link property, optionally qualified with a module name.

    .. eql:clause:: ACTION: action

        The following actions are allowed in the
        ``ALTER ABSTRACT LINK PROPERTY`` block:

        :eql:inline-synopsis:`RENAME TO <newname>;`
            Change the name of the link property item to *newname*.  All
            concrete link properties inheriting from this link property are
            also renamed.

        :eql:inline-synopsis:`EXTENDING ...`
            Alter the link property parent list.
            The full syntax of this action is:

            .. eql:synopsis::

                 EXTENDING <name> [, ...]
                    [ FIRST | LAST | BEFORE <parent> | AFTER <parent> ]

            This action makes the link property item a child of the specified
            list of parent link property items.  The requirements for the
            parent-child relationship are the same as when creating
            a link property.

            It is possible to specify the position in the parent list
            using the following optional keywords:

            * ``FIRST`` -- insert parent(s) at the beginning of the
              parent list,
            * ``LAST`` -- insert parent(s) at the end of the parent list,
            * ``BEFORE <parent>`` -- insert parent(s) before an
              existing *parent*,
            * ``AFTER <parent>`` -- insert parent(s) after an existing
              *parent*.

        :eql:inline-synopsis:`SET <attribute> := <value>;`
            Set link item's *attribute* to *value*.
            See :eql:stmt:`SET <SET ATTRIBUTE>` for details.

        :eql:inline-synopsis:`DROP ATTRIBUTE <attribute>;`
            Remove link item's *attribute* to *value*.
            See :eql:stmt:`DROP ATTRIBUTE <DROP ATTRIBUTE VALUE>` for details.

        :eql:inline-synopsis:`ALTER TARGET <typename>`
            Change the target type of the link property to the specified type.

        :eql:inline-synopsis:`CREATE CONSTRAINT <constraint-name> ...`
            Define a new constraint for this link property.
            See :eql:stmt:`CREATE CONSTRAINT` for details.

        :eql:inline-synopsis:`ALTER CONSTRAINT <constraint-name> ...`
            Alter the definition of a constraint for this link property.
            See :eql:stmt:`ALTER CONSTRAINT` for details.

        :eql:inline-synopsis:`DROP CONSTRAINT <constraint-name>;`
            Remove a constraint from this link property.
            See :eql:stmt:`DROP CONSTRAINT` for details.


DROP ABSTRACT LINK PROPERTY
===========================

.. eql:statement:: DROP ABSTRACT LINK PROPERTY
    :haswith:

    Remove an :ref:`abstract link property <ref_datamodel_linkprops>` from the
    schema.

    .. eql:synopsis::

        [ WITH <with-item> [, ...] ]
        DROP ABSTRACT LINK PROPERTY <name>;


    Description
    -----------

    ``DROP ABSTRACT LINK PROPERTY`` removes an existing link property item
    from the database schema.


    Examples
    --------

    Drop the abstract link property ``rank``:

    .. code-block:: edgeql

        DROP ABSTRACT LINK PROPERTY rank;


CREATE LINK PROPERTY
====================

.. eql:statement:: CREATE LINK PROPERTY

    Define a concrete link property on the specified link.

    .. eql:synopsis::

        CREATE [ INHERITED ] LINK PROPERTY <name> TO <typename>
        [ \{ <action>; [...] \} ]
        ;

        CREATE [ INHERITED ] LINK PROPERTY <name> := <expression>;

    Description
    -----------

    ``CREATE LINK PROPERTY`` defines a new concrete link property for a
    given link.

    There are two forms of ``CREATE LINK PROPERTY``, as shown in the syntax
    synopsis above.  The first form is the canonical definition form, and
    the second form is a syntax shorthand for defining a
    :ref:`computable link property <ref_datamodel_computables>`.


    Canonical Form
    --------------

    The canonical form of ``CREATE LINK PROPERTY`` defines a concrete
    link property with the given *name* and referring to the *typename* type.

    The ``INHERITED`` keyword is required when the containing link
    has parents with the same link proeprty name, or when there is an
    abstract link property with the same name defined in the same module
    as the containing link.  *Inherited* link properties form a persistent
    connections in the schema.  Schema modifications to parent link properties
    propagate to the child link property.

    .. eql:clause:: ACTION: action

        The following actions are allowed in the
        ``CREATE LINK PROPERTY`` block:

        :eql:inline-synopsis:`SET <attribute> := <value>;`
            Set link item's *attribute* to *value*.
            See :eql:stmt:`SET <SET ATTRIBUTE>` for details.


    Computable Link Form
    --------------------

    The computable form of ``CREATE LINK PROPERTY`` defines a concrete
    *computable* link property with the given *name*.  The type of the
    link is inferred from the *expression*.  The ``INHERITED`` keyword
    has the same meaning as in the canonical form.


ALTER LINK PROPERTY
===================

.. eql:statement:: ALTER LINK PROPERTY

    Alter the definition of a concrete link property on the specified link.

    .. eql:synopsis::

        ALTER LINK PROPERTY <name>
        \{ <action>; [...] \}
        ;

        ALTER LINK PROPERTY <name> <action>;


    Description
    -----------

    There are two forms of ``ALTER LINK``, as shown in the synopsis above.
    The first is the canonical form, which allows specifying multiple
    alter actions, while the second form is a shorthand for a single
    alter action.

    .. eql:clause:: ACTION: action

        The following actions are allowed in the
        ``ALTER LINK PROPERTY`` block:

        :eql:inline-synopsis:`RENAME TO <newname>;`
            Change the name of the concrete link to *newname*.  Renaming
            *inherited* links is not allowed, only non-inherited concrete
            links can be renamed.  When a concrete or abstract link is
            renamed, all concrete links that inherit from it are also
            renamed.

        :eql:inline-synopsis:`SET <attribute> := <value>;`
            Set link item's *attribute* to *value*.
            See :eql:stmt:`SET <SET ATTRIBUTE>` for details.

        :eql:inline-synopsis:`DROP ATTRIBUTE <attribute>;`
            Remove link item's *attribute* to *value*.
            See :eql:stmt:`DROP ATTRIBUTE <DROP ATTRIBUTE VALUE>` for details.

        :eql:inline-synopsis:`CREATE LINK PROPERTY <property-name> ...`
            Define a new link property item for this link.  See
            :eql:stmt:`CREATE LINK PROPERTY` for details.

        :eql:inline-synopsis:`ALTER LINK PROPERTY <property-name> ...`
            Alter the definition of a link property item for this link.  See
            :eql:stmt:`ALTER LINK PROPERTY` for details.

        :eql:inline-synopsis:`DROP LINK PROPERTY <property-name>;`
            Remove a link property item from this link.  See
            :eql:stmt:`DROP LINK PROPERTY` for details.

    Examples
    --------

    Set the ``title`` attribute of link property ``rank`` of abstract
    link ``favorites`` to ``"Rank"``:

    .. code-block:: edgeql

        ALTER ABSTRACT LINK favorites {
            ALTER LINK PROPERTY rank SET title := "Rank";
        };


DROP LINK PROPERTY
==================

.. eql:statement:: DROP LINK PROPERTY

    Remove a concrete link property from the specified link.

    .. eql:synopsis::

        DROP LINK PROPERTY <name>;

    Description
    -----------

    ``DROP LINK PROPERTY`` removes the specified link property from its
    containing link.  All link properties that inherit from this link
    property are also removed.

    Examples
    --------

    Remove link property ``rank`` from abstract link ``favorites``:

    .. code-block:: edgeql

        ALTER ABSTRACT LINK favorites {
            DROP LINK PROPERTY rank;
        };
