import unittest
from FlokAlgorithmLocal import FlokDataFrame, FlokAlgorithmLocal
from SelectTimeseries import SelectTimeseries
from Spread import Spread
import os

class SpreadUT(unittest.TestCase):

    def setUp(self):
        path = os.path.abspath('.')
        path += '\data\\root_test_d2'
        input_paths = [path]
        input_types = ["csv"]
        input_location = ["local_fs"]
        output_paths = ["root_test_d1_out.csv"]
        output_types = ["csv"]
        self.orig_dataset = FlokAlgorithmLocal().read(
            input_paths, input_types, input_location, output_paths, output_types)
        self.algorithm = Spread()

    def test_spread_1(self):
        self.timeseries = {"timeseries": "Time,s19"}
        self.serieslength = 14
        self.params = {}

    def test_spread_2(self):
        self.timeseries = {"timeseries": "Time,s19"}
        self.serieslength = 10000
        self.params = {}

    def tearDown(self):
        dataset = FlokDataFrame()
        dataset.addDF(SelectTimeseries().run(self.orig_dataset, self.timeseries).get(0).iloc[:self.serieslength])
        result = self.algorithm.run(dataset, self.params)
        print(result.get(0))


if __name__ == "__main__":
    unittest.main()
