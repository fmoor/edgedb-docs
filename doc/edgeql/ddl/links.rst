.. _ref_eql_ddl_links:

=====
Links
=====

This section describes the DDL commands pertaining to
:ref:`links <ref_datamodel_links>`.


CREATE ABSTRACT LINK
====================

.. eql:statement:: CREATE ABSTRACT LINK
    :haswith:

    Define a new :ref:`abstract link <ref_datamodel_links>`.

    .. eql:synopsis::

        [ WITH <with-item> [, ...] ]
        CREATE ABSTRACT LINK <name> [ EXTENDING <base> [, ...] ]
        [ \{ <action>; [...] \} ];

    Description
    -----------

    ``CREATE ABSTRACT LINK`` defines a new abstract link item.

    If *name* is qualified with a module name, then the link item is created
    in that module, otherwise it is created in the current module.
    The link name must be distinct from that of any existing schema item
    in the module.

    .. eql:clause:: EXTENDING: EXTENDING <base> [, ...]

        Optional clause specifying the *parents* of the new link item.

        Use of ``EXTENDING`` creates a persistent schema relationship
        between the new link and its parents.  Schema modifications
        to the parent(s) propagate to the child.

        If the same *link property* name exists in more than one parent, or
        is explicitly defined in the new link and at least one parent,
        then the data types of the link property targets must be *compatible*.
        If there is no conflict, the link properties are merged to form a
        single link property in the new link item.

    .. eql:clause:: ACTION: action

        The following actions are allowed in the
        ``CREATE ABSTRACT LINK`` block:

        :eql:inline-synopsis:`SET <attribute> := <value>;`
            Set link item's *attribute* to *value*.
            See :eql:stmt:`SET <SET ATTRIBUTE>` for details.

        :eql:inline-synopsis:`CREATE LINK PROPERTY`
            Define a concrete link property on the link.
            See :eql:stmt:`CREATE LINK PROPERTY` for details.

        :eql:inline-synopsis:`CREATE CONSTRAINT`
            Define a concrete constraint on the link.
            See :eql:stmt:`CREATE CONSTRAINT` for details.


ALTER ABSTRACT LINK
===================

.. eql:statement:: ALTER ABSTRACT LINK
    :haswith:

    Change the definition of an :ref:`abstract link <ref_datamodel_links>`.

    .. eql:synopsis::

        [ WITH <with-item> [, ...] ]
        ALTER ABSTRACT LINK <name>
        \{ <action>; [...] \}
        ;


    Description
    -----------

    ``ALTER ABSTRACT LINK`` changes the definition of an abstract link item.
    *name* must be a name of an existing abstract link, optionally qualified
    with a module name.

    .. eql:clause:: ACTION: action

        The following actions are allowed in the
        ``ALTER ABSTRACT LINK`` block:

        :eql:inline-synopsis:`RENAME TO <newname>;`
            Change the name of the link item to *newname*.  All concrete links
            inheriting from this links are also renamed.

        :eql:inline-synopsis:`EXTENDING ...`
            Alter the link parent list.  The full syntax of this action is:

            .. eql:synopsis::

                 EXTENDING <name> [, ...]
                    [ FIRST | LAST | BEFORE <parent> | AFTER <parent> ]

            This action makes the link item a child of the specified list
            of parent link items.  The requirements for the parent-child
            relationship are the same as when creating a link.

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

        :eql:inline-synopsis:`CREATE LINK PROPERTY <property-name> ...`
            Define a new link property item for this link.  See
            :eql:stmt:`CREATE LINK PROPERTY` for details.

        :eql:inline-synopsis:`ALTER LINK PROPERTY <property-name> ...`
            Alter the definition of a link property item for this link.  See
            :eql:stmt:`ALTER LINK PROPERTY` for details.

        :eql:inline-synopsis:`DROP LINK PROPERTY <property-name>;`
            Remove a link property item from this link.  See
            :eql:stmt:`DROP LINK PROPERTY` for details.

        :eql:inline-synopsis:`CREATE CONSTRAINT <constraint-name> ...`
            Define a new constraint for this link.  See
            :eql:stmt:`CREATE CONSTRAINT` for details.

        :eql:inline-synopsis:`ALTER CONSTRAINT <constraint-name> ...`
            Alter the definition of a constraint for this link.  See
            :eql:stmt:`ALTER CONSTRAINT` for details.

        :eql:inline-synopsis:`DROP CONSTRAINT <constraint-name>;`
            Remove a constraint from this link.  See
            :eql:stmt:`DROP CONSTRAINT` for details.


DROP ABSTRACT LINK
==================

.. eql:statement:: DROP ABSTRACT LINK
    :haswith:

    Remove an :ref:`abstract link <ref_datamodel_links>` from the schema.

    .. eql:synopsis::

        [ WITH <with-item> [, ...] ]
        DROP ABSTRACT LINK <name>;


    Description
    -----------

    ``DROP ABSTRACT LINK`` removes an existing link item from the database
    schema.  All subordinate schema items defined on this link, such
    as link properties and constraints, are removed as well.


    Examples
    --------

    Drop the link ``friends``:

    .. code-block:: edgeql

        DROP ABSTRACT LINK friends;


CREATE LINK
===========

.. eql:statement:: CREATE LINK
    :haswith:

    Define a new :ref:`concrete link <ref_datamodel_links>` for the
    specified *object type*.

    .. eql:synopsis::

        CREATE [ REQUIRED ] [ INHERITED ] LINK <name> TO <typename>
        [ \{ <action>; [...] \} ]
        ;

        CREATE [ INHERITED ] LINK <name> := <expression>;

    Description
    -----------

    ``CREATE LINK`` defines a new concrete link for a given object type.

    There are two forms of ``CREATE LINK``, as shown in the syntax synopsis
    above.  The first form is the canonical definition form, and the second
    form is a syntax shorthand for defining a
    :ref:`computable link <ref_eql_datamodel_computables>`.


    Canonical Form
    --------------

    The canonical form of ``CREATE LINK`` defines a concrete link *name*
    referring to the *typename* type.  If the optional ``REQUIRED``
    keyword is specified, the link is considered required.

    The ``INHERITED`` keyword is required when the containing object type
    has supertypes with the same link name, or when there is an abstract
    link with the same name defined in the same module as the containing
    object type.  *Inherited* links form a persistent connections in the
    schema.  Schema modifications to parent links propagate to the child
    link.

    .. eql:clause:: ACTION: action

        The following actions are allowed in the ``CREATE LINK`` block:

        * :eql:stmt:`SET <SET ATTRIBUTE>`


    Computable Link Form
    --------------------

    The computable form of ``CREATE LINK`` defines a concrete *computable*
    link *name*.  The type of the link is inferred from the *expression*.



ALTER LINK
==========

.. eql:statement:: ALTER LINK
    :haswith:

    Change the definition of a :ref:`concrete link <ref_datamodel_links>`
    on a given object type.

    .. eql:synopsis::

        ALTER LINK <name>
        \{ <action>; [...] \}
        ;

        ALTER LINK <name> <action>;


    Description
    -----------

    There are two forms of ``ALTER LINK``, as shown in the synopsis above.
    The first is the canonical form, which allows specifying multiple
    alter actions, while the second form is a shorthand for a single
    alter action.

    .. eql:clause:: ACTION: action

        The following actions are allowed in the
        ``ALTER LINK`` block:

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

        :eql:inline-synopsis:`CREATE CONSTRAINT <constraint-name> ...`
            Define a new constraint for this link.  See
            :eql:stmt:`CREATE CONSTRAINT` for details.

        :eql:inline-synopsis:`ALTER CONSTRAINT <constraint-name> ...`
            Alter the definition of a constraint for this link.  See
            :eql:stmt:`ALTER CONSTRAINT` for details.

        :eql:inline-synopsis:`DROP CONSTRAINT <constraint-name>;`
            Remove a constraint from this link.  See
            :eql:stmt:`DROP CONSTRAINT` for details.
