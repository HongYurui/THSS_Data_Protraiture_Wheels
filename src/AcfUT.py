import unittest
from FlokAlgorithmLocal import FlokDataFrame, FlokAlgorithmLocal
from SelectTimeseries import SelectTimeseries
from Acf import Acf
import os
class AcfUT(unittest.TestCase):

    def setUp(self):
        path = os.path.abspath('.')
        path +='\data\\root_test_d2'
        input_paths = [path]  # use a large dataset
        input_types = ["csv"]
        input_location = ["local_fs"]
        output_paths = ["root_test_d1_out.csv"]
        output_types = ["csv"]
        self.orig_dataset = FlokAlgorithmLocal().read(input_paths, input_types, input_location, output_paths, output_types)
        self.algorithm = Acf()

    def test_acf_1(self):
        self.timeseries = {"timeseries": "Time,s1"}
        self.serieslength = 5
        self.params = {}
    def test_acf_2(self):
        self.timeseries = {"timeseries": "Time,s16"}
        self.serieslength = 2500
        self.params = {}

    def tearDown(self):
        dataset = FlokDataFrame()
        dataset.addDF(SelectTimeseries().run(self.orig_dataset, self.timeseries).get(0).iloc[:self.serieslength])
        result = self.algorithm.run(dataset, self.params)
        print(result.get(0))


if __name__ == "__main__":
    unittest.main()
