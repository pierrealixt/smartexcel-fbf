import unittest

from .smart_excel import SmartExcel
from .fbf.data_model import FbfFloodData
from .fbf.definition import FBF_DEFINITION


class TestFlood(unittest.TestCase):
    def runTest(self):
        smart_excel = SmartExcel(
            output='test_fbf.xlsx',
            definition=FBF_DEFINITION,
            data=FbfFloodData(
                flood_event_id=15
            )
        )

        smart_excel.dump()

if __name__ == "__main__":
    unittest.main()
