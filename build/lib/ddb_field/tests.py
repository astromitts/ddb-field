import unittest


class FieldTests(unittest.TestCase):
    ''' Base class for tests that do not require database connectvity
    '''
    def setUp(self):
       pass

    def tearDown(self):
        pass

    def _execute_expectations(self, FieldClass, expectations):
        for result, inputs in expectations.items():
            if result.startswith('[') and result.endswith(']'):
                result = result.replace('[', '').replace(']', '').split(';')
                result = [r.strip() for r in result]
            elif  result.startswith('{') and result.endswith('}'):
                result_list = result.replace('{', '').replace('}', '').split(';')
                result = []
                for part in result_list:
                    parts = part.split(':')
                    result.append((parts[0].strip(), parts[1].strip()))
            if type(inputs) == list:
                for _inputs in inputs:
                    Field = FieldClass(_inputs[1], _inputs[0])
                    self.assertEquals(Field.value, result)
            else:
                Field = FieldClass(inputs[1], inputs[0])
                self.assertEquals(Field.value, result)



class FieldTests(FieldTests):
    def test_comma_formatter(self):
        from .ddb_field import comma_me
        num = comma_me(10000000000)
        self.assertTrue(num == '10,000,000,000')

        num = comma_me(100)
        self.assertTrue(num == '100')

    def test_default_field(self):
        from .ddb_field import Field

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

        self._execute_expectations(Field, expected_results)

    def test_field_properties(self):
        from .ddb_field import Field as FieldClass

        Field = FieldClass(
            {}, {'rawValue': 'test', 'foo': 'bananas', 'bar': 'ponies'})

        self.assertTrue('foo' in Field.display)
        self.assertTrue('bar' in Field.display)

    def test_textline(self):
        from .ddb_field import TextLine as Field

        expected_results = {
            'Winter is coming.': [
                ({'rawValue': 'winter is coming.'}, {'displayName': 'test'}),
                ({'rawValue': 'WINTER IS COMING.'}, {'displayName': 'test'}),
            ],
            'Winter Is Coming.': [
                ({'rawValue': 'winter is coming.'}, {'displayName': 'address'}),
                ({'rawValue': 'WINTER IS COMING.'}, {'displayName': 'address'}),
            ],
            'CA': [
                ({'rawValue': 'ca'}, {'displayName': 'state'}),
                ({'rawValue': 'CA'}, {'displayName': 'state'}),
            ],
            'NCAA II': [
                ({'rawValue': 'ncaa ii'}, {'displayName': 'association'}),
                ({'rawValue': 'ncaa II'}, {'displayName': 'association'}),
            ],
            '2000': [
                ({'rawValue': '2000'}, {'displayName': 'test'}),
                ({'rawValue': 2000}, {'displayName': 'test'}),
            ],
            '"hello"': [
                ({'rawValue': '\u201dhello\u201d'}, {'displayName': 'test'}),
                ({'rawValue': '\u201chello\u201c'}, {'displayName': 'test'}),
            ],
            "'hello'": [
                ({'rawValue': '\u2019hello\u2019'}, {'displayName': 'test'}),
                ({'rawValue': '\u2018hello\u2018'}, {'displayName': 'test'}),
            ],
            'N/A': [
                ({'rawValue': None}, {'displayName': 'test'}),
            ],

        }

        self._execute_expectations(Field, expected_results)

    def test_float_ratio(self):
        from .ddb_field import FloatRatio as Field

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

        self._execute_expectations(Field, expected_results)

    def test_usd_int(self):
        from .ddb_field import USDInt as Field
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

        self._execute_expectations(Field, expected_results)

    def test_usd_float(self):
        from .ddb_field import USDFloat as Field

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

        self._execute_expectations(Field, expected_results)

    def test_standard_percentage(self):
        from .ddb_field import STDPercentage as Field

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

        self._execute_expectations(Field, expected_results)

    def test_raw_percentage(self):
        from .ddb_field import RawPercentage as Field

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

        self._execute_expectations(Field, expected_results)

    def test_oracle_yesno(self):
        from .ddb_field import OracleYesNo as Field

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

        self._execute_expectations(Field, expected_results)

    def test_yesno(self):
        from .ddb_field import YesNo as Field

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

        self._execute_expectations(Field, expected_results)

    def test_delimited_field(self):
        from .ddb_field import DelimitedField as Field

        expected_results = {
            '[foo; baz; bat]': [
                ({'rawValue': 'foo; baz; bat;'}, {'delimiter': ';'}),
            ],
            '{foo: bananas; baz: ponies; bat: pumpkins}': [
                ({'rawValue': 'foo -- bananas; baz -- ponies; bat -- pumpkins;'},
                    {'delimiter': ';'}),
            ],
            'N/A': [
                ({'rawValue': None}, {}),
            ],

        }

        self._execute_expectations(Field, expected_results)

    def test_ranking_int(self):
        from .ddb_field import RankingInt as Field

        expected_results = {
            '1': [
                ({'rawValue': 1}, {}),
                ({'rawValue': '1'}, {}),
            ],
            '': [
                ({'rawValue': None}, {}),
            ],

        }

        self._execute_expectations(Field, expected_results)

    def test_int(self):
        from .ddb_field import Int as Field

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

        self._execute_expectations(Field, expected_results)

    def test_yearless_datetime(self):
        from .ddb_field import YearlessDatetime as Field

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
        self._execute_expectations(Field, expected_results)

    def test_phone(self):
        from .ddb_field import Phone as Field

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

        self._execute_expectations(Field, expected_results)

    def test_float(self):
        from .ddb_field import USNFloat as Field

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

        self._execute_expectations(Field, expected_results)


