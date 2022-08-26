import unittest
from FlokAlgorithmLocal import FlokDataFrame, FlokAlgorithmLocal
from SelectTimeseries import SelectTimeseries
from Minmax import Minmax

class MinmaxUT(unittest.TestCase):
    def setUp(self):
        input_paths = ["../data/root_test_zmy"]
        input_types = ["csv"]
        input_location = ["local_fs"]
        output_paths = ["../data/root_test_zmy_out.csv"]
        output_types = ["csv"]
        self.orif_dataset = FlokAlgorithmLocal().read(input_paths, input_types, input_location, output_paths, output_types)
        self.algorithm = Minmax()

    def test_minmax_1(self):
        self.timeseries = {"timeseries": "Time,s1"}
        self.params = {}

    def test_minmax_2(self):
        self.timeseries = {"timeseries": "Time,s1"}
        self.params = {"compute": "batch", "min": 0, "max": 10}

    def test_minmax_3(self):
        self.timeseries = {"timeseries": "Time,s2"}
        self.params = {"compute": "stream", "min": 1, "max": 10}

    def test_minmax_4(self):
        self.timeseries = {"timeseries": "Time,s2"}
        self.params = {"compute": "stream", "min": 1, "max": -1}

    def test_minmax_5(self):
        input_paths = ["../data/root_test_d1"]
        input_types = ["csv"]
        input_location = ["local_fs"]
        output_paths = ["../data/root_test_zmy_out.csv"]
        output_types = ["csv"]
        self.orif_dataset = FlokAlgorithmLocal().read(input_paths, input_types, input_location, output_paths, output_types)
        self.algorithm = Minmax()
        self.timeseries = {"timeseries": "Time,s7"}
        self.params = {}

    def tearDown(self):
        dataset = SelectTimeseries().run(self.orif_dataset, self.timeseries)
        result = self.algorithm.run(dataset, self.params)
        print(result.get(0))
        pass


if __name__ == "__main__":
    unittest.main()
