import datetime
import re
from collections import OrderedDict
from copy import deepcopy


def comma_me(amount):
    orig = amount
    new = re.sub("^(-?\d+)(\d{3})", '\g<1>,\g<2>', str(amount))
    if orig == new:
        return new
    else:
        return comma_me(new)


class Field(object):
    @classmethod
    def __init__(self, raw_value, precision=None, case=None, delimiter=';',
                 vocabulary={}):
        self.value = raw_value
        self.raw_value = None
        self.vocabulary = {}
        self.precision=precision
        self.sort_as = "Text"
        self.case = case
        self.delimiter = delimiter
        self.convert()
        self.set_raw()
        # TODO: Re-implement vocabulary
        # if self.field_metadata['displayName'] in vocabulary:
        #     self.vocabulary = vocabulary[self.field_metadata['displayName']]
        # if self.value in self.vocabulary:
        #     self.value = self.vocabulary[self.value]


    @classmethod
    def convert(self):
        stringify_list = (float, bool, int, datetime.date)
        if self.value:
            if isinstance(self.value, stringify_list):
                self.value = str(self.value)
        else:
            self.value = 'N/A'

    @classmethod
    def set_raw(self):
        pass

    @classmethod
    def _round_decimal(self, decimal, whole):
        vallist = []
        decimal = decimal.ljust(self.precision + 1, '0')
        for i in decimal:
            vallist.append(i)
        int_vals = [int(i) for i in vallist]
        test_num = int_vals[self.precision]
        cutoff_num = int_vals[self.precision - 1]
        if test_num > cutoff_num or test_num == 5:
            int_vals[self.precision - 1] = int_vals[self.precision - 1] + 1
        if self.precision == 0 and int(int_vals[0]) >= 5:
            whole = int(whole or 0) + 1
            return whole
        ind = 0
        rounded_decimal = []
        for i in int_vals:
            if ind < self.precision:
                rounded_decimal.append(str(i))
            ind += 1
        rounded_decimal = ('').join(rounded_decimal)
        return float('%s.%s' % (whole, rounded_decimal))



    @classmethod
    def _parse_number(self, value, precision=0, comma=True):
        precision = precision or 0
        if value and str(value).lower() not in ['none', 'n/a']:
            strval = str(value).replace(',', '')
            try:
                numval = float(strval)
            except ValueError:
                return None, None
            # force round up on .*5 (python does not do this out of the box)
            if '.' in strval:
                parts = strval.split('.')
                dollars = parts[0]
                cents = parts[1]
                rounded_decimal = self._round_decimal(cents, dollars)
                numval = float(rounded_decimal)
            else:
                numval = round(numval, precision)

            if float(numval).is_integer():
                numval = int(numval)

            strval = str(deepcopy(numval))

            if comma:
                if '.' in strval:
                    parts = strval.split('.')
                    dollars = comma_me(parts[0])
                    cents = parts[1]
                    strval = '%s.%s' % (dollars, cents)
                else:
                    strval = comma_me(strval)

            return strval, numval

        else:
            return value, None


class Int(Field):

    @classmethod
    def convert(self):
        self.sort_as = "Integer"
        if not self.value:
            self.value =  'N/A'
            return
        self.precision = 0
        if self.value:
            self.value, self.raw_value = self._parse_number(
                self.value, self.precision)


class USNFloat(Field):

    @classmethod
    def convert(self):
        self.sort_as = "Float"
        if self.value:
            self.value, self.raw_value = self._parse_number(
                self.value, self.precision)
        else:
            self.value = 'N/A'
            self.raw_value = None


class FloatRatio(Field):

    @classmethod
    def convert(self):
        self.sort_as = "Float"
        if self.value:
            self.value, self.raw_value = self._parse_number(
                self.value, self.precision)
            if self.value:
                self.value = str(self.value) + ':1'
            else:
                self.value = 'N/A'
                self.raw_value = None
        else:
            self.value = 'N/A'


class USDFloat(Field):

    @classmethod
    def convert(self):
        self.sort_as = "Float"
        self.precision = 2
        if self.value:
            self.value, self.raw_value = self._parse_number(
                self.value, self.precision)
            if self.value:
                self.value = '$%s' % self.value
            else:
                self.value = 'N/A'
                self.raw_value = None
        else:
            self.value = 'N/A'
            self.raw_value = None


class USDInt(Field):

    @classmethod
    def convert(self):
        self.sort_as = "Integer"
        self.precision = 0
        if self.value:
            self.value, self.raw_value = self._parse_number(
                self.value, self.precision)
            if self.value:
                self.value = '$%s' % self.value
            else:
                self.value = 'N/A'
                self.raw_value = None
        else:
            self.value = 'N/A'


class STDPercentage(Field):

    @classmethod
    def convert(self):
        self.sort_as = "Float"
        self.precision = self.precision or 0
        if self.value:
            self.value, self.raw_value = self._parse_number(
                self.value, self.precision)
            if self.value:
                self.value = self.value + '%'
            else:
                self.value = 'N/A'
                self.raw_value = None
        else:
            self.value = 'N/A'


class RawPercentage(Field):

    @classmethod
    def convert(self):
        self.sort_as = "Float"
        self.precision = self.precision or 0
        if self.value:
            self.value = float(self.value) * 100
            if self.value == 0:
                self.value = 'N/A'
                return
            self.value, self.raw_value = self._parse_number(
                self.value, self.precision)
            if self.value:
                self.value = self.value + '%'
            else:
                self.value = 'N/A'
                self.raw_value = None
        else:
            self.value = 'N/A'


class TextLine(Field):
    @classmethod
    def convert(self):
        char_map = {
            u"\u2018": "'",
            u"\u2019": "'",
            u"\u201c": "\"",
            u"\u201d": "\"",
        }
        if self.value and str(self.value).upper() == 'N/A':
            self.value = 'N/A'
            self.raw_value = None
            return
        if self.value:
            self.value = str(self.value)
            for bad_char, good_char in char_map.items():
                self.value = self.value.replace(bad_char, good_char)
            if self.case == 'upper':
                self.value = self.value.upper()

            elif self.case == 'title':
                self.value = self.value.title()

            else:
                self.value = self.value.capitalize()
        else:
            self.value = 'N/A'

    @classmethod
    def set_raw(self):
        if self.value and self.value != 'N/A':
            self.raw_value = self.value


class YesNo(Field):
    ''' A value that is not empty and not a "yes" value must be present for
        this to be "no", else it is N/A
    '''
    @classmethod
    def convert(self):
        if self.value is not None:
            if str(self.value).lower() in ('x', 'yes', 'y', 'Y', '1'):
                self.value = 'Yes'
            else:
                self.value = 'No'
        else:
            self.value = 'N/A'

    @classmethod
    def set_raw(self):
        if self.value and self.value != 'N/A':
            self.raw_value = self.value


class OracleYesNo(Field):
    ''' Oracle Yes/No is different from regular Yes/No because an Oracle
        Yes/No is presumed to be No if empty, instead of N/A
    '''
    @classmethod
    def convert(self):
        if self.value is not None:
            if str(self.value).lower() in ('x', 'yes', 'y', '1', 'true', '1'):
                self.value = 'Yes'
            else:
                self.value = 'No'
        else:
            self.value = 'No'

    @classmethod
    def set_raw(self):
        if self.value and self.value != 'N/A':
            self.raw_value = self.value


class YearlessDatetime(Field):
    @classmethod
    def convert(self):
        if self.value:
            formats = [
                '%Y-%m-%d',
                '%m/%d',
                '%m-%d-%Y',
                '%m/%d/%Y',
                '%m-%d-%y',
                '%m/%d/%y',

            ]
            out_val = None
            for format in formats:
                try:
                    out_val = datetime.datetime.strptime(
                        str(self.value), format).strftime('%B %d')
                    break
                except ValueError:
                    pass

            self.value = out_val or self.value
        else:
            self.value = 'N/A'

    @classmethod
    def set_raw(self):
        if self.value and self.value != 'N/A':
            self.raw_value = self.value


class Phone(Field):
    @classmethod
    def convert(self):
        if self.value and self.value != '':
            if len(self.value) < 10:
                self.value = self.value
                return
            extension = ''
            if len(self.value) > 10:
                extension = ' ext. %s' % self.value[10:]
            self.value = '(%s) %s-%s%s' % (  # noqa
                self.value[:3], self.value[3:6], self.value[6:10], extension)
        else:
            self.value = 'N/A'

    @classmethod
    def set_raw(self):
        if self.value and self.value != 'N/A':
            self.raw_value = self.value


class RankingInt(Field):

    @classmethod
    def convert(self):
        self.sort_as = "Integer"
        if self.value:
            self.value = '%s' % self.value
        else:
            self.value = ''


class DelimitedField(Field):
    @classmethod
    def convert(self):
        if self.value:
            if ' -- ' in self.value:
                parts = self.value.split(self.delimiter)
                self.value = []
                for part in parts:
                    string_parts = part.split('--')
                    if len(string_parts) > 1:
                        self.value.append(
                            (string_parts[0].strip(), string_parts[1].strip())
                        )
            else:
                parts = self.value.split(self.delimiter)
                self.value = [p.strip() for p in parts if p.strip() != '']
        else:
            self.value = 'N/A'

    @classmethod
    def set_raw(self):
        if self.value and self.value != 'N/A':
            self.raw_value = self.value


class DDBField(object):

    @classmethod
    def __init__(self, value, field_type=None, precision=None,
                 case=None, delimiter=';',):
        _default_field_model = Field
        _field_map = {
            'float': USNFloat,
            'float_ratio': FloatRatio,
            'textline': TextLine,
            'usd_float': USDFloat,
            'usd_int': USDInt,
            'std_percentage': STDPercentage,
            'raw_percentage': RawPercentage,
            'yes_no': YesNo,
            'oracleyes_no': OracleYesNo,
            'yearless_datetime': YearlessDatetime,
            'phone': Phone,
            'ranking_int': RankingInt,
            'ranking_string': RankingInt,
            'int': Int,
            'delimited_field': DelimitedField,
        }

        if field_type and field_type in _field_map:
            self.Field = _field_map[field_type]
        else:
            self.Field = _default_field_model

        self.field_type = field_type

        self.Field(
            value,
            precision=precision,
            case=case,
            delimiter=delimiter
        )
