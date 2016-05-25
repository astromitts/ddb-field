import datetime
import math
import re
from collections import OrderedDict


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
        self.vocabulary = {}
        self.precision=precision
        self.sort_as = "Text"
        self.case = case
        self.delimiter = delimiter
        self.convert()
        # TODO: Re-implement vocabulary
        # if self.field_metadata['displayName'] in vocabulary:
        #     self.vocabulary = vocabulary[self.field_metadata['displayName']]
        # if self.value in self.vocabulary:
        #     self.value = self.vocabulary[self.value]

        if self.value is None or self.value == 'None':
            self.value = ''

    @classmethod
    def convert(self):
        stringify_list = (float, bool, int, datetime.date)
        if self.value:
            if isinstance(self.value, stringify_list):
                self.value = str(self.value)
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


class USNFloat(Field):
    sort_as = "Float"

    @classmethod
    def convert(self):
        if self.value:
            if self.precision == 0:
                self.value = math.trunc(float(self.value))
            elif self.precision is not None:
                self.value = round(
                    float(self.value), self.precision)
                parts = str(self.value).split('.')
                dollars = parts[0]
                cents = parts[1].rjust( self.precision, '0')
                self.value = dollars + '.' + cents
            self.value = str(self.value)
        else:
            self.value = 'N/A'


class FloatRatio(Field):
    sort_as = "Float"

    @classmethod
    def convert(self):
        if self.value:
            self.value = float(self.value)
            if self.precision == 0:
                self.value = math.trunc(self.value)
            elif self.precision is not None:
                self.value = round(
                    self.value, self.precision)
            self.value = str(self.value) + ':1'
        else:
            self.value = 'N/A'


class USDFloat(Field):
    sort_as = "Float"

    @classmethod
    def convert(self):
        if self.value:
            self.value = '$%s' % str(round(float(self.value), 2))
            parts = self.value.split('.')
            dollars = parts[0]
            cents = parts[1].rjust(2, '0')
            self.value = dollars + '.' + cents
        else:
            self.value = 'N/A'


class USDInt(Field):
    sort_as = "Integer"

    @classmethod
    def convert(self):
        if self.value:
            self.value = '$%s' % comma_me(
                str(math.trunc(round(float(self.value)))))
        else:
            self.value = 'N/A'


class STDPercentage(Field):
    sort_as = "Float"

    @classmethod
    def convert(self):
        if self.value:
            if not isinstance(self.value, (int, float, complex)):  # noqa
                try:
                    self.value = float(self.value)
                except Exception:
                    self.value = 'N/A'
                    return
            if self.value == 0:
                self.value = 'N/A'
                return
            if self.precision == 0 or self.precision is None:
                self.value = math.trunc(round(self.value))
            elif self.precision is not None:
                self.value = round(self.value, self.precision)
            self.value = str(self.value) + '%'
        else:
            self.value = 'N/A'


class RawPercentage(Field):
    sort_as = "Float"

    @classmethod
    def convert(self):
        if self.value:
            self.value = float(self.value) * 100
            if self.value == 0:
                self.value = 'N/A'
                return
            if self.precision == 0 or self.precision is None:
                self.value = math.trunc(round(self.value))
            elif self.precision is not None:
                self.value = round(self.value, self.precision)
            self.value = str(self.value) + '%'
        else:
            self.value = 'N/A'


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
            self.value = None


class RankingInt(Field):
    sort_as = "Integer"

    @classmethod
    def convert(self):
        if self.value:
            self.value = '%s' % self.value
        else:
            self.value = ''


class Int(Field):
    sort_as = "Integer"

    @classmethod
    def convert(self):
        if not self.value:
            self.value =  'N/A'
        elif int(str(self.value).replace(',','')) < 1000:
            self.value = '%s' % self.value
        else:
            self.value = str(comma_me(str(self.value)))



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

class DDBField(object):

    @classmethod
    def __init__(self, field_type):
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

        if field_type in field_map:
            self.FieldClass = field_map[field_type]
        else:
            self.FieldClass = default_field_model
