from importlib import import_module
from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame
import pandas as pd
from datetime import datetime


class Histogram(FlokAlgorithmLocal):
    def run(self, inputDataSets, params):
        input_data = inputDataSets.get(0)
        output_data = input_data
        column = input_data.columns[1]
        max_value = max(output_data[column])
        min = params.get("min", -max_value)
        max_ = params.get("max", max_value)
        count = params.get("count", 1)
        if isinstance(min, str):
            min = float(min)
        if isinstance(max_, str):
            max_ = float(max_)
        if isinstance(count, str):
            count = int(count)
        bucket = [0]*count
        Time = []
        for j in range(len(output_data[column])):
            if output_data[column][j] < min:
                bucket[0] += 1
            elif output_data[column][j] >= max_:
                bucket[-1] += 1
            else:
                for i in range(1, count+1):
                    if (output_data[column][j] >= min+(i-1)*(max_-min)/count
                            and output_data[column][j] < min+i*(max_-min)/count):
                        bucket[i-1] += 1
        for i in range(count):
            Time.append(datetime.fromtimestamp((i+1)/1000.0))
        Time = pd.Series([t.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                         for t in Time])
        j = 'histogram({},\'min\'=\'{}\',\'max\'=\'{}\',\'count\'=\'{}\')'.format(
            column, min, max_, count)
        data = {'Time': Time, j: bucket}
        output_data = pd.DataFrame(data)
        result = FlokDataFrame()
        result.addDF(output_data)
        return result


if __name__ == "__main__":
    algorithm = Histogram()

    all_info_1 = {
        "input": ["./test_in.csv"],
        "inputFormat": ["csv"],
        "inputLocation": ["local_fs"],
        "output": ["./test_out_1.csv"],
        "outputFormat": ["csv"],
        "outputLocation": ["local_fs"],
        "parameters": {"min": 1, "max": 20.1, "count": 10}
    }

    params = all_info_1["parameters"]
    inputPaths = all_info_1["input"]
    inputTypes = all_info_1["inputFormat"]
    inputLocation = all_info_1["inputLocation"]
    outputPaths = all_info_1["output"]
    outputTypes = all_info_1["outputFormat"]
    outputLocation = all_info_1["outputLocation"]

    dataSet = algorithm.read(inputPaths, inputTypes,
                             inputLocation, outputPaths, outputTypes)
    from SelectTimeseries import SelectTimeseries
    dataSet = SelectTimeseries().run(
        dataSet, {"timeseries": "Time,root.test.d2.s2"})
    result = algorithm.run(dataSet, params)
    algorithm.write(outputPaths, result, outputTypes, outputLocation)
'''
    all_info_2 = {
        "input": ["./test_in.csv"],
        "inputFormat": ["csv"],
        "inputLocation": ["local_fs"],
        "output": ["./test_out_2.csv"],
        "outputFormat": ["csv"],
        "outputLocation": ["local_fs"],
        "parameters": {"timeseries": "Time,root.test.d2.s2","min":1,"max_":20,"count":10}
    }

    params = all_info_2["parameters"]
    inputPaths = all_info_2["input"]
    inputTypes = all_info_2["inputFormat"]
    inputLocation = all_info_2["inputLocation"]
    outputPaths = all_info_2["output"]
    outputTypes = all_info_2["outputFormat"]
    outputLocation = all_info_2["outputLocation"]

    dataSet = algorithm.read(inputPaths, inputTypes,
                             inputLocation, outputPaths, outputTypes)
    result = algorithm.run(dataSet, params)
    algorithm.write(outputPaths, result, outputTypes, outputLocation)
'''
