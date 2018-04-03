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

.. TODO: Insert a better illustration

Every node in the data graph has a specific *type*.  There are three
categories of types in EdgeDB: *object types*, *scalar types*, and
*collection types*.  Only object type nodes can have links to other nodes.
