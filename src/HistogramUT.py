import unittest
from FlokAlgorithmLocal import FlokDataFrame, FlokAlgorithmLocal
from SelectTimeseries import SelectTimeseries
from Histogram import Histogram
import os

class HistogramUT(unittest.TestCase):

    def setUp(self):       
        path = os.path.abspath('.')
        path +='\data\\root_test_d2'
        input_paths = [path]  
        input_types = ["csv"]
        input_location = ["local_fs"]
        output_paths = ["root_test_d1_out.csv"]
        output_types = ["csv"]
        self.orig_dataset = FlokAlgorithmLocal().read(input_paths, input_types, input_location, output_paths, output_types)
        self.algorithm = Histogram()

    def test_histogram_1(self):
        self.timeseries = {"timeseries": "Time,s3"}
        self.serieslength = 20
        self.params = {"min": "1", "max": "20", "count": "10"}

    def test_histogram_2(self):
        self.timeseries = {"timeseries": "Time,s3"}
        self.serieslength = 2500
        self.params = {"min": "5", "count": "10"}

    def tearDown(self):
        dataset = FlokDataFrame()
        dataset.addDF(SelectTimeseries().run(self.orig_dataset, self.timeseries).get(0).iloc[:self.serieslength])
        result = self.algorithm.run(dataset, self.params)
        print(result.get(0))


if __name__ == "__main__":
    unittest.main()
