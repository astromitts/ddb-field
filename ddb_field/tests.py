import unittest
from .ddb_field import DDBField


class FieldTestBase(unittest.TestCase):
    ''' Base class for tests that do not require database connectvity
    '''
    def setUp(self):
        pass

    def tearDown(self):
        pass


class OrcYesNo(FieldTestBase):

    def test(self):

        field = DDBField('Y', 'oracleyes_no')
        self.assertEquals(field.Field.raw_value, 'Yes')
        self.assertEquals(field.Field.value, 'Yes')

        field = DDBField('y', 'oracleyes_no')
        self.assertEquals(field.Field.raw_value, 'Yes')
        self.assertEquals(field.Field.value, 'Yes')

        field = DDBField('x', 'oracleyes_no')
        self.assertEquals(field.Field.raw_value, 'Yes')
        self.assertEquals(field.Field.value, 'Yes')

        field = DDBField('X', 'oracleyes_no')
        self.assertEquals(field.Field.raw_value, 'Yes')
        self.assertEquals(field.Field.value, 'Yes')

        field = DDBField('yes', 'oracleyes_no')
        self.assertEquals(field.Field.raw_value, 'Yes')
        self.assertEquals(field.Field.value, 'Yes')

        field = DDBField(1, 'oracleyes_no')
        self.assertEquals(field.Field.raw_value, 'Yes')
        self.assertEquals(field.Field.value, 'Yes')

        field = DDBField(0, 'oracleyes_no')
        self.assertEquals(field.Field.raw_value, 'No')
        self.assertEquals(field.Field.value, 'No')

        field = DDBField('N', 'oracleyes_no')
        self.assertEquals(field.Field.raw_value, 'No')
        self.assertEquals(field.Field.value, 'No')

        field = DDBField(False, 'oracleyes_no')
        self.assertEquals(field.Field.raw_value, 'No')
        self.assertEquals(field.Field.value, 'No')

        field = DDBField(None, 'oracleyes_no')
        self.assertEquals(field.Field.raw_value, 'No')
        self.assertEquals(field.Field.value, 'No')


class YesNo(FieldTestBase):

    def test(self):

        field = DDBField('Y', 'yes_no')
        self.assertEquals(field.Field.raw_value, 'Yes')
        self.assertEquals(field.Field.value, 'Yes')

        field = DDBField('y', 'yes_no')
        self.assertEquals(field.Field.raw_value, 'Yes')
        self.assertEquals(field.Field.value, 'Yes')

        field = DDBField('x', 'yes_no')
        self.assertEquals(field.Field.raw_value, 'Yes')
        self.assertEquals(field.Field.value, 'Yes')

        field = DDBField('X', 'yes_no')
        self.assertEquals(field.Field.raw_value, 'Yes')
        self.assertEquals(field.Field.value, 'Yes')

        field = DDBField('yes', 'yes_no')
        self.assertEquals(field.Field.raw_value, 'Yes')
        self.assertEquals(field.Field.value, 'Yes')

        field = DDBField(1, 'yes_no')
        self.assertEquals(field.Field.raw_value, 'Yes')
        self.assertEquals(field.Field.value, 'Yes')

        field = DDBField(0, 'yes_no')
        self.assertEquals(field.Field.raw_value, None)
        self.assertEquals(field.Field.value, 'N/A')

        field = DDBField('N', 'yes_no')
        self.assertEquals(field.Field.raw_value, 'No')
        self.assertEquals(field.Field.value, 'No')

        field = DDBField(False, 'yes_no')
        self.assertEquals(field.Field.raw_value, 'No')
        self.assertEquals(field.Field.value, 'No')

        field = DDBField(None, 'yes_no')
        self.assertEquals(field.Field.raw_value, None)
        self.assertEquals(field.Field.value, 'N/A')


class DelimitedField(FieldTestBase):

    def test(self):
        field = DDBField('foo; baz; bat;', 'delimited_field')
        self.assertEquals(field.Field.raw_value, 'foo; baz; bat;')
        self.assertEquals(field.Field.value, ['foo', 'baz', 'bat'])

        field = DDBField('foo| baz| bat|', 'delimited_field', delimiter='|')
        self.assertEquals(field.Field.raw_value, 'foo| baz| bat|')
        self.assertEquals(field.Field.value, ['foo', 'baz', 'bat'])

        field = DDBField(
            'foo -- bananas; baz -- ponies; bat -- pumpkins;',
            'delimited_field')
        self.assertEquals(
            field.Field.raw_value,
            'foo -- bananas; baz -- ponies; bat -- pumpkins;'
        )
        self.assertEquals(
            field.Field.value,
            [('foo', 'bananas'), ('baz', 'ponies'), ('bat', 'pumpkins')]
        )

        field = DDBField(None, 'delimited_field', delimiter='|')
        self.assertEquals(field.Field.raw_value, None)
        self.assertEquals(field.Field.value, 'N/A')

        field = DDBField('N/A', 'delimited_field', delimiter='|')
        self.assertEquals(field.Field.raw_value, None)
        self.assertEquals(field.Field.value, 'N/A')


class DateTime(FieldTestBase):

    def test(self):
        field = DDBField('1986-09-10', 'yearless_datetime')
        self.assertEquals(field.Field.raw_value, 'September 10')
        self.assertEquals(field.Field.value, 'September 10')

        field = DDBField('09/10', 'yearless_datetime')
        self.assertEquals(field.Field.raw_value, 'September 10')
        self.assertEquals(field.Field.value, 'September 10')

        field = DDBField('09-10-1986', 'yearless_datetime')
        self.assertEquals(field.Field.raw_value, 'September 10')
        self.assertEquals(field.Field.value, 'September 10')

        field = DDBField('09-10-86', 'yearless_datetime')
        self.assertEquals(field.Field.raw_value, 'September 10')
        self.assertEquals(field.Field.value, 'September 10')

        field = DDBField('09/10/86', 'yearless_datetime')
        self.assertEquals(field.Field.raw_value, 'September 10')
        self.assertEquals(field.Field.value, 'September 10')

        field = DDBField('09+10+1986', 'yearless_datetime')
        self.assertEquals(field.Field.raw_value, '09+10+1986')
        self.assertEquals(field.Field.value, '09+10+1986')

        field = DDBField(None, 'yearless_datetime')
        self.assertEquals(field.Field.raw_value, None)
        self.assertEquals(field.Field.value, 'N/A')


class Phone(FieldTestBase):

    def test(self):

        field = DDBField('8005554444', 'phone')
        self.assertEquals(field.Field.raw_value, '(800) 555-4444')
        self.assertEquals(field.Field.value, '(800) 555-4444')

        field = DDBField('8005554444456', 'phone')
        self.assertEquals(field.Field.raw_value, '(800) 555-4444 ext. 456')
        self.assertEquals(field.Field.value, '(800) 555-4444 ext. 456')

        field = DDBField('456', 'phone')
        self.assertEquals(field.Field.raw_value, '456')
        self.assertEquals(field.Field.value, '456')

        field = DDBField(None, 'phone')
        self.assertEquals(field.Field.raw_value, None)
        self.assertEquals(field.Field.value, 'N/A')


class Float(FieldTestBase):

    def test_text_inputs(self):
        field = DDBField('1.5', 'float', precision=1)
        self.assertEquals(field.Field.raw_value, 1.5)
        self.assertEquals(field.Field.value, '1.5')

        field = DDBField('1.50', 'float', precision=1)
        self.assertEquals(field.Field.raw_value, 1.5)
        self.assertEquals(field.Field.value, '1.5')

        field = DDBField('1.55', 'float', precision=1)
        self.assertEquals(field.Field.raw_value, 1.6)
        self.assertEquals(field.Field.value, '1.6')

        field = DDBField('1.55', 'float', precision=2)
        self.assertEquals(field.Field.raw_value, 1.55)
        self.assertEquals(field.Field.value, '1.55')

        field = DDBField(
            '1.34874759152215799614643545279383429672',
            'float',
            precision=1
        )
        self.assertEquals(field.Field.raw_value, 1.3)
        self.assertEquals(field.Field.value, '1.3')

    def test_float_inputs(self):
        field = DDBField(1.5, 'float', precision=1)
        self.assertEquals(field.Field.raw_value, 1.5)
        self.assertEquals(field.Field.value, '1.5')

        field = DDBField(1.55, 'float', precision=1)
        self.assertEquals(field.Field.raw_value, 1.6)
        self.assertEquals(field.Field.value, '1.6')

        field = DDBField(1.55, 'float')
        self.assertEquals(field.Field.raw_value, 2)
        self.assertEquals(field.Field.value, '2')

        field = DDBField(
            1.34874759152215799614643545279383429672,
            'float',
            precision=1
        )
        self.assertEquals(field.Field.raw_value, 1.3)
        self.assertEquals(field.Field.value, '1.3')

        field = DDBField(48.99, 'float', precision=1)
        self.assertEquals(field.Field.raw_value, 49)
        self.assertEquals(field.Field.value, '49')

        field = DDBField(48.999, 'float', precision=2)
        self.assertEquals(field.Field.raw_value, 49)
        self.assertEquals(field.Field.value, '49')

        field = DDBField(48.991, 'float', precision=2)
        self.assertEquals(field.Field.raw_value, 48.99)
        self.assertEquals(field.Field.value, '48.99')

        field = DDBField(48.91, 'float', precision=1)
        self.assertEquals(field.Field.raw_value, 48.9)
        self.assertEquals(field.Field.value, '48.9')


class Int(FieldTestBase):

    def test_text_inputs(self):
        field = DDBField('1.9', 'int')
        self.assertEquals(field.Field.raw_value, 2)
        self.assertEquals(field.Field.value, '2')

        field = DDBField('1.50', 'int')
        self.assertEquals(field.Field.raw_value, 2)
        self.assertEquals(field.Field.value, '2')

        field = DDBField('1.55', 'int')
        self.assertEquals(field.Field.raw_value, 2)
        self.assertEquals(field.Field.value, '2')

        field = DDBField('1.2', 'int')
        self.assertEquals(field.Field.raw_value, 1)
        self.assertEquals(field.Field.value, '1')

        field = DDBField('1', 'int')
        self.assertEquals(field.Field.raw_value, 1)
        self.assertEquals(field.Field.value, '1')

        field = DDBField('.5', 'int')
        self.assertEquals(field.Field.raw_value, 1)
        self.assertEquals(field.Field.value, '1')

    def test_int_inputs(self):
        field = DDBField(1.9, 'int')
        self.assertEquals(field.Field.raw_value, 2)
        self.assertEquals(field.Field.value, '2')

        field = DDBField(1.50, 'int')
        self.assertEquals(field.Field.raw_value, 2)
        self.assertEquals(field.Field.value, '2')

        field = DDBField(1.55, 'int')
        self.assertEquals(field.Field.raw_value, 2)
        self.assertEquals(field.Field.value, '2')

        field = DDBField(1.2, 'int')
        self.assertEquals(field.Field.raw_value, 1)
        self.assertEquals(field.Field.value, '1')

        field = DDBField(1, 'int')
        self.assertEquals(field.Field.raw_value, 1)
        self.assertEquals(field.Field.value, '1')

        field = DDBField(.5, 'int')
        self.assertEquals(field.Field.raw_value, 1)
        self.assertEquals(field.Field.value, '1')

    def test_comma_adds(self):
        field = DDBField(3000, 'int')
        self.assertEquals(field.Field.raw_value, 3000)
        self.assertEquals(field.Field.value, '3,000')

        field = DDBField('3000', 'int')
        self.assertEquals(field.Field.raw_value, 3000)
        self.assertEquals(field.Field.value, '3,000')


class FloatRatio(FieldTestBase):

    def test(self):
        field = DDBField('21', 'float_ratio')
        self.assertEquals(field.Field.value, '21:1')
        self.assertEquals(field.Field.raw_value, 21)

        field = DDBField('2,100', 'float_ratio')
        self.assertEquals(field.Field.value, '2,100:1')
        self.assertEquals(field.Field.raw_value, 2100)


class USDInt(FieldTestBase):

    def test(self):
        field = DDBField('1', 'usd_int')
        self.assertEquals(field.Field.raw_value, 1)
        self.assertEquals(field.Field.value, '$1')

        field = DDBField(1, 'usd_int')
        self.assertEquals(field.Field.raw_value, 1)
        self.assertEquals(field.Field.value, '$1')

        field = DDBField(1000, 'usd_int')
        self.assertEquals(field.Field.raw_value, 1000)
        self.assertEquals(field.Field.value, '$1,000')

        field = DDBField(None, 'usd_int')
        self.assertEquals(field.Field.raw_value, None)
        self.assertEquals(field.Field.value, 'N/A')


class USDFloat(FieldTestBase):

    def test(self):
        field = DDBField('1', 'usd_float')
        self.assertEquals(field.Field.raw_value, 1)
        self.assertEquals(field.Field.value, '$1')

        field = DDBField(1, 'usd_float')
        self.assertEquals(field.Field.raw_value, 1)
        self.assertEquals(field.Field.value, '$1')

        field = DDBField(1.55, 'usd_float')
        self.assertEquals(field.Field.raw_value, 1.55)
        self.assertEquals(field.Field.value, '$1.55')

        field = DDBField(1000, 'usd_float')
        self.assertEquals(field.Field.raw_value, 1000)
        self.assertEquals(field.Field.value, '$1,000')

        field = DDBField(None, 'usd_float')
        self.assertEquals(field.Field.raw_value, None)
        self.assertEquals(field.Field.value, 'N/A')


class StdPct(FieldTestBase):

    def test(self):
        field = DDBField('1', 'std_percentage')
        self.assertEquals(field.Field.raw_value, 1)
        self.assertEquals(field.Field.value, '1%')

        field = DDBField(1, 'std_percentage')
        self.assertEquals(field.Field.raw_value, 1)
        self.assertEquals(field.Field.value, '1%')

        field = DDBField(100, 'std_percentage')
        self.assertEquals(field.Field.raw_value, 100)
        self.assertEquals(field.Field.value, '100%')

        field = DDBField(None, 'std_percentage')
        self.assertEquals(field.Field.raw_value, None)
        self.assertEquals(field.Field.value, 'N/A')


class RawPct(FieldTestBase):

    def test_string_inputs(self):
        field = DDBField('1', 'raw_percentage')
        self.assertEquals(field.Field.raw_value, 100)
        self.assertEquals(field.Field.value, '100%')

        field = DDBField('.999999', 'raw_percentage')
        self.assertEquals(field.Field.raw_value, 100)
        self.assertEquals(field.Field.value, '100%')

        field = DDBField('.9999', 'raw_percentage', precision=2)
        self.assertEquals(field.Field.raw_value, 99.99)
        self.assertEquals(field.Field.value, '99.99%')

    def test_number_inputs(self):
        field = DDBField(1, 'raw_percentage')
        self.assertEquals(field.Field.raw_value, 100)
        self.assertEquals(field.Field.value, '100%')

        field = DDBField(.999999, 'raw_percentage')
        self.assertEquals(field.Field.raw_value, 100)
        self.assertEquals(field.Field.value, '100%')

        field = DDBField(.9999, 'raw_percentage', precision=2)
        self.assertEquals(field.Field.raw_value, 99.99)
        self.assertEquals(field.Field.value, '99.99%')

    def test_na(self):
        field = DDBField(None, 'raw_percentage')
        self.assertEquals(field.Field.raw_value, None)
        self.assertEquals(field.Field.value, 'N/A')


class TextLine(FieldTestBase):

    def test(self):
        field = DDBField('winter is coming', 'textline')
        self.assertEquals(field.Field.raw_value, 'Winter is coming')
        self.assertEquals(field.Field.value, 'Winter is coming')

    def test_casing(self):
        field = DDBField('winter is coming', 'textline', case='upper')
        self.assertEquals(field.Field.raw_value, 'WINTER IS COMING')
        self.assertEquals(field.Field.value, 'WINTER IS COMING')

        field = DDBField('winter is coming', 'textline', case='title')
        self.assertEquals(field.Field.raw_value, 'Winter Is Coming')
        self.assertEquals(field.Field.value, 'Winter Is Coming')

    def test_na(self):
        field = DDBField('N/A', 'textline')
        self.assertEquals(field.Field.raw_value, None)
        self.assertEquals(field.Field.value, 'N/A')

        field = DDBField('n/a', 'textline')
        self.assertEquals(field.Field.raw_value, None)
        self.assertEquals(field.Field.value, 'N/A')

        field = DDBField(None, 'textline')
        self.assertEquals(field.Field.raw_value, None)
        self.assertEquals(field.Field.value, 'N/A')

        field = DDBField('N/a', 'textline')
        self.assertEquals(field.Field.raw_value, None)
        self.assertEquals(field.Field.value, 'N/A')
