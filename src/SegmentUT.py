import unittest
from FlokAlgorithmLocal import FlokDataFrame, FlokAlgorithmLocal
from SelectTimeseries import SelectTimeseries
from Segment import Segment

class SegmentUT(unittest.TestCase):

    def setUp(self):
        input_paths = ["../data/root_test_d2"]  # use a large dataset
        input_types = ["csv"]
        input_location = ["local_fs"]
        output_paths = ["../data/root_test_d2_out.csv"]
        output_types = ["csv"]
        self.orig_dataset = FlokAlgorithmLocal().read(
            input_paths, input_types, input_location, output_paths, output_types)
        self.algorithm = Segment()

    def test_segment_1(self):
        self.timeseries = {"timeseries": "Time,s16"}
        self.serieslength = 40
        self.params = {'error': "0.1"}

    def test_segment_2(self):

        self.timeseries = {"timeseries": "Time,s16"}
        self.serieslength = 2500
        self.params = {'output': 'all', 'error': "1"}

    def tearDown(self):
        dataset = FlokDataFrame()
        dataset.addDF(SelectTimeseries().run(self.orig_dataset,
                      self.timeseries).get(0).iloc[:self.serieslength])
        result = self.algorithm.run(dataset, self.params)
        print(result.get(0))


if __name__ == "__main__":
    unittest.main()
