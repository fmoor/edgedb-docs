.. _ref_edgedb_data_model:

EdgeDB Data Model
=================

Overview
--------

Data in EdgeDB is interpreted as a *directed labeled property graph*.
The nodes contain the data, while the edges represent relationships
between the data.

Although EdgeDB itself is not a classical graph database, the property
graph model is ideal for the implementation of entity-relationship
data models found in most applications.

For example, a *City* can relate to a *Country* through the "capital"
relationship, and *Country* relates to *City* through the "country"
relationship.

::

            +-------+{capital}+------+
            |                        |
     +------+------+           +-----v-----+
     |             |           |           |
     |   Country   |           |    City   |
     |             |           |           |
     +------^------+           +-----+-----+
            |                        |
            +-------+{country}+------+

.. TODO: Insert an illustration that better explains the data model.

Every node in the data graph holds a value and has a specific *type*.
There are two main categories of types in EdgeDB: *object types* and
*primitive types*.

The EdgeDB data graph follows the following rules:

1. Only object type nodes can have links to other nodes, primitive type
   nodes have no links.

2. The identity of an object node is determined by the value of its
   ``id`` link, whereas all primitive type nodes have distinct identities.

3. All nodes in the data graph have distinct identities.

4. There can be a maximum of one link instance of a given link type
   between two object nodes.
