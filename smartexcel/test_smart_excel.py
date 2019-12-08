import os
import unittest
import psycopg2
from .smart_excel import SmartExcel

DUMMY_DEFINITION = [
    {
        'func': 'add_group_column',
        'kwargs': {
            'columns': [
                {
                    'name': 'NAME',
                    'key': 'name',
                    'validations': {
                        'excel': {
                            'validate': 'length',
                            'criteria': '>=',
                            'value': 0,
                            'input_title': 'Your name:'
                        }
                    }
                },
                {
                    'name': 'AGE',
                    'key': 'age',
                    'validations': {
                        'list_source_func': 'get_age_list'
                    }
                },
                {
                    'name': 'CITY OF BIRTH',
                    'key': 'city',
                    'validations': {
                        'list_source_func': 'get_city_list'
                    }
                }
            ]
        }
    }
]


class Dummy():
    def __init__(self, data):
        self.name = data['name']
        self.age = data['age']
        self.city = data['city']


class DummyData():
    def __init__(self):
        self.results = [
            Dummy({
                'name': 'PA',
                'age': 29,
                'city': 'Paris'
            }),
            Dummy({
                'name': 'Cairo',
                'age': 0,
                'city': 'Muizenberg'
            }),
            Dummy({
                'name': 'Carina',
                'age': 26,
                'city': 'Windhoek'
            })
        ]


    def write_name(self, instance, kwargs={}):
        return instance.name

    def write_age(self, instance, kwargs={}):
        return instance.age

    def write_city(self, instance, kwargs={}):
        return instance.city

    def get_age_list(self):
        return [i for i in range(0, 99)]

    def get_city_list(self):
        return [
            'Paris',
            'Muizenberg',
            'Windhoek',
            'Saint-Dizier'
        ]

    def write_get_repeat_func(self):
        return len(self.results)

    def write_get_name_func(self, instance, kwargs={}):
        return self.results[kwargs['index']].name


class TestSmartExcelDump(unittest.TestCase):
    def setUp(self):
        self.definition = DUMMY_DEFINITION
        self.data = DummyData()
        self.filepath = 'hello.xlsx'
        # /tmp/dummy_test.xlsx'

        if os.path.exists(self.filepath):
            os.remove(self.filepath)


    def runTest(self):
        self.assertFalse(os.path.exists(self.filepath))
        excel = SmartExcel(
            definition=self.definition,
            data=self.data,
            output=self.filepath
        )
        excel.dump()
        self.assertTrue(os.path.exists(self.filepath))
        self.assertTrue(excel.WRITEMODE)


class TestSmartExcelParse(unittest.TestCase):
    def setUp(self):
        self.definition = DUMMY_DEFINITION
        self.data = DummyData()
        self.filepath = '/tmp/dummy_test.xlsx'

        if os.path.exists(self.filepath):
            os.remove(self.filepath)

        SmartExcel(
            definition=self.definition,
            data=self.data,
            output=self.filepath
        ).dump()

    def test_parse(self):
        excel = SmartExcel(
            definition=self.definition,
            data=self.data,
            path=self.filepath
        )
        data = excel.parse()

        self.assertEqual(data, [
            {'name': 'PA', 'age': 29, 'city': 'Paris'},
            {'name': 'Cairo', 'age': 0, 'city': 'Muizenberg'},
            {'name': 'Carina', 'age': 26, 'city': 'Windhoek'}])



from .fbf.data_model import FbfFloodData
from .fbf.definition import FBF_DEFINITION
class TestFlood(unittest.TestCase):
    def test_add_sheet(self):
        smart_excel = SmartExcel(
            definition=FBF_DEFINITION,
            data=FbfFloodData(
                flood_event_id=43
            )
        )

        smart_excel.dump()

from collections import namedtuple
class TestPlPy(unittest.TestCase):
    def setUp(self):

        def_pl_res = namedtuple('PLyResult', 'status, nrows, rows, progress')
        self.pl_res = def_pl_res(
            status=5,
            nrows=1,
            rows=[
                {
                    'id': 15,
                    'flood_map_id': 15,
                    'acquisition_date': '2019-11-30'
                }
            ],
            progress=None
        )

    def runTest(self):
        fields = list(self.pl_res.rows[0].keys())
        def_meta_res = namedtuple('Result', ', '.join(fields))

        final_result = [
            def_meta_res(*list(row.values()))
            for row in self.pl_res.rows
        ]
        import pdb; pdb.set_trace()

if __name__ == "__main__":
    unittest.main()