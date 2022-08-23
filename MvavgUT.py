from math import nan
import unittest
from FlokAlgorithmLocal import FlokDataFrame, FlokAlgorithmLocal
from SelectTimeseries import SelectTimeseries
from Mvavg import Mvavg

class MvavgUT(unittest.TestCase):
    def setUp(self):
        input_paths = ["root_test_zmy"]
        input_types = ["csv"]
        input_location = ["local_fs"]
        output_paths = ["root_test_zmy_out.csv"]
        output_types = ["csv"]
        self.orif_dataset = FlokAlgorithmLocal().read(input_paths, input_types, input_location, output_paths, output_types)
        self.algorithm = Mvavg()

    def test_mvavg_1(self):
        self.timeseries = {"timeseries": "Time,s1"}
        self.params = {}

    def test_mvavg_2(self):
        self.timeseries = {"timeseries": "Time,s1"}
        self.params = {"window": 4}

    def test_mvavg_3(self):
        self.timeseries = {"timeseries": "Time,s2"}
        self.params = {"window": 8}
    
    def test_mvavg_4(self):
        input_paths = ["root_test_d1"]
        input_types = ["csv"]
        input_location = ["local_fs"]
        output_paths = ["root_test_zmy_out.csv"]
        output_types = ["csv"]
        self.orif_dataset = FlokAlgorithmLocal().read(input_paths, input_types, input_location, output_paths, output_types)
        self.algorithm = Mvavg()
        self.timeseries = {"timeseries": "Time,s9"}
        self.params = {"window": 3}

    def tearDown(self):
        dataset = SelectTimeseries().run(self.orif_dataset, self.timeseries)
        result = self.algorithm.run(dataset, self.params)
        print(result.get(0))
        pass


if __name__ == "__main__":
    unittest.main()
