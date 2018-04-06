.. _ref_datamodel_links:

=====
Links
=====

Link items define a specific relationship between two object types.  Link
instances relate one *object* to one or more different objects.

There are two kinds of link item declarations: *abstract links*,
and *concrete links*.  Abstract links are defined on module level and are not
tied to any particular object type.  Concrete links are defined on specific
object types.  Concrete links automatically extend abstract links with the
same name in the same module.


Definition
==========

Abstract Links
--------------

An *abstract link* may be defined in EdgeDB Schema using the ``abstract link``
declaration:

.. code-block:: pseudo-eql

    abstract link <link_name> [ extending [(] <parent_link> [, ...] [)]]:
        [ <property_declarations> ]
        [ <attribute_declarations> ]

Parameters:

    :eql:inline-synopsis:`<link_name>`
        Specifies the name of the link item.  Customarily, link type names
        are lowercase, with words separated by underscores as necessary for
        readability.

    :eql:inline-synopsis:`extending <parent_link> [, ...]`
        If specified, declares the *parents* of the link item.

        Use of ``extending`` creates a persistent schema relationship
        between this link and its parents.  Schema modifications
        to the parent(s) propagate to the child.

        If the same *property* name exists in more than one parent, or
        is explicitly defined in the new link and at least one parent,
        then the data types of the property targets must be *compatible*.
        If there is no conflict, the link properties are merged to form a
        single property in the new link item.

    :eql:inline-synopsis:`<property_declarations>`
        :ref:`Property <ref_datamodel_props>` declarations.

    :eql:inline-synopsis:`<constraint_declarations>`
        :ref:`Constraint <ref_datamodel_constraints>` declarations.

    :eql:inline-synopsis:`<attribute_declarations>`
        :ref:`Schema attribute <ref_datamodel_attributes>` declarations.


Abstract links can also be defined using the :eql:stmt:`CREATE ABSTRACT LINK`
EdgeQL command.


Concrete Links
--------------

A *concrete link* may be defined in EdgeDB Schema using the ``link``
declaration in the context of a ``type`` declaration:

.. code-block:: pseudo-eql

    type <TypeName>:
        [required] [readonly] [inherited] link <link_name>:
            [ cardinality := {'11' | '1*' | '*1' | '**'} ]
            [ expr := <computable_expr> ]
            [ default := <default_expr> ]
            [ <attribute_declarations> ]

    shorthand form for computable link declaration:

    type <TypeName>:
        [inherited] link <link_name> := <computable_expr>


Parameters:
    :eql:inline-synopsis:`required`
        If specified, the link is considered *required* for the parent
        object type.  It is an error for an object to have a required
        link resolve to an empty value.  Child links **always** inherit
        the *required* attribute, i.e it is not possible to make a
        required link non-required by extending it.

    :eql:inline-synopsis:`readonly`
        If specified, the link is considered *read-only*.  Modifications
        of this link are prohibited once an object is created.

    :eql:inline-synopsis:`cardinality := <cardinality>`
        Specifies the *cardinality* of this link, which, in order of
        decreasing strictness, can be one of:

        - ``'11'`` ("one-to-one") -- object may refer to exactly one other
          object, and the referred object cannot be referred to by any other
          object using this link.

        - ``'1*'`` ("one-to-many") -- object may refer to multiple objects,
          and the referred objects cannot be referred to by any other object
          using this link.

        - ``'*1'`` ("many-to-one") -- object may refer to exactly one other
          object, and the other object may be referred to by other objects
          using this link.  *This is the default*.

        - ``'**'`` ("many-to-many") -- object may refer to multiple other
          objects and the referred objects may be referred to by other objects
          using this link.

    :eql:inline-synopsis:`<computable_expr>`
        If specified, designates this link as a *computable link*
        (see :ref:`Computables <ref_datamodel_computables>`).  A computable
        link cannot be *required* or *readonly* (the latter is implied and
        always true).  There is a shorthand form using the ``:=`` syntax,
        as shown in the synopsis above.

    :eql:inline-synopsis:`<attribute_declarations>`
        :ref:`Schema attribute <ref_datamodel_attributes>` declarations.


Concrete links can also be defined using the
:eql:stmt:`CREATE LINK <CREATE-LINK>` EdgeQL command.
