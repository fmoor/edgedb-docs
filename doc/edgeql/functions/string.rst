.. _ref_edgeql_functions_string:


String
======

    .. TODO::

        This whole section will need more explanation and details with
        rules, flags, etc.

.. eql:function:: std::lower(str) -> str

    :param $0: input string
    :paramtype $0: str

    :return: lowercase copy of the input string
    :returntype: str

    Return a lowercase copy of the input string.

    .. code-block:: eql

        SELECT lower('Some Fancy Title');
        # returns 'some fancy title'

.. eql:function:: std::re_match(str, str) -> array<str>

    :param $0: input string
    :paramtype $0: str
    :param $1: regular expression
    :paramtype $1: str

    :return: first matched groups as :eql:type:`array\<str\>`
    :returntype: array<str>

    Find the first regular expression match in a string.

    Given an input string and a regular expression string find the
    first match for the regular expression within the string. Return
    the match, each match represented by an :eql:type:`array\<str\>`
    of matched groups.

.. eql:function:: std::re_match_all(str, str) -> SET OF array<str>

    :param $0: input string
    :paramtype $0: str
    :param $1: regular expression
    :paramtype $1: str

    :return: set of all matched groups as :eql:type:`array\<str\>`
    :returntype: SET OF array<str>

    Find all regular expression matches in a string.

    Given an input string and a regular expression string repeatedly
    match the regular expression within the string. Return the set of
    all matches, each match represented by an :eql:type:`array\<str\>`
    of matched groups.

.. eql:function:: std::re_test(str, str) -> bool

    :param $0: input string
    :paramtype $0: str
    :param $1: regular expression
    :paramtype $1: str

    :return: ``TRUE`` if there is a match, ``FALSE`` otherwise
    :returntype: bool

    Test if a regular expression has a match in a string.

    Given an input string and a regular expression string test whether
    there is a match for the regular expression within the string.
    Return ``TRUE`` if there is a match, ``FALSE`` otherwise.
