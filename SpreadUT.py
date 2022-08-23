import unittest
from FlokAlgorithmLocal import FlokDataFrame, FlokAlgorithmLocal
from SelectTimeseries import SelectTimeseries
from Spread import Spread


class SpreadUT(unittest.TestCase):

    def setUp(self):
        input_paths = ["root_test_d1"]
        input_types = ["csv"]
        input_location = ["local_fs"]
        output_paths = ["root_test_d1_out.csv"]
        output_types = ["csv"]
        self.orig_dataset = FlokAlgorithmLocal().read(
            input_paths, input_types, input_location, output_paths, output_types)
        self.algorithm = Spread()

    def test_spread_1(self):
        self.timeseries = {"timeseries": "Time,s1"}
        self.params = {}

    def test_spread_2(self):
        self.timeseries = {"timeseries": "Time,s2"}
        self.params = {}

    def tearDown(self):
        dataset = SelectTimeseries().run(self.orig_dataset, self.timeseries)
        result = self.algorithm.run(dataset, self.params)
        print(result.get(0))


if __name__ == "__main__":
    unittest.main()
