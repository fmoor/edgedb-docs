.. _ref_datamodel_constraints:

===========
Constraints
===========

*Constraints* are an EdgeDB mechanism that provides fine-grained control
over which data is considered valid.  A constraint may be defined on a
:ref:`scalar type <ref_datamodel_scalar_types>`, a
:ref:`concrete link <ref_datamodel_links_concrete>`, or a
:ref:`concrete property <ref_datamodel_props_concrete>`.


Definition
==========


Abstract Constraints
--------------------

An *abstract constraint* may be defined in EdgeDB Schema using the
``abstract constraint`` declaration:

.. code-block:: pseudo-eql

    abstract constraint <constr_name> [( [<argspec>] [, ...] )]
            [on (<subject_expr>)]
            [extending [(] <parent_constr>, [, ...] [)] ]:
        [ expr := <constr_expression> ]
        [ errmessage := <error_message> ]
        [ <attribute_declarations> ]

    where <argspec> is:

    [ $<argname>: ] <argtype>


Parameters
~~~~~~~~~~

:eql:inline-synopsis:`<constr_name>`
    The name of the constraint.

:eql:inline-synopsis:`<argspec>`
    An optional list of constraint arguments.  *argname* optionally specifies
    the argument name, and *argtype* specifies the argument type.

:eql:inline-synopsis:`<subject_expr>`
    An optional expression defining the *subject* of the constraint.
    If not specified, the subject is the value of the schema item on
    which the constraint is defined.

:eql:inline-synopsis:`extending <parent_constr> [, ...]`
    If specified, declares the *parent* constraints for this constraint.

:eql:inline-synopsis:`expr := <constr_expression>`
    An boolean expression that returns ``true`` for valid data and
    ``false`` for invalid data.  The expression may refer to special
    variables: ``__self__`` for the value of the scalar type, link or
    property value; and ``__subject__`` which is the constraint's subject
    expression as defined by *subject_expr*.

:eql:inline-synopsis:`errmessage := <error_message>`
    An optional string literal defining the error message template that
    is raised when the constraint is violated.  The template is a formatted
    string that may refer to constraint context variables in curly braces.
    The template may refer to the following:

    - ``$argname`` -- the value of the specified constraint argument
    - ``__self__`` -- the value of the ``title`` attribute of the scalar type,
      property or link on which the constraint is defined.

:eql:inline-synopsis:`<attribute_declarations>`
    :ref:`Schema attribute <ref_datamodel_attributes>` declarations.


Concrete Constraints
--------------------

A *concrete constraint* may be defined in EdgeDB Schema using the
``constraint`` declaration in the context of a ``scalar type``, ``property``,
or ``link`` declaration:

.. code-block:: pseudo-eql

    scalar type <typename>:
        constraint <constr_name> [( [$<argname> := ] <argvalue> [, ...] )]
                [on (<subject_expr>)]:
            [ <attribute_declarations> ]


Parameters
~~~~~~~~~~

:eql:inline-synopsis:`<constr_name>`
    The name of the previously defined abstract constraint.

:eql:inline-synopsis:`<argname>`
    The name of an argument.

:eql:inline-synopsis:`<argvalue>`
    The value of an argument as a literal constant of the correct type.

:eql:inline-synopsis:`<subject_expr>`
    An optional expression defining the *subject* of the constraint.
    If not specified, the subject is the value of the schema item on
    which the constraint is defined.

:eql:inline-synopsis:`<attribute_declarations>`
    :ref:`Schema attribute <ref_datamodel_attributes>` declarations.


Standard Constraints
====================

The standard library defines the following constraints:

- ``std::enum(array<any>)`` -- specifies the list of allowed values
  directly:

  .. code-block:: eschema

     scalar type status_t extending str:
         constraint enum (['Open', 'Closed', 'Merged'])

- ``std::max(any)`` -- specifies the maximum value for the subject:

  .. code-block:: eschema

     scalar type max_100 extending int:
        contraint max(100)

- ``std::maxexclusive(any)`` -- specifies the maximum value
  (as an open interval) for the subject:

  .. code-block:: eschema

     scalar type max_100 extending int:
        contraint max(100)

- ``std::expression`` -- uses the constraint subject directly as a constraint
  expression, the subject expression needs to be specified:

  .. code-block:: eschema

     scalar type starts_with_a extending str:
         constraint expression on (__subject__[0] = 'A')



Examples
========
