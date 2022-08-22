import unittest
import select

from SelectTimeseries import SelectTimeseries
from Acf import Acf
from Distinct import Distinct
from Histogram import Histogram


class SelectTimeseriesUT(unittest.TestCase):

    def setUp(self):
        inputPaths = ["root_test_d1"]
        inputTypes = ["csv"]
        inputLocation = ["local_fs"]
        outputPaths = ["root_test_d1_out.csv"]
        outputTypes = ["csv"]
        outputLocation = ["local_fs"]

    def test_SelectTimeseries_1(self):
        pass

    def test_SelectTimeseries_2(self):

        pass

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
