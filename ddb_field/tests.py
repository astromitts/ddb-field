import unittest
from .ddb_field import DDBField


class FieldTestBase(unittest.TestCase):
    ''' Base class for tests that do not require database connectvity
    '''
    def setUp(self):
       pass

    def tearDown(self):
        pass

    def _execute_expectations(self, field_type=None, expectations={}):
        for result, inputs in expectations.items():
            if result.startswith('[') and result.endswith(']'):
                result = result.replace('[', '').replace(']', '').split(';')
                result = [r.strip() for r in result]
                print ('result: %s' % result)
            elif  result.startswith('{') and result.endswith('}'):
                result_list = result.replace('{', '').replace(
                    '}', '').split(';')
                result = []
                for part in result_list:
                    parts = part.split(':')
                    result.append((parts[0].strip(), parts[1].strip()))
                print ('result: %s' % result)

            for _inputs in inputs:
                print("testing %s for %s" % (_inputs[0]['rawValue'], result))
                if _inputs[1] and 'precision' in _inputs[1]:
                    precision = _inputs[1]['precision']
                else:
                    precision = None

                if _inputs[1] and 'case' in _inputs[1]:
                    case = _inputs[1]['case']
                else:
                    case = None

                if _inputs[1] and 'delimiter' in _inputs[1]:
                    delimiter = _inputs[1]['delimiter']
                else:
                    delimiter = ';'

                field = DDBField(
                    value=_inputs[0]['rawValue'],
                    field_type=field_type,
                    precision=precision,
                    case=case,
                    delimiter=delimiter,
                )
                self.assertEquals(field.Field.value, result)



class FieldTests(FieldTestBase):
    def test_comma_formatter(self):
        from .ddb_field import comma_me
        num = comma_me(10000000000)
        self.assertTrue(num == '10,000,000,000')

        num = comma_me(100)
        self.assertTrue(num == '100')

    def test_default_field(self):

        expected_results = {
            'winter is coming.': [
                ({'rawValue': 'winter is coming.'}, {}),
            ],
            '2000': [
                ({'rawValue': '2000'}, {}),
                ({'rawValue': 2000}, {}),
            ],
            'N/A': [
                ({'rawValue': None}, {}),
            ],

        }

        self._execute_expectations(expectations=expected_results)


    def test_textline(self):

        expected_results = {
            'Winter is coming.': [
                ({'rawValue': 'winter is coming.'}, {}),
                ({'rawValue': 'WINTER IS COMING.'}, {}),
            ],
            'Winter Is Coming.': [
                ({'rawValue': 'winter is coming.'}, {'case': 'title'}),
                ({'rawValue': 'WINTER IS COMING.'}, {'case': 'title'}),
            ],
            'CA': [
                ({'rawValue': 'ca'}, {'case': 'upper'}),
                ({'rawValue': 'CA'}, {'case': 'upper'}),
            ],
            'NCAA II': [
                ({'rawValue': 'ncaa ii'}, {'case': 'upper'}),
                ({'rawValue': 'ncaa II'}, {'case': 'upper'}),
            ],
            '2000': [
                ({'rawValue': '2000'}, {}),
                ({'rawValue': 2000}, {}),
            ],
            '"hello"': [
                ({'rawValue': '\u201dhello\u201d'}, {}),
                ({'rawValue': '\u201chello\u201c'}, {}),
            ],
            "'hello'": [
                ({'rawValue': '\u2019hello\u2019'}, {}),
                ({'rawValue': '\u2018hello\u2018'}, {}),
            ],
            'N/A': [
                ({'rawValue': None}, {}),
            ],

        }

        self._execute_expectations('textline', expected_results)

    def test_float_ratio(self):

        expected_results = {
            '45:1': [
                ({'rawValue': '45.558'}, {'precision': 0}),
                ({'rawValue': 45.558}, {'precision': 0}),
            ],
            '45.56:1': [
                ({'rawValue': '45.558'}, {'precision': 2}),
                ({'rawValue': 45.558}, {'precision': 2}),
            ],
            'N/A': [
                ({'rawValue': None}, {'precision': 0}),
                ({'rawValue': None}, {'precision': 2}),
            ],

        }

        self._execute_expectations('float_ratio', expected_results)

    def test_usd_int(self):
        expected_results = {
            '$45': [
                ({'rawValue': '45'}, {}),
                ({'rawValue': 45}, {}),
                ({'rawValue': '45.12'}, {}),
            ],
            'N/A': [
                ({'rawValue': None}, {}),
                ({'rawValue': None}, {}),
            ],

        }

        self._execute_expectations('usd_int', expected_results)

    def test_usd_float(self):

        expected_results = {
            '$45.00': [
                ({'rawValue': '45'}, {}),
                ({'rawValue': 45}, {}),
            ],
            '$45.35': [
                ({'rawValue': 45.35}, {}),
                ({'rawValue': '45.35'}, {}),
                ({'rawValue': 45.355}, {}),
            ],
            'N/A': [
                ({'rawValue': None}, {}),
                ({'rawValue': None}, {}),
            ],

        }

        self._execute_expectations('usd_float', expected_results)

    def test_standard_percentage(self):

        expected_results = {
            '100%': [
                ({'rawValue': 99.999999}, {'precision': 0}),
                ({'rawValue': '99.999999'}, {'precision': 0}),
                ({'rawValue': 100}, {'precision': 0}),
                ({'rawValue': '100'}, {'precision': 0}),
            ],
            '99.99%': [
                ({'rawValue': 99.99}, {'precision': 2}),
                ({'rawValue': '99.99'}, {'precision': 2}),
            ],
            'N/A': [
                ({'rawValue': None}, {'precision': 0}),
                ({'rawValue': None}, {'precision': 2}),
            ],

        }

        self._execute_expectations('std_percentage', expected_results)

    def test_raw_percentage(self):

        expected_results = {
            '100%': [
                ({'rawValue': .999999}, {'precision': 0}),
                ({'rawValue': '.999999'}, {'precision': 0}),
                ({'rawValue': 1}, {'precision': 0}),
                ({'rawValue': '1'}, {'precision': 0}),
            ],
            '99.99%': [
                ({'rawValue': .9999}, {'precision': 2}),
                ({'rawValue': '.9999'}, {'precision': 2}),
            ],
            'N/A': [
                ({'rawValue': None}, {'precision': 0}),
                ({'rawValue': None}, {'precision': 2}),
            ],
            'N/A': [
                ({'rawValue': 0}, {'precision': 0}),
                ({'rawValue': '0'}, {'precision': 2}),
            ],

        }

        self._execute_expectations('raw_percentage', expected_results)

    def test_oracle_yesno(self):

        expected_results = {
            'Yes': [
                ({'rawValue': 'Y'}, {}),
                ({'rawValue': 'y'}, {}),
                ({'rawValue': 'x'}, {}),
                ({'rawValue': 'X'}, {}),
                ({'rawValue': 'YES'}, {}),
                ({'rawValue': 1}, {}),
            ],
            'No': [
                ({'rawValue': None}, {}),
                ({'rawValue': 0}, {}),
                ({'rawValue': 'N'}, {}),
                ({'rawValue': 'False'}, {}),
            ],

        }

        self._execute_expectations('oracleyes_no', expected_results)

    def test_yesno(self):

        expected_results = {
            'Yes': [
                ({'rawValue': 'Y'}, {}),
                ({'rawValue': 'y'}, {}),
                ({'rawValue': 'x'}, {}),
                ({'rawValue': 'X'}, {}),
                ({'rawValue': 'YES'}, {}),
                ({'rawValue': 1}, {}),
            ],
            'No': [
                ({'rawValue': 0}, {}),
                ({'rawValue': 'N'}, {}),
                ({'rawValue': 'False'}, {}),
            ],
            'N/A': [
                ({'rawValue': None}, {}),
            ],

        }

        self._execute_expectations('yes_no', expected_results)

    def test_delimited_field(self):

        expected_results = {
            '[foo; baz; bat]': [
                ({'rawValue': 'foo; baz; bat;'}, {}),
                ({'rawValue': 'foo| baz| bat|'}, {'delimiter': '|'}),
            ],
            '{foo: bananas; baz: ponies; bat: pumpkins}': [
                (
                    {'rawValue':
                    'foo -- bananas; baz -- ponies; bat -- pumpkins;'},
                    {}
                ),
            ],
            'N/A': [
                ({'rawValue': None}, {}),
            ],

        }

        self._execute_expectations('delimited_field', expected_results)

    def test_ranking_int(self):

        expected_results = {
            '1': [
                ({'rawValue': 1}, {}),
                ({'rawValue': '1'}, {}),
            ],
            '': [
                ({'rawValue': None}, {}),
            ],

        }

        self._execute_expectations('ranking_int', expected_results)

    def test_int(self):

        expected_results = {
            '1': [
                ({'rawValue': 1}, {}),
                ({'rawValue': '1'}, {}),
            ],
            '1,000': [
                ({'rawValue': 1000}, {}),
                ({'rawValue': '1000'}, {}),
                ({'rawValue': '1,000'}, {}),
            ],
            '100,000': [
                ({'rawValue': 100000}, {}),
                ({'rawValue': '100000'}, {}),
                ({'rawValue': '100,000'}, {}),
            ],
            'N/A': [
                ({'rawValue': None}, {}),
            ],

        }

        self._execute_expectations('int', expected_results)

    def test_yearless_datetime(self):

        expected_results = {
            'September 10': [
                ({'rawValue': '1986-09-10'}, {}),
                ({'rawValue': '09/10'}, {}),
                ({'rawValue': '09-10-1986'}, {}),
                ({'rawValue': '09-10-86'}, {}),
                ({'rawValue': '09/10/86'}, {}),
            ],
            '09+10+1986': [
                ({'rawValue': '09+10+1986'}, {}),
            ],
            'N/A': [
                ({'rawValue': None}, {}),
            ],

        }
        self._execute_expectations('yearless_datetime', expected_results)

    def test_phone(self):

        expected_results = {
            '(800) 555-4444': [
                ({'rawValue': '8005554444'}, {}),
            ],
            '(800) 555-4444 ext. 456': [
                ({'rawValue': '8005554444456'}, {}),
            ],
            '456': [
                ({'rawValue': '456'}, {}),
            ],
            '': [
                ({'rawValue': None}, {}),
            ],

        }

        self._execute_expectations('phone', expected_results)

    def test_float(self):

        expected_results = {
            '1': [
                ({'rawValue': 1}, {'precision': 0}),
                ({'rawValue': '1'}, {'precision': 0}),
            ],
            '1.00': [
                ({'rawValue': 1.000}, {'precision': 2}),
                ({'rawValue': '1.000'}, {'precision': 2}),
                ({'rawValue': '1'}, {'precision': 2}),
            ],
            'N/A': [
                ({'rawValue': None}, {}),
            ],

        }

        self._execute_expectations('float', expected_results)


