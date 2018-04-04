.. _ref_edgeql_fundamentals:


Fundamentals
============

EdgeQL is the primary language used to interact with EdgeDB, and
can be used to define, mutate and query data.  EdgeQL input consists
of a sequence of *commands*, and the database returns a specific response
to each command in sequence.

For example, the following EdgeQL ``SELECT`` command would return a
set of all `User` objects with the value of the ``name`` link equal to
``"Jonh"``.

.. code-block:: eql

    SELECT User FILTER User.name = 'John';


.. _ref_edgeql_fundamentals_type_system:

Type system
-----------

EdgeQL is a strongly typed language.  Every value in EdgeQL has a type,
which is determined statically from the database schema and the expression
that defines that value.


.. _ref_edgeql_fundamentals_set:

Everything is a set
-------------------

Every value in EdgeQL is viewed as a set of elements.
A set may be empty (*empty set*), contain a single element (a *singleton*),
or contain multiple elements.

.. note::
    :class: aside

    Strictly speaking, EdgeQL sets are *multisets*, as they do not require
    the elements to be unique.

A set cannot contain elements of different base types.  Mixing objects and
primitive types, as well as primitive types with different base type, is
not allowed.

Traditional relational databases deal with tables and use ``NULL`` as
a value denoting absence of data.  EdgeDB works with *sets*, so the absence of
data is just an empty set.


.. _ref_edgeql_fundamentals_references:

Set references and paths
------------------------

A *set reference* is a *name* (a simple identifier or a qualified schema name)
that represents a set of values.  It can be the name of an object type, the
name of a view, or an *expression alias* defined in a statement.

For example a reference to the ``User`` object type in the following
query will result in a set of all ``User`` objects:

.. code-block:: eql

    SELECT User;

Note, that unlike SQL no explicit ``FROM`` clause is needed.

A *path expression* (or simply a *path*) represents a set of values that
are reachable from a given set of nodes via a specific path in the data graph.
For example, the following will result in a set of all names of ``Users`` who
are friends with some other user:

.. code-block:: eql

    SELECT User.friends.name;

See :ref:`ref_edgeql_expressions_paths` for more information.


.. _ref_edgeql_fundamentals_functional:

EdgeQL is functional
--------------------

EdgeQL is a functional language in the sense that every
expression can be represented as a composition of functions.

Consider a query:

.. code-block:: eql

    SELECT User
    FILTER User.age > 20
    ORDER BY User.name

EdgeDB will evaluate this query as the following hypothetical functional
expression:

::

    order(
        filter(
            select_all(type = 'User'),
            predicate = function(u) => greater(u.age, 20)
        ),
        key = function(u) => u.name
    )

Notably, every EdgeQL statement can be interpreted as a pipeline: subsequent
clauses use the result of the preceding clause as input.
See :ref:`ref_edgeql_statements` for more information on how statements
and clauses are interpreted.

For simplicity, a reference to a *function* in this section means any
EdgeQL operator, clause or an actual function.

There are two main ways a function consumes an argument:
element-wise or as a whole.  The way is determined by how the parameter
declaration.

Element-wise computation algorithm:

1. Make a cartesian product of all element-wise arguments
2. Call the function repeatedly on each tuple of the product
3. Form the output set by concatenating the result of each
   function invocation.

.. code-block:: pseudo eql

    db> WITH A := {1, 2}, B := {3, 4}
    ... SELECT A * B;
    3
    4
    6
    8



::
    union(
        product(select_all('A'), select_all('B')),
        function(a, b) => a * b
    )

means that the function is called repeatedly
for every tuple in the cartesian product


- Element-wise.

  The output set can be derived by applying the same function to each
  individual input element (taken as a singleton) and merging the
  result with a union. This element-wise nature of a function is
  typical of basic arithmetic
  :ref:`operators<ref_edgeql_expressions_elops>`. This is also the
  default for user-defined functions in EdgeQL.

  .. code-block:: eschema

    # schema definition of a function that will be
    # applied in an element-wise fashion
    function plus_ten(int) -> int:
        from edgeql :>
            SELECT $0 + 10;

  In the above example only the input type without any additional
  qualifiers is given. This means that the function will be
  interpreted as an element-wise function. In particular this means
  that it will *not* be called on empty sets, since the result of any
  element-wise function applied to an empty set is an empty set.

- Element-wise with special handling of the empty set.

  For non-empty inputs the output set is produced exactly the same way
  as for a regular element-wise case. However, the function will be
  invoked for empty set input as well since it may produce some
  special output even in this case.

  .. code-block:: eschema

    # schema definition of a function that will be
    # applied in an element-wise fashion with special
    # handling of empty input
    function plus_ten2(optional int) -> int:
        from edgeql :>
            SELECT $0 + 10 IF EXISTS $0 ELSE 10;

  The above example works just like ``plus_ten``, but in addition
  produces the result of ``10`` even when the input is an empty set.
  Note that without the ``optional`` keyword ``plus_ten2`` would be
  functionally identical to ``plus_ten`` as it would never be invoked
  on empty input (regardless of the fact that it is capable of
  producing a non-empty result for it).

  This type of input handling is used by many EdgeQL operators. For
  example, it is used by the coalescing operator :eql:op:`??<COALESCE>`.

- Set as a whole.

  The output set is dependent on the entire input set and cannot be
  produced by merging outputs in an element-wise fashion.
  This is typical of aggregate functions, such as :eql:func:`sum` or
  :eql:func:`count`.

  .. code-block:: eschema

    # schema definition of a function that will be
    # applied to the input set as a whole
    function conatins_ten(set of int) -> bool:
        from edgeql :>
            SELECT 10 IN $0;

  The keywords ``set of`` mean that the input set works as a single
  entity. The output set for ``contains_ten`` is always a boolean
  singleton (either ``{TRUE}`` or ``{FALSE}``) and is independent of
  the input size.

It is important to note that these are technically properties of
function `parameters` and not the function overall. It is perfectly
possible to have a function that behaves in an element-wise fashion
w.r.t. one parameter and is aggregate-like w.r.t. another. In fact,
the EdgeQL operator :eql:op:`IN` has exactly this property.

There's another important interaction of function arguments. As long
as the arguments are independent of each other (i.e. they use
different symbols) the qualifiers in the function definition govern
how the function is applied as per the above. However, if the
arguments are dependent (i.e. they use the same symbols) then there's
an additional rule to resolve how the function is applied:

.. note::

    If even one of the arguments is element-wise, all arguments that
    are related to it must behave in an element-wise fashion
    regardless of the qualifiers.

This rule basically takes the principle that ":ref:`the same symbol
refers to the same thing<ref_edgeql_fundamentals_same>`" and applies
it to the function arguments. That's why if some symbol is interpreted
as an element-wise argument then it must be element-wise for all other
arguments of the same function.

Consider the following query:

.. code-block:: eql

    # the signature of built-in 'count':
    # function count(SET OF any) -> int

    WITH MODULE example
    SELECT count(Issue.watchers);

The function :eql:func:`count` normally treats the argument set as a
whole, so the query above counts the total number of distinct issue
watchers. To get a count of issue watchers on a per-issue basis, the
following query is needed:

.. code-block:: eql

    WITH MODULE example
    SELECT (Issue, count(Issue.watchers));

Tuples behave like element-wise functions w.r.t. all of their
elements. This means that the symbol ``Issue`` is treated as an
element-wise argument in this context. This, in turn, means that it
:eql:func:`count` is evaluated separately for each element of ``Issue``. So
the result is a set of tuples containing an issue and a watchers count for
that specific issue much like the simpler example of :ref:`user
name<ref_edgeql_fundamentals_same>`.


.. _ref_edgeql_fundamentals_scope:

Scope
-----

.. this section is going to need some more coherence

Scoping rules build on top of another rule: same symbol means the same
thing (in particular that means that same path prefixes mean the same
thing anywhere in the expression). Scoping rules specify when the same
symbols may refer to *different* entities. So the full rule can be
stated as follows:

.. note::

    Same symbols mean the same thing within any specific scope.

Every EdgeQL statement exists in its own scope. One can also envision
the current state of the DB as a base scope (or schema-level scope)
within which statements are defined. This schema-level scope notion is
relevant for understanding how ``DETACHED`` keyword works.

What creates a new scope? Any time a function with a ``SET OF``
argument is called, that argument exists in its own sub-scope (or
nested scope). Any nested scope is affected by all the enclosing
scopes, but any further refinement of a symbol's semantics do not
propagate back up. This also means that parallel (or sibling) scopes
do not affect each other's semantics.

.. code-block:: eql

    # Select first and last name for each user.
    WITH MODULE example
    SELECT (User.first_name,
            # this mention of 'User' is the same
            # as the one above
            User.last_name);

    # Select the counts of first and last names.
    # This is kind of trivial, but
    WITH MODULE example
    SELECT (
        # The argument to 'count' exists in its own sub-scope.
        # User.first_name and User.last_name in that sub-scope are
        # treated element-wise.
        count(User.first_name + User.last_name),

        # The argument to 'count' exists in a different sub-scope.
        # User.email in this sub-scope is not related to the
        # User.last_name above.
        count(User.email)
    );

Due to parallel sub-scopes, both :eql:func:`count` expressions are
evaluated on the input sets as a whole and not on a per-user basis
like in a tuple.

The ``DETACHED`` keyword creates a whole new scope, parallel to the
statement in which it appears, nested directly in the schema-level
scope.

Defining an alias via ``:=`` operator (whether in the ``WITH`` block
or elsewhere) puts the expression to the right of ``:=`` in a new sub-
scope.

.. code-block:: eql

    # select first and last name for each user
    WITH MODULE example
    SELECT (User.first_name,
            # this mention of 'User' is the same
            # as the one above
            User.last_name);

    # select all possible combinations of first and last names
    WITH MODULE example
    SELECT (User.first_name,
            # DETACHED keyword makes this mention of 'User'
            # completely unrelated to the one above
            DETACHED User.last_name);

One way to interpret any query is to follow these steps:

1) Find all ``DETACHED`` expressions and treat them as entirely
   separate from anything else within the statement. One way to think
   of this is to imagine that there's actually a schema-level view
   defined for each of the ``DETACHED`` expressions.

2) Resolve whether each particular function will be evaluated element-
   wise or not based on the ``SET OF`` scoping rules.

3) Treat every alias on the right side of ``:=`` as if it were a view
   defined in the schema to represent the set given by the left-hand-
   side expression.

.. _ref_edgeql_fundamentals_path:

.. potentially this section should be moved into operators since it
   covers `.`, `.>`, `.<`, `[IS ...]`, and `@`

Path Expressions
----------------

Path expressions (typically referred to as simply `paths`) are
fundamental building blocks of EdgeQL. A path defines a set of data in
EdgeDB (just like any other expression) based on the data type and
relationship with other data.

A path always starts with some ``concept`` as its `root` and it may
have an arbitrary number of `steps` following various ``links``. The
simplest path consists only of a `root` and is interpreted to mean
'all objects of the type `root`'.

.. code-block:: eql

    WITH MODULE example
    SELECT Issue;

In the above example ``Issue`` is a path that represents all objects in
the database of type ``Issue``. That is the result of the above query.

.. code-block:: eql

    WITH MODULE example
    SELECT Issue.owner;

The path ``Issue.owner`` consists of the `root` ``Issue`` and a `path
step` ``.owner``. It specifies the set of all objects that can be
reached from any object of type ``Issue`` by following its link
``owner``. This means that the above query will only retrieve users
that actually have at least one issue. The ``.`` operator in the path
separates `steps` and each step corresponds to a ``link`` name that
must be followed. By default, links are followed in the `outbound`
direction (the direction that is actually specified in the schema).
The direction of the link can be also specified explicitly by using
``>`` for `outbound` and ``<`` for `inbound`. Thus, the above query
can be rewritten more explicitly, but equivalently as:

.. code-block:: eql

    WITH MODULE example
    SELECT Issue.>owner;

To select all issues that actually have at least one watcher, it is
possible to construct a path using `inbound` link:

.. code-block:: eql

    WITH MODULE example
    SELECT User.<watchers;

The path in the above query specifies the set of all objects that can
be reached from ``User`` by following any ``link`` named ``watchers``
that has ``User`` as its target, back to the source of the ``link``.
In our case, there is only one link in the schema that is called
``watchers``. This link belongs to ``Issue`` and indeed it has
``User`` as its target, so the above query will get all the ``Issue``
objects that have at least one watcher. Only links that have a concept
as their target can be followed in the `inbound` direction. It is not
possible to follow inbound links on atoms.

Just like the direction of the step can be specified explicitly in a
path, so can the type of the link target. In order to retrieve all the
``SystemUsers`` that have actually created new ``Issues`` (as opposed
to ``Comments``) the following query could be made:

.. code-block:: eql

    WITH MODULE example
    SELECT Issue.owner[IS SystemUser];

In the above query the `path step` is expressed as ``owner[IS
SystemUser]``, where ``owner`` is the name of the link to follow, and
the qualifier ``[IS ...]`` specifies a restriction on the target's
type.

This is equivalent to:

.. code-block:: eql

    WITH MODULE example
    SELECT Issue.owner
    FILTER Issue.owner IS SystemUser;

The biggest difference between the two of the above representations is
that ``[IS SystemUser]`` allows to refer to links specific to
``SystemUser``.

Finally combining all of the above, it is possible to write a query to
retrieve all the ``Comments`` to ``Issues`` created by ``SystemUsers``:

.. code-block:: eql

    WITH MODULE example
    SELECT SystemUser.<owner[IS Issue].<issue;

    # or equivalently

    WITH MODULE example
    SELECT SystemUser
        # follow the link 'owner' to a source Issue
        .<owner[IS Issue]
        # follow the link 'issue' to a source Comment
        .<issue[IS Comment];

.. note::

    Links technically also belong to a module. Typically, the module
    doesn't need to be specified (because it is the default module or
    the link name is unambiguous), but sometimes it is necessary to
    specify the link module explicitly. The entire fully-qualified
    link name then needs to be enclosed in parentheses:

    .. code-block:: eql

        WITH MODULE some_module
        SELECT A.foo.bar;

Link properties
+++++++++++++++

It is possible to have a path that represents a set of link properties
as opposed to link target values. Since link properties have to be
atomic, the step pointing to the link property is always the last step
in a path. The link property is accessed by using ``@`` instead
of ``.``.

Consider the following schema:

.. code-block:: eschema

    link favorites:
        link property rank to int

    concept Post:
        required link body to str
        required link owner to User

    concept User extending std::Named:
        link favorites to Post:
            mapping := '**'

Then the query selecting all favorite Post sorted by their rank is:

.. code-block:: eql

    WITH MODULE example
    SELECT User.favorites
    ORDER BY User.favorites@rank;


.. THE BELOW IS STILL IN PROCESS OF REWRITING

The general structure of a simple EdgeQL query::

    [WITH [alias AS] MODULE module [,...] ]
    SELECT expression
    [FILTER expression]
    [ORDER BY expression [THEN ...]]
    [OFFSET expression]
    [LIMIT expression] ;

:eql:stmt:`SELECT`, ``FILTER``, ``ORDER BY``, ``OFFSET`` and ``LIMIT``
clauses are explained in more details in the
:ref:`Statements<ref_edgeql_statements>` section. ``WITH`` is a
convenience clause that optionally :ref:`assigns aliases<ref_edgeql_with>`
being used in the query. In particular the most common use of the
``WITH`` block is to provide a default module for the query.

Note that the only required clause in the query is ``SELECT`` itself.
Expressions in all query clauses act as set generators. ``FILTER``
clause can be used to restrict the selected set and ``ORDER BY`` is
used for sorting. ``OFFSET`` and ``LIMIT`` are used to return only a
part of the selected set.

For example, a query to get all issues reported by Alice Smith:

.. code-block:: eql

    SELECT example::Issue
    FILTER example::Issue.owner.name = 'Alice Smith';

A somewhat neater way of writing the same query is:

.. code-block:: eql

    WITH MODULE example
    SELECT Issue
    FILTER Issue.owner.name = 'Alice Smith';


Using expressions
-----------------

One of the basic units in EdgeQL are
:ref:`expressions<ref_edgeql_expressions>`. These always denote
objects or values. Basically, a concept instance is an object and
everything else is a value (more details can be found in the
:ref:`type system<ref_edgeql_types>` section).

.. code-block:: eql

    WITH MODULE example
    SELECT Issue
    FILTER Issue.owner.name = 'Alice Smith';

The above query has two examples of two kinds of expressions: path
expression and arithmetic expression.

Path expressions specify a set by starting with a concept and
following zero or more links from this concept to either atoms or
other concepts. The expressions ``Issue`` and ``Issue.owner.name`` are
examples of path expressions that point to a set of concepts and a set
of atoms, respectively.

Arithmetic expressions can be made out of other expressions by
applying various arithmetic operators, e.g. ``Issue.owner.name =
'Alice Smith'``. Because it is used in the ``FILTER`` clause, the
expression is evaluated for every member of the ``SELECT`` set and
used to filter out some of these members from the result.

.. code-block:: eql

    WITH MODULE example
    SELECT (
        SELECT Issue
        FILTER Issue.owner.name = 'Alice Smith'
    ).time_estimate;

The above query will return a set of time estimates for all of the
issues owned by Alice Smith rather than the ``Issue`` objects.

.. note::

    ``time_estimate`` is an *atomic value* (integer), so the resulting
    set can contain duplicate values. Every integer is effectively
    considered a distinct element of the set even when there are
    already set elements of the same value in the set. See
    :ref:`Everything is a set<ref_overview_set>` and
    :ref:`how expressions work<ref_edgeql_expressions>` for more
    details.

.. code-block:: eql

    WITH MODULE example
    SELECT (Issue.name, Issue.body)
    FILTER Issue.owner.name = 'Alice Smith';

The above query will return a set of 2-tuples containing the values of issue
``name`` and ``body`` for all of the issues owned by Alice Smith.
:eql:type:`tuples <tuple>` can be used in other
expressions as a whole opaque entity or serialized for some external
use. This construct is similar to selecting individual columns in SQL
except that the column name is lost. If structural information is
important `shapes` should be used instead.


.. _ref_edgeql_shapes:

Shapes
------

Shapes are a way of specifying which data should be retrieved for each
object. This annotation does not actually alter the objects in any
way, but rather provides a guideline for serialization.

Shapes define the *relationships structure* of the data that is
retrieved from the DB. Thus shapes themselves are a lexical
specification used with valid expressions denoting objects.

Shapes allow retrieving a set of objects as a `forest`, where each
base object is the root of a `tree`. Technically, this set of trees is
a directed graph possibly even containing cycles. However, the
serialized representation is based on a set of trees (or nested JSON).

Another use of shapes is *augmentation* of the object data. This can
be useful for serialization, but also as a convenient way of computing
some values used for filtering.

For example it's possible to augment each user object with the
information about how many issues they have:

.. code-block:: eql

    SELECT User {
        name,
        # "issues" is not a link in the schema, it is a computable
        # defined in the shape
        issues := count(User.<owner[IS Issue])
    };

Similarly, we can add a filter based on the number of issues that a
user has by referring to the :ref:`computable<ref_edgeql_computables>`
defined by the shape:

.. code-block:: eql

    SELECT User {
        name,
        issues := count(User.<owner[IS Issue])
    } FILTER User.issues > 5;

In order to refer to :ref:`computables<ref_edgeql_computables>` a
shape must be in the same lexical statement as the expression
referring to it.

.. note::

    Shapes serve an important function of pre-fetching specific data
    and *that data only* when serialized. For example, it's possible
    to fetch all issues with ``watchers`` restricted to a specific
    subset of users, then in the processing code safely refer to
    ``issue.watchers`` without further restrictions and only access
    the restricted set of watchers that was fetched.

    .. code-block:: eql

        SELECT Issue {
            name,
            text,
            # we only want real watchers, not internal
            # system accounts
            watchers: {
                name
            } FILTER Issue.watchers IS NOT SystemUser
        };


Using shapes
------------

:ref:`Shapes<ref_edgeql_shapes>` are the way of specifying structured
object data. They are used to get a set of `objects` and their
relationships in a structured way. Shape specification can be added to
any expression that denotes an object. Fundamentally, a shape
specification does not alter the identity of the objects it is
attached to, because it doesn't in any way change the existing
objects, but rather specifies additional data about them.

For example, a query that retrieves a set of ``Issue`` objects with
``name`` and ``body``, but no other information (like
``time_estimate``, ``owner``, etc.) for all of the issues owned by
Alice Smith, would look like this:

.. code-block:: eql

    WITH MODULE example
    SELECT
    Issue {
        name,
        body
    } FILTER Issue.owner.name = 'Alice Smith';

Shapes can be nested to retrieve more complex structures:

.. code-block:: eql

    WITH MODULE example
    SELECT Issue {  # base shape
        name,
        body,
        owner: {    # this is a nested shape
            name
        }
    };

The above query will retrieve all of the ``Issue`` objects. Each
object will have ``name``, ``body`` and ``owner`` links, where
``owner`` will also have a ``name``. To restrict this to only issues
that are not 'closed', the following query can be used:

.. code-block:: eql

    WITH MODULE example
    SELECT Issue {  # base shape
        name,
        body,
        owner: {    # this is a nested shape
            name
        }
    } FILTER Issue.status.name != 'closed';


To retrieve all users and their associated issues (if any), the following
shape query can be used:

.. code-block:: eql

    WITH MODULE example
    SELECT User {
        name,
        owned := (SELECT
            User.<owner[IS Issue] {
                number,
                body,
                status: {
                    name
                }
            }
        )
    };

By default only outbound links may be referred to in shapes directly
(like link ``status`` for the concept ``Issue``). Thus a computable
``owned`` is used to include data by following the inbound link
``owner`` to its origin. Since the link ``owner`` on ``Issue`` is
``*1`` (by default), when it is followed in the other direction is
functions as a ``1*``. So ``<owner`` points to a `set` of multiple
issues sharing a particular owner. For each issue the sub-shape for
the ``status`` link will be retrieved containing just the ``name``.

Note that the the sub-shape does not mandate that only the users that
*own* at least one ``Issue`` are returned, merely that *if* they have
some issues the names and bodies of these issues should be included in
the returned value. The query effectively says 'please return the set
of *all* users and provide this specific information for each of them
if available'. This is one of the important differences between
`shape` specification and a :ref:`path<ref_edgeql_fundamentals_path>`.

Shape annotation is preserved only by operations that preserve the
type (rather than specify a type or the result explicitly). In general
terms, any operation that maps :eql:type:`any` onto :eql:type:`any`
also preserves shapes, but operations that specify the types
explicitly (such as :eql:op:`+<PLUS>`, which is polymorphic, but
specifies :eql:type:`int64`, :eql:type:`float64`, or :eql:type:`str`
explicitly as the return type) effectively "remove" shape annotation
from the result.
