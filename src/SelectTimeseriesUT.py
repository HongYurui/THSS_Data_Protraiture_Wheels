import unittest
from FlokAlgorithmLocal import FlokDataFrame, FlokAlgorithmLocal
from SelectTimeseries import SelectTimeseries


class SelectTimeseriesUT(unittest.TestCase):
    def setUp(self):
        input_paths = ["../data/root_test_d1"]
        input_types = ["csv"]
        input_location = ["local_fs"]
        output_paths = ["../data/root_test_d1_out.csv"]
        output_types = ["csv"]
        self.orig_dataset = FlokAlgorithmLocal().read(input_paths, input_types, input_location, output_paths, output_types)
        self.algorithm = SelectTimeseries()

    def test_selecttimeseries_1(self):
        self.timeseries = {}
        self.serieslength = 40
        self.params = {"timeseries": "Time,s1"}

    def test_selecttimeseries_2(self):
        self.timeseries = {}
        self.serieslength = 40
        self.params = {"timeseries": "Time,s1,s3,s5"}

    def tearDown(self):
        dataset = FlokDataFrame()
        dataset.addDF(self.orig_dataset.get(0))
        result = self.algorithm.run(dataset, self.params)
        print(result.get(0))


if __name__ == "__main__":
    unittest.main()
