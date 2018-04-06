.. _ref_datamodel_overview:

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

``str`` in the above example is a
:ref:`scalar type <ref_datamodel_scalar_types>`.  EdgeDB also supports
several :ref:`collection types <ref_datamodel_collection_types>`.

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
    links
    constraints
    views
    modules
    databases
    eschema/index
