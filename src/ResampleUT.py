import unittest
import pandas as pd
from FlokAlgorithmLocal import FlokDataFrame, FlokAlgorithmLocal
from SelectTimeseries import SelectTimeseries
from Resample import Resample


class ResampleUT(unittest.TestCase):

    def setUp(self):
        input_paths = ["../data/root_test_d1"]
        input_types = ["csv"]
        input_location = ["local_fs"]
        output_paths = ["../data/root_test_d1_out.csv"]
        output_types = ["csv"]
        self.orig_dataset = FlokAlgorithmLocal().read(input_paths, input_types, input_location, output_paths, output_types)
        self.algorithm = Resample()

    def test_resample_1(self):
        self.timeseries = {"timeseries": "Time,s14"}
        self.serieslength = 5
        self.params = {"every": "5m", "interp": "linear"}

    def test_resample_2(self):
        self.timeseries = {"timeseries": "Time,s14"}
        self.serieslength = 5
        self.params = {"every": "30m", "aggr": "first"}

    def test_resample_3(self):
        self.timeseries = {"timeseries": "Time,s14"}
        self.serieslength = 5
        self.params = {"every": "30m", "start": "2021-03-06 15:00:00"}

    def tearDown(self):
        dataset = FlokDataFrame()
        data = SelectTimeseries().run(self.orig_dataset, self.timeseries).get(0).iloc[:self.serieslength]
        # timestamp not identical but vital, reset required
        data.iloc[0, 0] = pd.to_datetime("2021-03-06 16:00:00", format="%Y-%m-%d %H:%M:%S")
        for i in range(1, self.serieslength):
            data.iloc[i, 0]  = data.iloc[i - 1, 0] + pd.Timedelta(minutes=15)
        dataset.addDF(data)
        result = self.algorithm.run(dataset, self.params)
        print(result.get(0))


if __name__ == "__main__":
    unittest.main()
