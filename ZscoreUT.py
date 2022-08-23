import unittest
from FlokAlgorithmLocal import FlokDataFrame, FlokAlgorithmLocal
from SelectTimeseries import SelectTimeseries
from Zscore import Zscore


class ZscoreUT(unittest.TestCase):

    def setUp(self):
        input_paths = ["root_test_d1"]
        input_types = ["csv"]
        input_location = ["local_fs"]
        output_paths = ["root_test_d1_out.csv"]
        output_types = ["csv"]
        self.orif_dataset = FlokAlgorithmLocal().read(
            input_paths, input_types, input_location, output_paths, output_types)
        self.algorithm = Zscore()

    def test_zscore_1(self):
        self.timeseries = {"timeseries": "Time,s1"}
        self.params = {}

    def test_zscore_2(self):
        self.timeseries = {"timeseries": "Time,s2"}
        self.params = {"compute": "stream", "avg": 1, "std": 1}

    def tearDown(self):
        dataset = SelectTimeseries().run(self.orif_dataset, self.timeseries)
        result = self.algorithm.run(dataset, self.params)
        print(result.get(0))


if __name__ == "__main__":
    unittest.main()
