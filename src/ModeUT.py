from math import nan
import unittest
from FlokAlgorithmLocal import FlokDataFrame, FlokAlgorithmLocal
from SelectTimeseries import SelectTimeseries
from Mode import Mode

class ModeUT(unittest.TestCase):
    def setUp(self):
        input_paths = ["../data/root_test_zmy"]
        input_types = ["csv"]
        input_location = ["local_fs"]
        output_paths = ["../data/root_test_zmy_out.csv"]
        output_types = ["csv"]
        self.orif_dataset = FlokAlgorithmLocal().read(input_paths, input_types, input_location, output_paths, output_types)
        self.algorithm = Mode()

    def test_mode_1(self):
        self.timeseries = {"timeseries": "Time,s1"}
        self.params = {}

    def test_mode_2(self):
        self.timeseries = {"timeseries": "Time,s2"}
        self.params = {}

    def test_mode_3(self):
        self.timeseries = {"timeseries": "Time,s3"}
        self.params = {}

    def test_mode_4(self):
        input_paths = ["../data/root_test_d1"]
        input_types = ["csv"]
        input_location = ["local_fs"]
        output_paths = ["../data/root_test_zmy_out.csv"]
        output_types = ["csv"]
        self.orif_dataset = FlokAlgorithmLocal().read(input_paths, input_types, input_location, output_paths, output_types)
        self.algorithm = Mode()
        self.timeseries = {"timeseries": "Time,s8"}
        self.params = {}

    def tearDown(self):
        dataset = SelectTimeseries().run(self.orif_dataset, self.timeseries)
        result = self.algorithm.run(dataset, self.params)
        print(result.get(0))

if __name__ == "__main__":
    unittest.main()
