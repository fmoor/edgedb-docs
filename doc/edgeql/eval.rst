.. _ref_eql_eval:

Expression Evaluation
=====================

For simplicity, a reference to a *function* in this section means any
EdgeQL operator, clause or an actual function.

There are two main ways a function is applied to an argument:
*element-wise* or as a *whole set*.  The way is determined by the
function declaration: arguments declared with the ``SET OF`` keyword
are passed as a whole set, arguments declared without the ``SET OF`` keyword
are passed *element-wise*.

For example, basic arithmetic :ref:`operators <ref_eql_expr_elops>`
are declared as element-wise for their arguments, while aggregate functions,
such as :eql:func:`sum` or :eql:func:`count` take their input as a whole.

An expression is evaluated recursively using the following procedure:

.. _ref_eql_fundamentals_eval_algo:

1. :ref:`Canonicalize <ref_eql_fundamentals_path_canon>` all path
   expressions.

2. Make a cartesian product of all element-wise inputs.
   See :ref:`ref_eql_emptyset` on what happens when the
   product is empty.

3. Iterate over the input product tuple, and on every iteration:

    - replace set references in the expression and all subexpressions
      with the corresponding value from the input tuple;

    - compute the values of all ``SET OF`` arguments recursively;

    - apply the function and store the result.

4. Append the results of all iterations to obtain the final result.

Below is an example of element-wise multiplication:

.. code-block:: edgeql-repl

    db> WITH A := {1, 2}, B := {3, 4}
    ... SELECT A * B;
    {3, 4, 6, 8}


An example of whole-set function:

.. code-block:: edgeql-repl

    db> WITH A := {1, 2}
    ... SELECT count(A);
    {2}


An example of both:

.. code-block:: edgeql-repl

    db> WITH A := {1, 2}, B := {3, 4}
    ... SELECT (A, count(B));
    {
      (1, 2),
      (2, 2)
    }

Importantly, when the element-wise input is iterated over, *all* set
references are replaced with a corresponding element, so when the below
expression is evaluated, ``count(A)`` is essentially ``count({a})`` and
is always equal to ``1``:

.. code-block:: edgeql-repl

    db> WITH A := {1, 2}, B := {3, 4, 5}
    ... SELECT (A, count(A), count(B));
    {
      (1, 1, 3),
      (2, 1, 3)
    }


.. _ref_eql_emptyset:

Empty Set Handling
------------------

In the :ref:`evaluation algorithm <ref_eql_fundamentals_eval_algo>` above,
the second step is making a cartesian product of element-wise inputs.
Consequently, if any argument is an *empty set* the product will also be an
empty set.  In this situation there are two possible scenarios:

1. If *none* of the function arguments were declared as ``OPTIONAL``,
   the function is never called and the result is an empty set.  This is
   the most common case.

2. If *any* of the function arguments were declared as ``OPTIONAL``, the
   function is called once with element-wise arguments as empty sets,
   its result is returned.

For example, the following query returns an empty set:

.. code-block:: edgeql-repl

    db> SELECT {2} * {};
    {}

A most notable example of a function that *does* get called on empty input
is the :eql:op:`coalescing <COALESCE>` operator.
