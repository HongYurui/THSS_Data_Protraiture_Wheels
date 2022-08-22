import unittest
import select

from SelectTimeseries import SelectTimeseries
from Acf import Acf
from Distinct import Distinct
from Histogram import Histogram


class SelectTimeseriesUT(unittest.TestCase):

    def setUp(self):
        pass

    def test_SelectTimeseries_1(self):
        print('SelectTimeseries测试场景1')
        
        all_info_1 = {
            "input": ["./test_in.csv"],
            "inputFormat": ["csv"],
            "inputLocation": ["local_fs"],
            "output": ["./test_out_1.csv"],
            "outputFormat": ["csv"],
            "outputLocation": ["local_fs"],
            "parameters": {}
        }

        params = all_info_1["parameters"]
        inputPaths = all_info_1["input"]
        inputTypes = all_info_1["inputFormat"]
        inputLocation = all_info_1["inputLocation"]
        outputPaths = all_info_1["output"]
        outputTypes = all_info_1["outputFormat"]
        outputLocation = all_info_1["outputLocation"]
        #acf
        algorithm = Acf()
        all_info_1['output'] = ["./test_out_1_acf.csv"]
        params = all_info_1["parameters"]
        outputPaths = all_info_1["output"]
        #print(all_info_1)
        dataSet = algorithm.read(inputPaths, inputTypes,
                                inputLocation, outputPaths, outputTypes)
        dataSet = SelectTimeseries().run(
            dataSet, {"timeseries": "Time,root.test.d2.s2"})
        result = algorithm.run(dataSet, params)
        algorithm.write(outputPaths, result, outputTypes, outputLocation)
        #distinct
        algorithm = Distinct()
        all_info_1['output'] = ["./test_out_1_distinct.csv"]
        params = all_info_1["parameters"]
        outputPaths = all_info_1["output"]
        #print(all_info_1)
        dataSet = algorithm.read(inputPaths, inputTypes,
                                 inputLocation, outputPaths, outputTypes)
        dataSet = SelectTimeseries().run(
            dataSet, {"timeseries": "Time,root.test.d2.s2"})
        result = algorithm.run(dataSet, params)
        algorithm.write(outputPaths, result, outputTypes, outputLocation)
        #histogram
        algorithm = Histogram()
        all_info_1['output'] = ["./test_out_1_histogram.csv"]
        all_info_1['parameters'] = {"min": 1, "max_": 20, "count": 10}
        params = all_info_1["parameters"]
        outputPaths = all_info_1["output"]
        #print(all_info_1)
        dataSet = algorithm.read(inputPaths, inputTypes,
                                 inputLocation, outputPaths, outputTypes)
        dataSet = SelectTimeseries().run(
            dataSet, {"timeseries": "Time,root.test.d2.s2"})
        result = algorithm.run(dataSet, params)
        algorithm.write(outputPaths, result, outputTypes, outputLocation)
        pass

    def test_SelectTimeseries_2(self):
        print('SelectTimeseries测试场景2')
        pass

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
