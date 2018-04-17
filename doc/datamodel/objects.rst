.. _ref_datamodel_object_types:

============
Object Types
============

Object types are the primary components of EdgeDB schema.  An object type
is a collection of named :ref:`properties <ref_datamodel_props>` and
:ref:`links <ref_datamodel_links>` to other object types.   An instance of
an object type is called an *object*.  All data in EdgeDB is represented by
objects and by links between objects.

Every object has a globally unique *identity* represented by a ``UUID``
value.  Object's identity is assigned on object's creation and never
changes.  Referring to object's ``id`` property yields its identity as a
:eql:type:`std::uuid` value.

Object types can *extend* other object types, in which case the extending
type is called a *subtype* and types being extended are called *supertypes*.
A subtype inherits all links, properties and other attributes of its
supertypes.

``std::Object`` is the root of object type hierarchy, all object
types in EdgeDB extend ``std::Object`` directly or indirectly.

.. eql:type:: std::Object

    Root object type.

    Definition:

    .. code-block:: eschema

        type Object:
            # Universally unique object identifier
            required readonly property id -> std::uuid

            # Object type in the information schema.
            required readonly link __type__ -> schema::ObjectType


Definition
==========

Object types may be defined in EdgeDB Schema using the ``type`` keyword:

.. code-block:: pseudo-eql

    [abstract] type <TypeName> [extending [(] <supertype> [, ...] [)]]:
        [ <property_declarations> ]
        [ <link_declarations> ]
        [ <index_declarations> ]
        [ <attribute_declarations> ]
        ...

Parameters:

    :eql:inline-synopsis:`abstract`
        If specified, the declared type will be *abstract*.

    :eql:inline-synopsis:`<TypeName>`
        Specifies the name of the object type.  Customarily, object type names
        use the CapWords convention.

    :eql:inline-synopsis:`extending <supertype> [, ...]`
        If specified, declares the *supertypes* of the new type.

        Use of ``extending`` creates a persistent type relationship
        between the new subtype and its supertype(s).  Schema modifications
        to the supertype(s) propagate to the subtype.

        References to supertypes in queries will also include objects of
        the subtype.

        If the same *link* or *property* name exists in more than one
        supertype, or is explicitly defined in the subtype and at
        least one supertype then the data types of the link targets must
        be *compatible*.  If there is no conflict, the links are merged to
        form a single link in the new type.

    :eql:inline-synopsis:`<property_declarations>`
        :ref:`Property <ref_datamodel_props>` declarations.

    :eql:inline-synopsis:`<link_declarations>`
        :ref:`Link <ref_datamodel_links>` declarations.

    :eql:inline-synopsis:`<index_declarations>`
        :ref:`Index <ref_datamodel_indexes>` declarations.

    :eql:inline-synopsis:`<attribute_declarations>`
        :ref:`Schema attribute <ref_datamodel_attributes>` declarations.

A :eql:stmt:`CREATE TYPE` EdgeQL command may also be used to define a new
object type.
