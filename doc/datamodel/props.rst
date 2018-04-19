.. _ref_datamodel_props:

==========
Properties
==========

:ref:`Object types <ref_datamodel_object_types>` and
:ref:`links <ref_datamodel_links>` contain *properties*: a name-value
collection of primitive data associated with the given object or link
instance.

Every property is declared to have a specific
:ref:`scalar type <ref_datamodel_scalar_types>` or a
:ref:`collection type <ref_datamodel_collection_types>`.

There are two kinds of property item declarations: *abstract properties*,
and *concrete properties*.  Abstract properties are defined on module level
and are not tied to any particular object type or link.  Concrete properties
are defined on specific object types.  Concrete properties automatically
extend abstract properties with the same name in the same module.


Definition
==========

Abstract Properties
-------------------

An *abstract property* may be defined in EdgeDB Schema using the
``abstract property`` declaration:

.. code-block:: pseudo-eql

    abstract property <prop_name> [ extending [(] <parent_prop> [, ...] [)]]:
        [ <attribute_declarations> ]

Parameters:

    :eql:inline-synopsis:`<prop_name>`
        Specifies the name of the property item.  Customarily, property names
        are lowercase, with words separated by underscores as necessary for
        readability.

    :eql:inline-synopsis:`extending <parent_prop> [, ...]`
        If specified, declares the *parents* of the property item.

        Use of ``extending`` creates a persistent schema relationship
        between this property and its parents.  Schema modifications
        to the parent(s) propagate to the child.

    :eql:inline-synopsis:`<attribute_declarations>`
        :ref:`Schema attribute <ref_datamodel_attributes>` declarations.


Abstract links can also be defined using the
:eql:stmt:`CREATE ABSTRACT PROPERTY` EdgeQL command.


.. _ref_datamodel_props_concrete:

Concrete Properties
-------------------

A *concrete property* may be defined in EdgeDB Schema using the ``property``
declaration in the context of a ``type`` or ``abstract link`` declaration:

.. code-block:: pseudo-eql

    type <TypeName>:
        [required] [readonly] [inherited] property <prop_name>:
            [ expr := <computable_expr> ]
            [ default := <default_expr> ]
            [ <attribute_declarations> ]

    shorthand form for computable property declaration:

    type <TypeName>:
        [inherited] property <prop_name> := <computable_expr>

    link property declaration:

    abstract link <link_name>:
        [readonly] [inherited] property <prop_name>:
            [ expr := <computable_expr> ]
            [ default := <default_expr> ]
            [ <attribute_declarations> ]

    shorthand form for computable link property declaration:

    abstract link <link_name>:
        [inherited] property <prop_name> := <computable_expr>


Parameters:
    :eql:inline-synopsis:`required`
        If specified, the property is considered *required* for the
        parent object type.  It is an error for an object to have a required
        property resolve to an empty value.  Child properties **always**
        inherit the *required* attribute, i.e it is not possible to
        make a required property non-required by extending it.

        .. note::

            Link properties cannot be ``required``.

    :eql:inline-synopsis:`readonly`
        If specified, the property is considered *read-only*.  Modifications
        of this property are prohibited once an object or link is created.

    :eql:inline-synopsis:`<computable_expr>`
        If specified, designates this property as a *computable property*
        (see :ref:`Computables <ref_datamodel_computables>`).  A computable
        property cannot be *required* or *readonly* (the latter is implied and
        always true).  There is a shorthand form using the ``:=`` syntax,
        as shown in the synopsis above.

    :eql:inline-synopsis:`<attribute_declarations>`
        :ref:`Schema attribute <ref_datamodel_attributes>` declarations.


Concrete links can also be defined using the
:eql:stmt:`CREATE LINK <CREATE-LINK>` EdgeQL command.
