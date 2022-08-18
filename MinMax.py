from datetime import datetime
import pandas as pd
from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame

class MINMAX(FlokAlgorithmLocal):
    def run(self, inputDataSets, params, compute="batch", min=0, max=1):
        input_data = inputDataSets.get(0)
        output_data = input_data.copy()
        
        for column in range(1, input_data.shape[1]):
            MAX = input_data.iloc[:, column].max()
            MIN = input_data.iloc[:, column].min()
            for i in range(0, input_data.shape[0]):
                if compute == "stream":
                    output_data.iloc[i, column] = (input_data.iloc[i, column] - MIN)/(MAX - MIN)*(max - min) + min
                else:
                    output_data.iloc[i, column] = (input_data.iloc[i, column] - MIN)/(MAX - MIN)

        result = FlokDataFrame()
        result.addDF(output_data)
        return result
        
if __name__ == "__main__":
    algorithm = MINMAX()

    all_info_1 = {
        "input": ["./test_in.csv"],
        "inputFormat": ["csv"],
        "inputLocation": ["local_fs"],
        "output": ["./test_out_1.csv"],
        "outputFormat": ["csv"],
        "outputLocation": ["local_fs"],
        "parameters": {"unit": "1S"}
    }

    params = all_info_1["parameters"]
    inputPaths = all_info_1["input"]
    inputTypes = all_info_1["inputFormat"]
    inputLocation = all_info_1["inputLocation"]
    outputPaths = all_info_1["output"]
    outputTypes = all_info_1["outputFormat"]
    outputLocation = all_info_1["outputLocation"]

    dataSet = algorithm.read(inputPaths, inputTypes, inputLocation, outputPaths, outputTypes)
    result = algorithm.run(dataSet, params)
    algorithm.write(outputPaths, result, outputTypes, outputLocation)

    all_info_2 = {
        "input": ["./test_in.csv"],
        "inputFormat": ["csv"],
        "inputLocation": ["local_fs"],
        "output": ["./test_out_2.csv"],
        "outputFormat": ["csv"],
        "outputLocation": ["local_fs"],
        "parameters": {"timeseries": "Time,root.test.d2.s2"}
    }

    params = all_info_2["parameters"]
    inputPaths = all_info_2["input"]
    inputTypes = all_info_2["inputFormat"]
    inputLocation = all_info_2["inputLocation"]
    outputPaths = all_info_2["output"]
    outputTypes = all_info_2["outputFormat"]
    outputLocation = all_info_2["outputLocation"]

    dataSet = algorithm.read(inputPaths, inputTypes, inputLocation, outputPaths, outputTypes)
    result = algorithm.run(dataSet, params)
    algorithm.write(outputPaths, result, outputTypes, outputLocation)