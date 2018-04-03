.. _ref_edgeql_operators:


Operators
=========

Expressions allow to manipulate, query, and modify data in EdgeQL.
Operators are used to build expressions out of the basic component
parts: literals, :ref:`paths<ref_edgeql_fundamentals_paths>`,
:ref:`shapes<ref_edgeql_shapes>`, :ref:`functions<ref_edgeql_functions>`,
and even :ref:`statements<ref_edgeql_statements>`.

All expressions in EdgeQL evaluate to

:ref:`multisets<ref_edgeql_fundamentals_multisets>`, which this
documentation refers to simple as `sets` for reasons of brevity. All
sets in EdgeQL have to contain elements of the same :ref:`fundamental
type<ref_edgeql_types>`. Broadly all types can be broken down
into the following categories: `objects`, `atomic values`, `array`,
`maps`, or `tuples`.

It is convenient to treat all expressions as `sets`, in particular
``1`` is equivalent to ``{1}`` in EdgeQL. Also, there's no way to
produce nested sets in EdgeQL as an expression (although conceptually
:ref:`GROUP<ref_edgeql_statements_group>` statement operates on sets
of sets as one of its intermediate steps). Because of that nested
sets are automatically flattened:

    ``{1, 2, {3, 4}, 5}`` ≡ ``{1, 2, 3, 4, 5}``

.. note::

    Those familiar with *bunch theory* will recognize that effectively
    EdgeQL operates on bunches rather than multisets. We choose to use
    the notation typically associated with sets, such as ``{a, b,
    c}``, because of the need to disambiguate *tuples* from sets (or
    bunches) without using symbols that are difficult to type.

        ``a, b, c`` - is a bunch

        ``(a, b, c)`` - is an EdgeQL tuple (but could be confused with
        a bunch)

        ``{a, b, c}`` - is an EdgeQL multiset (which has properties very
        similar to a bunch)


Set and element arguments
-------------------------

In EdgeDB operators and functions can take sets or individual elements
as arguments. For the purpose of generalization all operators can be
viewed as :ref:`functions<ref_edgeql_fundamentals_function>`. Since
fundamentally EdgeDB operates on sets, that means that all functions
that are defined to take elements are generalized to operate on sets
by applying the function to each input set element separately.
Incidentally, since ultimately EdgeDB operates on sets it is
conceptually convenient to treat all functions as returning sets as
their result.

.. note::

    Given an *n-ary* function *f* and A\ :sub:`1`, ..., A\ :sub:`n`
    ⊆ U, define the result set of applying the function as:

        :emphasis:`f`\ (A\ :sub:`1`, ..., A\ :sub:`n`) ≡
        { :emphasis:`f`\ (t): ∀ t ∈ A\ :sub:`1` ⨉ ... ⨉ A\ :sub:`n` }

Functions that operate on sets only, don't require additional
mechanisms to be applied to EdgeDB sets.

In the general case a function can have some arguments as elements and others
as sets. The generalized formula is the given by the following:

.. note::

    Given a function *F* with *n* element-parameters and *m* set-
    parameters as well as A\ :sub:`1`, ..., A\ :sub:`n`, B\ :sub:`1`,
    ..., B\ :sub:`m` ⊆ U, the result set of applying the function is
    as follows:

        :emphasis:`F`\ (A\ :sub:`1`, ..., A\ :sub:`n`, B\ :sub:`1`, ...,
        B\ :sub:`m`) ≡

            { :emphasis:`F`\ (a\ :sub:`1`, ..., a\ :sub:`n`, B\ :sub:`1`,
            ..., B\ :sub:`m`): ∀ a\ :sub:`1`, ..., a\ :sub:`n` ∈ A\
            :sub:`1` ⨉ ... ⨉ A\ :sub:`n` }

One of the basic operators in EdgeQL (:eql:op:`IN`) is an example of such a
mixed function and will be covered in more details below. Many
operators and most library functions have all their parameters as
either all sets or all elements.

The above definitions assume that all the input sets are different
from each other. What happens when some of the input sets are
semantically the same? In that case there's a particular interaction
between element-parameters and set-parameters.

For simplicity we can consider the case when some 2 input sets are the
same. Let's call them both `X`. This results in 3 possible general
cases:

- The same sets are both used as element-parameters

    :emphasis:`F`\ (X, X, A\ :sub:`3`, ..., A\ :sub:`n`, B\ :sub:`1`, ...,
    B\ :sub:`m`) ≡

            { :emphasis:`F`\ (x, x, a\ :sub:`3`, ..., a\ :sub:`n`, B\ :sub:`1`,
            ..., B\ :sub:`m`): ∀ x, a\ :sub:`3`, ..., a\ :sub:`n` ∈ X ⨉ A\
            :sub:`3` ⨉ ... ⨉ A\ :sub:`n` }

- The same sets are both used as set-parameters

    :emphasis:`F`\ (A\ :sub:`1`, ..., A\ :sub:`n`, X, X, B\ :sub:`3`, ...,
    B\ :sub:`m`) ≡

            { :emphasis:`F`\ (a\ :sub:`1`, ..., a\ :sub:`n`, X, X, B\ :sub:`3`,
            ..., B\ :sub:`m`): ∀ a\ :sub:`1`, ..., a\ :sub:`n` ∈ A\
            :sub:`1` ⨉ ... ⨉ A\ :sub:`n` }

- One of the sets is element-parameter and the other is set-parameter

    :emphasis:`F`\ (X, A\ :sub:`2`, ..., A\ :sub:`n`, X, B\ :sub:`2`, ...,
    B\ :sub:`m`) ≡

            { :emphasis:`F`\ (x, a\ :sub:`2`, ..., a\ :sub:`n`, {x},
            B\ :sub:`2`, ..., B\ :sub:`m`):
            ∀ x, a\ :sub:`2`, ..., a\ :sub:`n` ∈
            X ⨉ A\ :sub:`2` ⨉ ... ⨉ A\ :sub:`n` }

The first two cases are fairly straightforward and intuitive. The
third case is special and defines how EdgeDB processes queries. That
is the basic rule from which
:ref:`longest common prefix<ref_edgeql_scope_prefix>` property follows.

In EdgeQL there are 3 kinds of :ref:`parameter types
<ref_edgeql_fundamentals_function>`:

- Element-wise (default)
- :eql:type:`OPTIONAL`
- :eql:type:`SET-OF`

The first 2 act as element-parameters when interacting with any other
types. :eql:type:`SET-OF` acts as a set-parameter when interacting with
any other types.

EdgeQL uses :eql:type:`SET-OF` qualifier in function declarations
to disambiguate between the element-parameters and set-parameters.
EdgeQL operator signatures can be described in a similar way to make
it clear how they are applied.

In order to reduce all expression components into either paths
(symbols) or function calls it is necessary to conceptualize what is
the signature of the operator that wraps a statement and makes it an
expression (syntactically it's ``(<statement>)``):

.. code-block:: eschema

    function stmt_to_expr(set of any) -> set of any:
        from edgeql :>
            ...

Basically, statements-as-expressions are treated similar to aggregates
in terms of how they interact with what's outside of them. A parallel
can be drawn between that and :eql:func:`array_agg`, but instead of
producing an array, the result is still a *set*.


Operations and paths
--------------------

There is some important interaction of the rule of
:ref:`longest common prefix<ref_edgeql_scope_prefix>`
for paths and operation cardinality. Consider the following example:

.. code-block:: eql

    SELECT Issue.status.name + Issue.number;

The expression ``Issue.status.name`` is a set of all strings, that are
reachable from any ``Issue`` by following the link ``status`` and then
``name``.  Because the link ``status`` has the default cardinality of
``*1`` and so does the link ``name`` overall the expression has the
same cardinality as the set of ``Issues``.  Similarly, as a separate
expression ``Issue.number`` would have the same cardinality as
``Issues``.  However, due to the common prefix rule that states that a
common prefix denotes *the same* object the operation :eql:op:`+<PLUS>`
is not applied to the cross-product of the set ``Issue.status.name``
and ``Issue.number`` as if they were independent.  Instead for every
common prefix (``Issue`` in this case), the operation is applied to
the cross-product of the subsets denoted by the remainder of the
operand paths.  For the sample query, these subsets happen to be
singleton sets for every ``Issue``, because all the links followed
from ``Issue`` have the default cardinality ``*1``, pointing to
singleton sets.  Thus the result of the operation for each ``Issue``
is also a singleton set and the overall cardinality of the expression
``Issue.status.name + Issue.number`` is the same as the cardinality of
``Issues``.


.. _ref_edgeql_expressions_setops:

Operations signatures
---------------------

Statements and clauses are effectively set operations and are
discussed in more details in the
:ref:`Statements<ref_edgeql_statements>` section. One of the
building blocks used in these examples is a set literal, e.g. ``{1, 2,
3}``. In the simplest form this expression denotes a set of elements.
Like any other EdgeDB sets the elements all have to be of the same
type (all sets are homogeneous).

Basic set operators:

.. eql:operator:: DISTINCT: DISTINCT A

    :optype A: SET OF any
    :resulttype: any

    Return a set without repeating any elements.

    :eql:op:`DISTINCT` is a set operator that returns a new set where
    no member is equal to any other member. Considering that any two
    objects are equal if and only if they have the same identity (that
    is to say, the value of an object is equal to its identity), this
    operator is mainly useful when applied to sets of atomic values
    (or any other non-object, such as an array or tuple).


.. eql:operator:: UNION: A UNION B

    :optype A: SET OF any
    :optype B: SET OF any
    :resulttype: SET OF any

    Merge two multisets.

    Formally :eql:op:`UNION` is a *multiset sum*, so effectively it
    merges two multisets keeping all of their members.

    For example, applying :eql:op:`UNION` to ``{1, 2, 2}`` and
    ``{2}``, results in the multiset ``{1, 2, 2, 2}``.


.. eql:operator:: SETLITERAL: {A0, ... }

    :optype A0: SET OF any
    :resulttype: SET OF any

    Merge all elements into a single multiset.

    The set literal has more advanced features in EdgeDB. If any other
    sets are nested in it, the set literal will *flatten* them out.
    Effectively a set literal is equivalent to applying :eql:op:`UNION`
    to all its elements:

    ``{1, 2, {3, 4}, 5}`` ≡ ``{1, 2, 3, 4, 5}``

    For any two sets ``A``, ``B`` of the same type:
    ``{A, B}`` = ``A UNION B``


.. eql:operator:: STMTWRAP: ( statement )

    :optype statement: SET OF any
    :resulttype: SET OF any

    Treat a statement as an expression.

    Wrapping a statement into parentheses to make into expression
    treats the entire argument set as a :eql:type:`SET-OF`.

    ``(SELECT User)`` is the same as ``{User}``.


.. eql:operator:: EXISTS: EXISTS A

    :optype A: SET OF any
    :resulttype: bool

    Test whether a set is not empty.

    :eql:op:`EXISTS` is a set operator that returns a singleton set
    ``{TRUE}`` if the input set is not ``{}`` and returns ``{FALSE}``
    otherwise.

    .. note::

        Technically, :eql:op:`EXISTS` behaves like a special built-in
        :ref:`aggregate function<ref_edgeql_functions_agg>`. It is
        sufficiently basic and a special case that it is an *operator*
        unlike a built-in aggregate function :eql:func:`count`.


.. eql:operator:: IF..ELSE: A IF C ELSE B

    :optype A: SET OF any
    :optype C: bool
    :optype B: SET OF any
    :resulttype: SET OF any

    Conditionally provide one or the other result.

    It's worth noting that :eql:op:`IF..ELSE` is a kind of syntax
    sugar for the following expression:

    .. code-block:: eql

        # SELECT a IF cond ELSE b is equivalent to the below:
        SELECT
            (SELECT a FILTER cond)
            UNION
            (SELECT b FILTER NOT cond);

    One of the consequences of this is that if the ``cond`` expression
    is ``{}``, the whole choice expression evaluates to ``{}``.


.. eql:operator:: COALESCE: A ?? B

    :optype A: OPTIONAL any
    :optype B: SET OF any
    :resulttype: SET OF any

    Evaluate to ``A`` for non-empty ``A``, otherwise evaluate to ``B``.

    A typical use case of coalescing operator is to provide default
    values for optional links.

    .. code-block:: eql

        # Get a set of tuples (<issue name>, <priority>)
        # for all issues.
        WITH
            MODULE example
        SELECT
            (Issue.name, Issue.priority.name ?? 'n/a');

    Without the coalescing operator the above query would skip any
    ``Issue`` without priority.


.. eql:operator:: IN: A IN B or A NOT IN B

    :optype A: any
    :optype B: SET OF any
    :resulttype: bool

    Test the membership of an element in a set.

    Set membership operators :eql:op:`IN` and :eql:op:`NOT IN<IN>`
    that test for each element of ``A`` whether the it is present in ``B``.

    .. code-block:: eql

        SELECT 1 IN {1, 3, 5};
        # returns [True]

        SELECT 'Alice' IN User.name;

        SELECT {1, 2} IN {1, 3, 5};
        # returns [True, False]


.. _ref_edgeql_expressions_elops:

Element operations
------------------

Element operators are those that treat all of their operands as
element-wise. Most of these operators require their operands to be of
the same :ref:`type<ref_edgeql_types>`.

Logical
~~~~~~~

.. eql:operator:: OR: A OR B

    :optype A: bool
    :optype B: bool
    :resulttype: bool

    Logical disjunction.


.. eql:operator:: AND: A AND B

    :optype A: bool
    :optype B: bool
    :resulttype: bool

    Logical conjunction.


.. eql:operator:: NOT: NOT A

    :optype A: bool
    :resulttype: bool

    Logical negation.

Comparison
~~~~~~~~~~

.. eql:operator:: EQ: A = B

    :optype A: any
    :optype B: any
    :resulttype: bool

    Compare two values for equality.


.. eql:operator:: NEQ: A != B

    :optype A: any
    :optype B: any
    :resulttype: bool

    Compare two values for inequality.


.. eql:operator:: COALEQ: A ?= B

    :optype A: OPTIONAL any
    :optype B: OPTIONAL any
    :resulttype: bool

    Compare two values for equality.

    Works the same as regular :eql:op:`=<EQ>`, but also allows
    comparing ``{}``.  Two ``{}`` are considered equal.


.. eql:operator:: COALNEQ: A ?!= B

    :optype A: OPTIONAL any
    :optype B: OPTIONAL any
    :resulttype: bool

    Compare two values for inequality.

    Works the same as regular :eql:op:`\!=<NEQ>`, but also allows
    comparing ``{}``.  Two ``{}`` are considered equal.


.. eql:operator:: LT: A < B

    :optype A: any
    :optype B: any
    :resulttype: bool

    ``TRUE`` if ``A`` is less than ``B``.


.. eql:operator:: GT: A > B

    :optype A: any
    :optype B: any
    :resulttype: bool

    ``TRUE`` if ``A`` is greater than ``B``.


.. eql:operator:: LTEQ: A <= B

    :optype A: any
    :optype B: any
    :resulttype: bool

    ``TRUE`` if ``A`` is less than or equal to ``B``.


.. eql:operator:: GTEQ: A >= B

    :optype A: any
    :optype B: any
    :resulttype: bool

    ``TRUE`` if ``A`` is greater than or equal to ``B``.


Arithmetic
~~~~~~~~~~

.. eql:operator:: PLUS: A + B

    :optype A: numeric or str or bytes
    :optype B: numeric or str or bytes
    :resulttype: numeric or str or bytes

    Arithmetic addition or string concatenation.

    Arithmetic addition if operands are :eql:type:`numbers<numeric>`.

    Concatenation if operands are :eql:type:`str` or :eql:type:`bytes`.


.. eql:operator:: MINUS: A - B

    :optype A: numeric
    :optype B: numeric
    :resulttype: numeric

    Arithmetic subtraction.


.. eql:operator:: UMINUS: -A

    :optype A: numeric
    :resulttype: numeric

    Arithmetic negation.


.. eql:operator:: MULT: A * B

    :optype A: numeric
    :optype B: numeric
    :resulttype: numeric

    Arithmetic multiplication.


.. eql:operator:: DIV: A / B

    :optype A: numeric
    :optype B: numeric
    :resulttype: numeric

    Arithmetic division.


.. eql:operator:: MOD: A % B

    :optype A: numeric
    :optype B: numeric
    :resulttype: numeric

    Remainder from division (modulo).


.. eql:operator:: POW: A ^ B

    :optype A: numeric
    :optype B: numeric
    :resulttype: numeric

    Power operation.


String
~~~~~~

.. eql:operator:: LIKE: A LIKE B

    :optype A: str or bytes
    :optype B: str or bytes
    :resulttype: bool

    Case-sensitive simple string matching.

    :eql:op:`LIKE` works exactly the same way as in SQL.


.. eql:operator:: ILIKE: A ILIKE B

    :optype A: str or bytes
    :optype B: str or bytes
    :resulttype: bool

    Case-insensitive simple string matching.

    :eql:op:`ILIKE` works exactly the same way as in SQL.


Type-checking
~~~~~~~~~~~~~

.. eql:operator:: IS: A IS B or A IS NOT B

    :optype A: any
    :optype B: type
    :resulttype: bool

    Type-checking of ``A`` w.r.t. type ``B``.

    Type-checking operators :eql:op:`IS` and :eql:op:`IS NOT<IS>` that
    test whether the left operand is of any of the types given by the
    comma-separated list of types provided as the right operand.

    Note that ``B`` is special and is not any kind of expression, so
    it does not in any way participate in the interactions of sets and
    longest common prefix rules.

    .. code-block:: eql

        SELECT 1 IS int;
        # returns [True]

        SELECT User IS NOT SystemUser
        FILTER User.name = 'Alice';
        # returns [True]

        SELECT User IS (Text, Named);
        # returns [True, ..., True], one for every user


.. _ref_edgeql_types_casts:

Type-casts
----------

Sometimes it is necessary to convert data from one type to another.
This is called *casting*. In order to *cast* one expression into a
different type the expression is prefixed with the ``<new_type>``,
as follows:

.. code-block:: eql

    # cast a string literal into an integer
    SELECT <int>"42";

    # cast an array of integers into an array of str
    SELECT <array<str>>[1, 2 , 3];

    # cast an issue number into a string
    SELECT <str>example::Issue.number;

Casts also work for converting tuples or declaring different tuple
element names for convenience.

.. code-block:: eql

    SELECT <tuple<int, str>>(1, 3);
    # returns [[1, '3']]

    WITH
        # a test tuple set, that could be a result of
        # some other computation
        stuff := (1, 'foo', 42)
    SELECT (
        # cast the tuple into something more convenient
        <tuple<a: int, name: str, b: int>>stuff
    ).name;  # access the 'name' element

An important use of *casting* is in defining the type of an empty
set ``{}``, which can be required for purposes of type disambiguation.

.. code-block:: eql

    WITH MODULE example
    SELECT Text {
        name :=
            Text[IS Issue].name IF Text IS Issue ELSE
            <str>{},
            # the cast to str is necessary here, because
            # the type of the computable must be defined
        body,
    };


Operator Precedence
-------------------

EdgeQL operators listed in order of precedence from lowest to highest:

.. list-table::
    :widths: auto
    :header-rows: 1

    * - operator
    * - :eql:op:`UNION`
    * - :eql:op:`IF..ELSE`
    * - :eql:op:`OR`
    * - :eql:op:`AND`
    * - :eql:op:`NOT`
    * - :eql:op:`=<EQ>`, :eql:op:`\!=<NEQ>`, :eql:op:`?=<COALEQ>`,
        :eql:op:`?\!=<COALNEQ>`
    * - :eql:op:`\<<LT>`, :eql:op:`><GT>`, :eql:op:`\<=<LTEQ>`,
        :eql:op:`>=<GTEQ>`
    * - :eql:op:`LIKE`, :eql:op:`ILIKE`
    * - :eql:op:`IN`, :eql:op:`NOT IN<IN>`
    * - :eql:op:`IS`, :eql:op:`IS NOT<IS>`
    * - :eql:op:`+<PLUS>`, :eql:op:`-<MINUS>`
    * - :eql:op:`/<DIV>`, :eql:op:`*<MULT>`, :eql:op:`%<MOD>`
    * - :eql:op:`??<COALESCE>`
    * - :eql:op:`DISTINCT`, unary :eql:op:`-<UMINUS>`
    * - :eql:op:`^<POW>`
    * - Type-casts_
