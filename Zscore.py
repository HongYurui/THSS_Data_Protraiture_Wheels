from datetime import date, datetime
from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame
import math
import pandas as pd
from datetime import datetime
class Zscore(FlokAlgorithmLocal):
    def run(self, inputDataSets, params):
        input_data = inputDataSets.get(0)
        output_data = input_data
        column = input_data.columns[1]
        compute = params.get('compute', 'batch')
        Time=[]
        for i in range(len(output_data)):
            Time.append(datetime.fromtimestamp((i+1)/1000))
        if compute == 'stream':
            avg = params.get("avg", 0)
            std = params.get("std", 1)
            output_data[column] = (output_data[column]-avg)/std
            j = 'Zscore({},\'avg\'=\'{}\',\'std\'=\'{}\')'.format(
                column, avg, std)
            data = {'Time': Time, j: output_data[column]}
            output_data = pd.DataFrame(data)
        else:
            mean = sum(output_data[column])/len(output_data[column])
            std = math.sqrt(
                sum((output_data[column]-mean) ** 2)/len(output_data[column]))
            output_data[column] = (output_data[column]-mean)/std
            j = 'Zscore('+str(column)+')'
            data = {'Time': Time, j: output_data[column]}
            output_data = pd.DataFrame(data)

        result = FlokDataFrame()
        result.addDF(output_data)
        return result


if __name__ == "__main__":
    algorithm = Zscore()

    all_info_1 = {
        "input": ["./test_in.csv"],
        "inputFormat": ["csv"],
        "inputLocation": ["local_fs"],
        "output": ["./test_out_1.csv"],
        "outputFormat": ["csv"],
        "outputLocation": ["local_fs"],
        "parameters": {"compute": "batch"}
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
        "parameters": {"compute":"stream","avg":1,"std":1}
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
    from SelectTimeseries import SelectTimeseries
    dataSet = SelectTimeseries().run(dataSet, {"timeseries": "Time,root.test.d2.s2"})
    result = algorithm.run(dataSet, params)
    algorithm.write(outputPaths, result, outputTypes, outputLocation)
'''
