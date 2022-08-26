import unittest
from FlokAlgorithmLocal import FlokDataFrame, FlokAlgorithmLocal
from SelectTimeseries import SelectTimeseries
from Percentile import Percentile

class PercentileUT(unittest.TestCase):
    def setUp(self):
        input_paths = ["root_test_zmy"]
        input_types = ["csv"]
        input_location = ["local_fs"]
        output_paths = ["root_test_zmy_out.csv"]
        output_types = ["csv"]
        self.orif_dataset = FlokAlgorithmLocal().read(input_paths, input_types, input_location, output_paths, output_types)
        self.algorithm = Percentile()

    def test_percentile_1(self):
        self.timeseries = {"timeseries": "Time,s1"}
        self.params = {}

    def test_percentile_2(self):
        self.timeseries = {"timeseries": "Time,s1"}
        self.params = {"rank" : 0.75, "error" : 0.03}

    def test_percentile_3(self):
        self.timeseries = {"timeseries": "Time,s2"}
        self.params = {"rank" : 0.25}

    def test_percentile_4(self):
        input_paths = ["root_test_d1"]
        input_types = ["csv"]
        input_location = ["local_fs"]
        output_paths = ["root_test_zmy_out.csv"]
        output_types = ["csv"]
        self.orif_dataset = FlokAlgorithmLocal().read(input_paths, input_types, input_location, output_paths, output_types)
        self.algorithm = Percentile()
        self.timeseries = {"timeseries": "Time,s11"}
        self.params = { "rank": 0.2 , "error": 0.01}

    def tearDown(self):
        dataset = SelectTimeseries().run(self.orif_dataset, self.timeseries)
        result = self.algorithm.run(dataset, self.params)
        print(result.get(0))


if __name__ == "__main__":
    unittest.main()
