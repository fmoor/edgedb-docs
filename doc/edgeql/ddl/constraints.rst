.. _ref_eql_ddl_constraints:

===========
Constraints
===========

This section describes the DDL commands pertaining to
:ref:`constraints <ref_datamodel_constraints>`.


CREATE ABSTRACT CONSTRAINT
==========================

:eql-statement:
:eql-haswith:

Define a new :ref:`abstract constraint <ref_datamodel_constraints>`.

.. eql:synopsis::

    [ WITH [ <module-alias> := ] MODULE <module-name> ]
    CREATE ABSTRACT CONSTRAINT <name> [ ( [<argspec>] [, ...] ) ]
        [ ON ( <subject-expr> ) ]
        [ EXTENDING <base> [, ...] ]
    "{"
        [ SET expr := <constr-expression> ; ]
        [ SET errmessage := <error-message> ; ]
        [ SET <attr-name> := <attr-value> ; ]
        [ ... ]
    "}" ;

    # where <argspec> is:

    [ $<argname>: ] <argtype>


Description
-----------

``CREATE ABSTRACT CONSTRAINT`` defines a new abstract constraint.

If *name* is qualified with a module name, then the constraint is
created in that module, otherwise it is created in the current module.
The constraint name must be distinct from that of any existing schema item
in the module.


Parameters
----------

:eql:synopsis:`[ <module-alias> := ] MODULE <module-name>`
    An optional list of module alias declarations to be used in the
    migration definition.  When *module-alias* is not specified,
    *module-name* becomes the effective current module and is used
    to resolve all unqualified names.

:eql:synopsis:`<name>`
    The name (optionally module-qualified) of the new constraint.

:eql:synopsis:`<argspec>`
    An optional list of constraint arguments.
    :eql:synopsis:`<argname>` optionally specifies
    the argument name, and :eql:synopsis:`<argtype>`
    specifies the argument type.

:eql:synopsis:`<subject-expr>`
    An optional expression defining the *subject* of the constraint.
    If not specified, the subject is the value of the schema item on
    which the concrete constraint is defined.  The expression must refer
    to the original subject of the constraint as ``__subject__``.

:eql:synopsis:`EXTENDING <base> [, ...]`
    If specified, declares the *parent* constraints for this constraint.

:eql:synopsis:`SET expr := <constr_expression>`
    A boolean expression that returns ``true`` for valid data and
    ``false`` for invalid data.  The expression may refer to the subject
    of the constraint as ``__subject__``.

:eql:synopsis:`SET errmessage := <error_message>`
    An optional string literal defining the error message template that
    is raised when the constraint is violated.  The template is a formatted
    string that may refer to constraint context variables in curly braces.
    The template may refer to the following:

    - ``$argname`` -- the value of the specified constraint argument
    - ``__subject__`` -- the value of the ``title`` attribute of the scalar
      type, property or link on which the constraint is defined.

:eql:synopsis:`SET <attr-name> := <attr-value>;`
    An optional list of schema attribute values for the constraint.
    See :eql:stmt:`SET <SET ATTRIBUTE>` for details.


Examples
--------

Create an abstract constraint "uppercase" which checks if the subject
is a string in upper case.

.. code-block:: edgeql

    CREATE ABSTRACT CONSTRAINT uppercase {
        SET expr := upper(__subject__) = __subject__;
        SET title := "Upper case constraint";
        SET errmessage := "{__subject__} is not in upper case";
    };


ALTER ABSTRACT CONSTRAINT
=========================

:eql-statement:
:eql-haswith:

Alter the definition of an
:ref:`abstract constraint <ref_datamodel_constraints>`.

.. eql:synopsis::

    [ WITH [ <module-alias> := ] MODULE <module-name> ]
    ALTER ABSTRACT CONSTRAINT <name>
    "{"
        [ RENAME TO <new-name> ; ]
        [ SET expr := <constr-expression> ; ]
        [ SET errmessage := <error-message> ; ]
        [ SET <attr-name> := <attr-value> ; ]
        [ ... ]
    "}" ;


Description
-----------

``ALTER ABSTRACT CONSTRAINT`` changes the definition of an abstract constraint
item.  *name* must ve a name of an existing abstract constraint, optionally
qualified with a module name.


Parameters
----------

:eql:synopsis:`[ <module-alias> := ] MODULE <module-name>`
    An optional list of module alias declarations to be used in the
    migration definition.  When *module-alias* is not specified,
    *module-name* becomes the effective current module and is used
    to resolve all unqualified names.

:eql:synopsis:`<name>`
    The name (optionally module-qualified) of the constraint to alter.

:eql:synopsis:`RENAME TO <new-name>`
    Change the name of the constraint to *new-name*.  All concrete
    constraints inheriting from this constraint are also renamed.

:eql:synopsis:`SET expr := <constr_expression>`
    Changes the constraint expression.  See the relevant paragraph in
    :eql:stmt:`CREATE ABSTRACT CONSTRAINT` for details on constraint
    expressions.

:eql:synopsis:`SET errmessage := <error_message>`
    Changes the constraint error message.


DROP ABSTRACT CONSTRAINT
========================

:eql-statement:
:eql-haswith:


Remove an :ref:`abstract constraint <ref_datamodel_constraints>`
from the schema.

.. eql:synopsis::

    [ WITH [ <module-alias> := ] MODULE <module-name> ]
    DROP ABSTRACT CONSTRAINT <name> ;


Description
-----------

``DROP ABSTRACT CONSTRAINT`` removes an existing abstract constraint
item from the database schema.  If any schema items depending on this
constraint exist, the operation is refused.


Parameters
----------

:eql:synopsis:`[ <module-alias> := ] MODULE <module-name>`
    An optional list of module alias declarations to be used in the
    migration definition.  When *module-alias* is not specified,
    *module-name* becomes the effective current module and is used
    to resolve all unqualified names.

:eql:synopsis:`<name>`
    The name (optionally module-qualified) of the constraint to remove.


Examples
--------

Drop abstract constraint ``uppercase``:

.. code-block:: edgeql

    DROP ABSTRACT CONSTRAINT uppercase;


CREATE CONSTRAINT
=================

:eql-statement:

Define a concrete constraint on the specified schema item.

.. eql:synopsis::

    [ WITH [ <module-alias> := ] MODULE <module-name> ]
    CREATE [ DELEGATED ] CONSTRAINT <name>
        [ ( [<argspec>] [, ...] ) ]
        [ ON ( <subject-expr> ) ]
    "{"
        [ SET errmessage := <error-message> ; ]
        [ SET <attr-name> := <attr-value> ; ]
        [ ... ]
    "}" ;

    # where <argspec> is:

    [ $<argname> := ] <argvalue>


Description
-----------

``CREATE CONSTRAINT`` defines a new concrete constraint.  It can only be
used in the context of :eql:stmt:`CREATE SCALAR TYPE`,
:eql:stmt:`ALTER SCALAR TYPE`, :eql:stmt:`CREATE PROPERTY`,
:eql:stmt:`ALTER PROPERTY`, :eql:stmt:`CREATE LINK`, or
:eql:Stmt:`ALTER LINK`.

*name* must be a name (optionally module-qualified) of previously defined
abstract constraint.


Parameters
----------

:eql:synopsis:`[ <module-alias> := ] MODULE <module-name>`
    An optional list of module alias declarations to be used in the
    migration definition.  When *module-alias* is not specified,
    *module-name* becomes the effective current module and is used
    to resolve all unqualified names.

:eql:synopsis:`DELEGATED`
    If specified, the created constraint is a delegated constraint.

:eql:synopsis:`<name>`
    The name (optionally module-qualified) of the abstract constraint
    from which this constraint is derived.

:eql:synopsis:`<argspec>`
    An optional list of constraint arguments.  :eql:synopsis:`<argname>`
    optionally specifies the argument name, and :eql:synopsis:`<argvalue>`
    specifies the argument value.  The argument value specification must
    match the parameter declaration of the abstract constraint.

:eql:synopsis:`<subject-expr>`
    An optional expression defining the *subject* of the constraint.
    If not specified, the subject is the value of the schema item on
    which the concrete constraint is defined.  The expression must refer
    to the original subject of the constraint as ``__subject__``.

:eql:synopsis:`SET errmessage := <error_message>`
    An optional string literal defining the error message template that
    is raised when the constraint is violated.  See the relevant
    paragraph in :eql:stmt:`CREATE ABSTRACT CONSTRAINT` for the rules
    of error message template syntax.

:eql:synopsis:`SET <attr-name> := <attr-value>;`
    An optional list of schema attribute values for the constraint.
    See :eql:stmt:`SET <SET ATTRIBUTE>` for details.


Examples
--------

Create a maximum length constraint on the property "name" of the "User" type:

.. code-block:: edgeql

    ALTER TYPE User ALTER PROPERTY name
    CREATE CONSTRAINT std::maxlength(100);


ALTER CONSTRAINT
================

:eql-statement:

Alter the definition of a concrete constraint on the specified schema item.





DROP CONSTRAINT
===============

:eql-statement:

Remove a concrete constraint from the specified schema item.
