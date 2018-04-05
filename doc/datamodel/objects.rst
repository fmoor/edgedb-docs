.. _ref_datamodel_object_types:

Object Types
============

Object types are the primary component of EdgeDB schema.  An object type
is a collection of named *links* to other types.   An instance of an
object type is called an *object*.  All data in EdgeDB is represented by
objects and by links between objects.

Every object has a globally unique *identity* represented by a ``UUID``
value.  Object's identity is assigned on object's creation and never
changes.  Referring to object's ``id`` link yields its identity as a
:eql:type:`std::uuid` value.

Object types can *extend* other object types, in which case the extending
type is called a *subtype* and types being extended are called *supertypes*.
A subtype inherits all links and attributes of its supertypes.

:eql:type:`std::Object` is the root of object type hierarchy, all object
types in EdgeDB extend ``std::Object`` directly or indirectly.

.. eql:type:: std::Object

    Root object type.

    Definition:

    .. code-block:: eschema

        type Object:
            # Universally unique object identifier
            required readonly link id to std::uuid

            # Object type in the information schema.
            required readonly link __type__ to schema::ObjectType
