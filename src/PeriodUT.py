from math import nan
import unittest
from FlokAlgorithmLocal import FlokDataFrame, FlokAlgorithmLocal
from SelectTimeseries import SelectTimeseries
from Period import Period

class PeriodUT(unittest.TestCase):
    def setUp(self):
        input_paths = ["root_test_zmy"]
        input_types = ["csv"]
        input_location = ["local_fs"]
        output_paths = ["root_test_zmy_out.csv"]
        output_types = ["csv"]
        self.orif_dataset = FlokAlgorithmLocal().read(input_paths, input_types, input_location, output_paths, output_types)
        self.algorithm = Period()

    def test_period_1(self):
        self.timeseries = {"timeseries": "Time,s4"}
        self.params = {}

    def test_period_2(self):
        self.timeseries = {"timeseries": "Time,s5"}
        self.params = {}
    
    def test_period_3(self):
        self.timeseries = {"timeseries": "Time,s7"}
        self.params = {}

    def test_period_4(self):
        input_paths = ["root_test_d1"]
        input_types = ["csv"]
        input_location = ["local_fs"]
        output_paths = ["root_test_zmy_out.csv"]
        output_types = ["csv"]
        self.orif_dataset = FlokAlgorithmLocal().read(input_paths, input_types, input_location, output_paths, output_types)
        self.algorithm = Period()
        self.timeseries = {"timeseries": "Time,s12"}
        self.params = {}
        dataset = FlokDataFrame()
        dataset.addDF(SelectTimeseries().run(self.orif_dataset, self.timeseries).get(0).iloc[:9])
        result = self.algorithm.run(dataset, self.params)
        print(result.get(0))


    def tearDown(self):
        dataset = SelectTimeseries().run(self.orif_dataset, self.timeseries)
        result = self.algorithm.run(dataset, self.params)
        print(result.get(0))


if __name__ == "__main__":
    unittest.main()
