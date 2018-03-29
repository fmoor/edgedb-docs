import contextlib
import os.path
import subprocess
import tempfile
import textwrap
import unittest

import requests_xml


class BuildFailedError(Exception):
    pass


class BaseDomainTest:

    def build(self, src, *, format='html'):
        src = textwrap.dedent(src)

        with tempfile.TemporaryDirectory() as td_in, \
                tempfile.TemporaryDirectory() as td_out:

            fn = os.path.join(td_in, 'contents.rst')
            with open(fn, 'wt') as f:
                f.write(src)
                f.flush()

            args = [
                'sphinx-build',
                '-b', format,
                '-W',
                '-C',
                '-D', 'extensions=edgedb.sphinxext',
                '-q',
                td_in,
                td_out,
                fn
            ]

            try:
                subprocess.run(
                    args, check=True,
                    stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            except subprocess.CalledProcessError as ex:
                msg = [
                    'The build has failed.',
                    '',
                    'STDOUT',
                    '======',
                    ex.stdout.decode(),
                    '',
                    'STDERR',
                    '======',
                    ex.stderr.decode(),
                    '',
                    'INPUT',
                    '=====',
                    src
                ]
                new_ex = BuildFailedError('\n'.join(msg))
                new_ex.stdout = ex.stdout.decode()
                new_ex.stderr = ex.stderr.decode()
                raise new_ex from ex

            with open(os.path.join(td_out, f'contents.{format}'), 'rt') as f:
                out = f.read()

            return out

    @contextlib.contextmanager
    def assert_fails(self, err):
        with self.assertRaises(BuildFailedError) as raised:
            yield

        self.assertRegex(raised.exception.stderr, err)


class TestEqlType(unittest.TestCase, BaseDomainTest):

    def test_eql_type_1(self):
        src = '''
        .. eql:type:: int

            descr
        '''

        with self.assert_fails('eql:type must include a namespace'):
            self.build(src)

    def test_eql_type_2(self):
        src = '''
        .. eql:type:: std::int
        '''

        with self.assert_fails('the directive must include a description'):
            self.build(src)

    def test_eql_type_3(self):
        src = '''
        .. eql:type:: std::int

            aaa

        Testing refs :eql:type:`int1`
        '''

        with self.assert_fails("cannot resolve :eql:type: targeting 'int1'"):
            self.build(src)

    def test_eql_type_4(self):
        src = '''
        .. eql:type:: std::int

            aaa

        Testing refs :eql:type:`int`
        '''

        self.assertRegex(
            self.build(src),
            r'(?x).*<a .* href="#std::int".*')

    def test_eql_type_5(self):
        src = '''
        .. eql:type:: std::int

            long text long text long text long text long text long text
            long text long text long text long text long text long text

            long text
        '''

        with self.assert_fails("shorter than 80 characters"):
            self.build(src)


class TestEqlFunction(unittest.TestCase, BaseDomainTest):

    def test_eql_func_1(self):
        src = '''
        .. eql:type:: std::int

            An integer.

        .. eql:function:: std::test(any) -> any

            :param $0: param
            :paramtype $0: int

            :return: something
            :returntype: any

            blah

        Testing :eql:func:`XXX <test>` ref.
        Testing :eql:func:`test` ref.
        '''

        out = self.build(src, format='xml')
        x = requests_xml.XML(xml=out)

        func = x.xpath('//desc[@desctype="function"]')
        self.assertEqual(len(func), 1)
        func = func[0]
        param, ret = func.xpath('//field')

        self.assertEqual(func.attrs['summary'], 'blah')

        self.assertEqual(
            param.attrs,
            {'eql-name': 'parameter', 'eql-paramname': '$0',
             'eql-paramtype': 'int'})

        self.assertEqual(
            ret.attrs,
            {'eql-name': 'return', 'eql-paramname': '',
             'eql-paramtype': 'any'})

        self.assertEqual(
            param.xpath('''
                //reference[@eql-type="type" and @refid="std::int"] /
                    literal_emphasis/text()
            '''),
            ['int'])

        self.assertEqual(
            x.xpath('''
                //paragraph /
                reference[@eql-type="function" and @refid="std::test"] /
                literal / text()
            '''),
            ['XXX', 'test()'])

    def test_eql_func_2(self):
        src = '''
        .. eql:function:: std::test() -> any

            :return: something
            :returntype: any

            long text long text long text long text long text long text
            long text long text long text long text long text long text

            long text
        '''

        with self.assert_fails("shorter than 80 characters"):
            self.build(src)

    def test_eql_func_3(self):
        src = '''
        .. eql:function:: std::test(any) -> any

            :param $0: aaaa
            :type $0: int

            blah
        '''

        expected = r'''(?xs)
        found\sunknown\sfield\s'type' .*
        Possible\sreason:\sfield\s'type'\sis\snot\ssupported
        '''

        with self.assert_fails(expected):
            self.build(src)

    def test_eql_func_4(self):
        src = '''
        .. eql:function:: std::test(any) -> any

            :param $0: aaaa
            :paramtype: int

            blah
        '''

        expected = r'''(?xs)
        found\sunknown\sfield\s'paramtype' .*
        Possible\sreason:\sfield\s'paramtype'\sis\snot\ssupported
        '''

        with self.assert_fails(expected):
            self.build(src)

    def test_eql_func_5(self):
        src = '''
        .. eql:function:: std::test(any) -> any

            :param $0: aaaa
            :paramtype $0: int

        blah
        '''

        with self.assert_fails('the directive must include a description'):
            self.build(src)

    def test_eql_func_6(self):
        src = '''
        .. eql:function:: std::test(any) -> any

            blah

            :param $0: aaaa
            :paramtype $0: int

            blah
        '''

        with self.assert_fails(
                'fields must be specified before all other content'):
            self.build(src)


class TestEqlOperator(unittest.TestCase, BaseDomainTest):

    def test_eql_op_1(self):
        src = '''
        .. eql:operator:: PLUS: A + B

            :optype A: int or str or bytes
            :optype B: int or str or bytes
            :returntype: int or str or bytes

            Arithmetic addition.

        some text

        :eql:op:`XXX <plus>`
        '''

        out = self.build(src, format='xml')
        x = requests_xml.XML(xml=out)

        self.assertEqual(
            len(x.xpath('''
                //desc_signature[@eql-name="plus" and @eql-signature="A + B"] /
                *[
                    (self::desc_annotation and text()="operator") or
                    (self::desc_name and text()="A + B")
                ]
            ''')),
            2)

        self.assertEqual(len(x.xpath('//field[@eql-name="operand"]')), 2)
        self.assertEqual(len(x.xpath('//field[@eql-name="returntype"]')), 1)

        self.assertEqual(
            x.xpath('''
                //paragraph /
                reference[@eql-type="operator" and @refid="operator::plus"] /
                literal / text()
            '''),
            ['XXX'])


class TestEqlKeyword(unittest.TestCase, BaseDomainTest):

    def test_eql_kw_1(self):
        src = '''
        .. eql:keyword:: SET-OF

            blah

        some text

        :eql:kw:`XXX <SET-OF>`
        '''

        out = self.build(src, format='xml')
        x = requests_xml.XML(xml=out)

        self.assertEqual(
            len(x.xpath('''
                //desc[@desctype="keyword"] /

                desc_signature[@eql-name="SET-OF"] /
                *[
                    (self::desc_annotation and text()="keyword") or
                    (self::desc_name and text()="SET OF")
                ]
            ''')),
            2)

        self.assertEqual(
            x.xpath('''
                //paragraph /
                reference[@eql-type="keyword" and @refid="keyword::set-of"] /
                literal / text()
            '''),
            ['XXX'])


class TestEqlStatement(unittest.TestCase, BaseDomainTest):

    def test_eql_stmt_1(self):
        src = '''
        .. eql:clause:: FILTER: aaa

            blah
        '''

        with self.assert_fails(
                'directive must be nested in a :eql:statement:'):
            self.build(src)

    def test_eql_stmt_2(self):
        src = '''
        .. eql:synopsis::

            blah
        '''

        with self.assert_fails(
                'directive must be nested in a :eql:statement:'):
            self.build(src)

    def test_eql_stmt_3(self):
        src = '''

        .. eql:statement:: SELECT
            :haswith:

            A short SELECT desc.

            .. eql:synopsis::

                code-syn-sample

            .. eql:clause:: FILTER: A FILTER B

                :paramtype A: any
                :paramtype B: SET OF any
                :returntype: any

                blah

        A ref to :eql:stmt:`SELECT`

        A ref to :eql:clause:`FLT <SELECT:FILTER>`.
        '''

        out = self.build(src, format='xml')
        x = requests_xml.XML(xml=out)

        self.assertEqual(
            x.xpath('''
                //desc[@desctype="statement"] // desc[@desctype="clause"] /
                desc_signature[@eql-fullname="filter"] / * / text()
            '''),
            ['clause', 'A FILTER B'])

        self.assertEqual(
            x.xpath('''
                //desc_content /
                literal_block[@language="pseudo-eql"] / text()
            '''),
            ['code-syn-sample'])

        self.assertEqual(
            x.xpath('''
                //paragraph /
                reference[@eql-type="statement" and
                          @refid="statement::select"] /
                literal / text()
            '''),
            ['SELECT'])

        self.assertEqual(
            x.xpath('''
                //paragraph /
                reference[@eql-type="clause" and
                          @refid="clause::select::filter"] /
                literal / text()
            '''),
            ['FLT'])