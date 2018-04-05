Data Model
==========

EdgeDB is an object-relational database with strongly typed schema.

An EdgeDB schema is primarily composed from *object type* definitions, which
describe entities in a specific domain.  An *object type* is a collection
of named references to other types (*links*).

Here is an example of a simple EdgeDB type using the eschema notation:

.. code-block:: eschema

    type User:
        link name to str
        link address to str
        link friends to User

There are two main categories of types in EdgeDB: *object types* and
*primitive types*.  Primitive types are further subdivided into
*scalar types* and *collection types*.

* :ref:`ref_datamodel_object_types`

    A collection of links to other types.  Object type instances, or
    ``objects`` are globally unique.

* :ref:`ref_datamodel_scalar_types`

    Individual basic types such as :eql:type:`int32` and :eql:type:`str`.

* :ref:`ref_datamodel_collection_types`

    There are 3 kinds of collection types built into EdgeDB:
    :eql:type:`array`, :eql:type:`map`, and :eql:type:`tuple`.

EdgeDB schemas consist of :ref:`modules <ref_datamodel_modules>` and can
also contain the following declarations:

* :ref:`ref_datamodel_links`
* :ref:`ref_datamodel_linkprops`
* :ref:`ref_datamodel_constraints`
* :ref:`ref_datamodel_attributes`
* :ref:`ref_datamodel_functions`

.. toctree::
    :maxdepth: 3
    :hidden:

    objects
    scalars/index
    colltypes
    functions
    constraints
    views
    modules
    databases
