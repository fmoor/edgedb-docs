.. _ref_datamodel_scalar_types:

Scalar Types
============

*Scalar types* are primitive individual types.  Scalar type instances
hold a single value, called a *scalar value*.

The standard EdgeDB scalar types are:

- :ref:`Numeric types <ref_datamodel_scalars_numeric`:
    * :eql:type:`int16`
    * :eql:type:`int32`
    * :eql:type:`int64`
    * :eql:type:`float32`
    * :eql:type:`float64`
    * :eql:type:`numeric`

- :ref:`Boolean type <ref_datamodel_scalars_boolean>`

- :ref:`Date/Time types <ref_datamodel_scalars_datetime>`

- :ref:`UUID type <ref_datamodel_scalars_uuid>`


.. toctree::
    :maxdepth: 3

    numeric
    str
    bool
    datetime
    bytes
    sequence
    uuid
    json
