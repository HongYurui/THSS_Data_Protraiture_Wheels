import unittest
import pandas as pd
from FlokAlgorithmLocal import FlokDataFrame, FlokAlgorithmLocal
from SelectTimeseries import SelectTimeseries
from Integral import Integral


class IntegralUT(unittest.TestCase):

    def setUp(self):
        input_paths = ["../data/root_test_d1"]
        input_types = ["csv"]
        input_location = ["local_fs"]
        output_paths = ["../data/root_test_d1_out.csv"]
        output_types = ["csv"]
        self.orig_dataset = FlokAlgorithmLocal().read(input_paths, input_types, input_location, output_paths, output_types)
        self.algorithm = Integral()

    def test_integral_1(self):
        self.timeseries = {"timeseries": "Time,s4"}
        self.serieslength = 8
        self.params = {"unit": "1m"}

    def test_integral_2(self):
        self.timeseries = {"timeseries": "Time,s4"}
        self.serieslength = 8
        self.params = {}

    def tearDown(self):
        dataset = FlokDataFrame()
        data = SelectTimeseries().run(self.orig_dataset, self.timeseries).get(0).iloc[:self.serieslength]
        # timestamp not identical but vital, reset required
        for i in [5 ,6, 7]:
            data.iloc[i, 0]  = pd.to_datetime(data.iloc[i, 0]) + pd.Timedelta(seconds=2)
        dataset.addDF(data)
        result = self.algorithm.run(dataset, self.params)
        print(result.get(0))


if __name__ == "__main__":
    unittest.main()
