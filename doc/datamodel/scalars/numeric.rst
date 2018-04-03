.. _ref_datamodel_scalars_numeric:

Numeric Types
=============

.. eql:type:: std::numeric

    Any number of arbitrary precision.

    All of the following types can be cast into numeric:
    :eql:type:`int16`, :eql:type:`int32`, :eql:type:`int64`,
    :eql:type:`float32`, and :eql:type:`float64`.

.. eql:type:: std::int16

    A 16-bit signed integer.

.. eql:type:: std::int32

    A 32-bit signed integer.

.. eql:type:: std::int64

    A 64-bit signed integer.

.. eql:type:: std::float32

    A variable precision, inexact number.

    Minimal guaranteed precision is at least 6 decimal digits.

.. eql:type:: std::float64

    A variable precision, inexact number.

    Minimal guaranteed precision is at least 15 decimal digits.
