import unittest
from FlokAlgorithmLocal import FlokDataFrame, FlokAlgorithmLocal
from SelectTimeseries import SelectTimeseries
from Mad import Mad


class MadUT(unittest.TestCase):

    def setUp(self):
        input_paths = ["../data/root_test_d1"]
        input_types = ["csv"]
        input_location = ["local_fs"]
        output_paths = ["../data/root_test_d1_out.csv"]
        output_types = ["csv"]
        self.orig_dataset = FlokAlgorithmLocal().read(input_paths, input_types, input_location, output_paths, output_types)
        self.algorithm = Mad()

    def test_mad_1(self):
        self.timeseries = {"timeseries": "Time,s5"}
        self.serieslength = 26
        self.params = {"error": "0.01"}

    def test_mad_2(self):
        self.timeseries = {"timeseries": "Time,s5"}
        self.serieslength = 26
        self.params = {}

    def tearDown(self):
        dataset = FlokDataFrame()
        dataset.addDF(SelectTimeseries().run(self.orig_dataset, self.timeseries).get(0).iloc[:self.serieslength])
        result = self.algorithm.run(dataset, self.params)
        print(result.get(0))


if __name__ == "__main__":
    unittest.main()
