.. _ref_eql_ddl_props:

==========
Properties
==========

This section describes the DDL commands pertaining to
:ref:`properties <ref_datamodel_props>`.


CREATE ABSTRACT PROPERTY
=============================

.. eql:statement:: CREATE ABSTRACT PROPERTY
    :haswith:

    Define a new :ref:`abstract property <ref_datamodel_props>`.

    .. eql:synopsis::

        [ WITH <with-item> [, ...] ]
        CREATE ABSTRACT PROPERTY <name> [ EXTENDING <base> [, ...] ]
        [ \{ <action>; [...] \} ]
        ;

    Description
    -----------

    ``CREATE ABSTRACT PROPERTY`` defines a new abstract property
    item.

    If *name* is qualified with a module name, then the property item
    is created in that module, otherwise it is created in the current module.
    The property name must be distinct from that of any existing schema
    item in the module.

    .. eql:clause:: EXTENDING: EXTENDING <base> [, ...]

        Optional clause specifying the *parents* of the new property item.

        Use of ``EXTENDING`` creates a persistent schema relationship
        between the new property and its parents.  Schema modifications
        to the parent(s) propagate to the child.

    .. eql:clause:: ACTION: action

        The following actions are allowed in the
        ``CREATE ABSTRACT PROPERTY`` block:

        ``SET <attribute> := <value>;``
            Set link item's *attribute* to *value*.
            See :eql:stmt:`SET <SET ATTRIBUTE>` for details.


ALTER ABSTRACT PROPERTY
=======================

.. eql:statement:: ALTER ABSTRACT PROPERTY
    :haswith:

    Change the definition of an
    :ref:`abstract property <ref_datamodel_props>`.

    .. eql:synopsis::

        [ WITH <with-item> [, ...] ]
        ALTER ABSTRACT PROPERTY <name>
        \{ <action>; [...] \};

    Description
    -----------

    ``ALTER ABSTRACT PROPERTY`` changes the definition of an abstract
    property item.  *name* must be a name of an existing abstract
    property, optionally qualified with a module name.

    .. eql:clause:: ACTION: action

        The following actions are allowed in the
        ``ALTER ABSTRACT PROPERTY`` block:

        :eql:inline-synopsis:`RENAME TO <newname>;`
            Change the name of the property item to *newname*.  All
            concrete link properties inheriting from this property are
            also renamed.

        :eql:inline-synopsis:`EXTENDING ...`
            Alter the property parent list.
            The full syntax of this action is:

            .. eql:synopsis::

                 EXTENDING <name> [, ...]
                    [ FIRST | LAST | BEFORE <parent> | AFTER <parent> ]

            This action makes the property item a child of the specified
            list of parent property items.  The requirements for the
            parent-child relationship are the same as when creating
            a property.

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
            Change the target type of the property to the specified type.

        :eql:inline-synopsis:`CREATE CONSTRAINT <constraint-name> ...`
            Define a new constraint for this property.
            See :eql:stmt:`CREATE CONSTRAINT` for details.

        :eql:inline-synopsis:`ALTER CONSTRAINT <constraint-name> ...`
            Alter the definition of a constraint for this property.
            See :eql:stmt:`ALTER CONSTRAINT` for details.

        :eql:inline-synopsis:`DROP CONSTRAINT <constraint-name>;`
            Remove a constraint from this property.
            See :eql:stmt:`DROP CONSTRAINT` for details.


DROP ABSTRACT PROPERTY
======================

.. eql:statement:: DROP ABSTRACT PROPERTY
    :haswith:

    Remove an :ref:`abstract property <ref_datamodel_props>` from the
    schema.

    .. eql:synopsis::

        [ WITH <with-item> [, ...] ]
        DROP ABSTRACT PROPERTY <name>;


    Description
    -----------

    ``DROP ABSTRACT PROPERTY`` removes an existing property item
    from the database schema.


    Examples
    --------

    Drop the abstract property ``rank``:

    .. code-block:: edgeql

        DROP ABSTRACT PROPERTY rank;


CREATE PROPERTY
====================

.. eql:statement:: CREATE PROPERTY

    Define a concrete property on the specified link.

    .. eql:synopsis::

        CREATE [ INHERITED ] PROPERTY <name> TO <typename>
        [ \{ <action>; [...] \} ]
        ;

        CREATE [ INHERITED ] PROPERTY <name> := <expression>;

    Description
    -----------

    ``CREATE PROPERTY`` defines a new concrete property for a
    given link.

    There are two forms of ``CREATE PROPERTY``, as shown in the syntax
    synopsis above.  The first form is the canonical definition form, and
    the second form is a syntax shorthand for defining a
    :ref:`computable property <ref_datamodel_computables>`.


    Canonical Form
    --------------

    The canonical form of ``CREATE PROPERTY`` defines a concrete
    property with the given *name* and referring to the *typename* type.

    The ``INHERITED`` keyword is required when the containing link
    has parents with the same link proeprty name, or when there is an
    abstract property with the same name defined in the same module
    as the containing link.  *Inherited* link properties form a persistent
    connections in the schema.  Schema modifications to parent link properties
    propagate to the child property.

    .. eql:clause:: ACTION: action

        The following actions are allowed in the
        ``CREATE PROPERTY`` block:

        :eql:inline-synopsis:`SET <attribute> := <value>;`
            Set link item's *attribute* to *value*.
            See :eql:stmt:`SET <SET ATTRIBUTE>` for details.


    Computable Link Form
    --------------------

    The computable form of ``CREATE PROPERTY`` defines a concrete
    *computable* property with the given *name*.  The type of the
    link is inferred from the *expression*.  The ``INHERITED`` keyword
    has the same meaning as in the canonical form.


ALTER PROPERTY
===================

.. eql:statement:: ALTER PROPERTY

    Alter the definition of a concrete property on the specified link.

    .. eql:synopsis::

        ALTER PROPERTY <name>
        \{ <action>; [...] \}
        ;

        ALTER PROPERTY <name> <action>;


    Description
    -----------

    There are two forms of ``ALTER LINK``, as shown in the synopsis above.
    The first is the canonical form, which allows specifying multiple
    alter actions, while the second form is a shorthand for a single
    alter action.

    .. eql:clause:: ACTION: action

        The following actions are allowed in the
        ``ALTER PROPERTY`` block:

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

        :eql:inline-synopsis:`CREATE PROPERTY <property-name> ...`
            Define a new property item for this link.  See
            :eql:stmt:`CREATE PROPERTY` for details.

        :eql:inline-synopsis:`ALTER PROPERTY <property-name> ...`
            Alter the definition of a property item for this link.  See
            :eql:stmt:`ALTER PROPERTY` for details.

        :eql:inline-synopsis:`DROP PROPERTY <property-name>;`
            Remove a property item from this link.  See
            :eql:stmt:`DROP PROPERTY` for details.

    Examples
    --------

    Set the ``title`` attribute of property ``rank`` of abstract
    link ``favorites`` to ``"Rank"``:

    .. code-block:: edgeql

        ALTER ABSTRACT LINK favorites {
            ALTER PROPERTY rank SET title := "Rank";
        };


DROP PROPERTY
==================

.. eql:statement:: DROP PROPERTY

    Remove a concrete property from the specified link.

    .. eql:synopsis::

        DROP PROPERTY <name>;

    Description
    -----------

    ``DROP PROPERTY`` removes the specified property from its
    containing link.  All link properties that inherit from this link
    property are also removed.

    Examples
    --------

    Remove property ``rank`` from abstract link ``favorites``:

    .. code-block:: edgeql

        ALTER ABSTRACT LINK favorites {
            DROP PROPERTY rank;
        };
