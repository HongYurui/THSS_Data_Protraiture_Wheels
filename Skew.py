from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame
import math
import pandas as pd


class Skew(FlokAlgorithmLocal):
    def run(self, inputDataSets, params):
        input_data = inputDataSets.get(0)
        output_data = input_data
        column = input_data.columns[1]
        output_data.dropna(inplace=True)
        mean = sum(output_data[column])/len(output_data[column])
        std = math.sqrt(sum((output_data[column]-mean) **
                        2)/len(output_data[column]))
        skew = sum(((output_data[column]-mean)/std)** 3)/len(output_data[column])
        # j = 'skew({})'.format(column)
        # data = {'Time': '1970-01-01 08:00:00.000', j: skew}
        # output_data = pd.DataFrame(data, index=[0])
        output_data = pd.DataFrame([['1970-01-01 08:00:00.000', skew]], index=[0], columns=['Time', 'skew(s1)'])

        result = FlokDataFrame()
        result.addDF(output_data)
        return result


if __name__ == "__main__":
    algorithm = Skew()

    all_info_1 = {
        "input": ["root_test_d1"],
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

    dataSet = algorithm.read(inputPaths, inputTypes,
                             inputLocation, outputPaths, outputTypes)
    from SelectTimeseries import SelectTimeseries
    dataSet = SelectTimeseries().run(
        dataSet, {"timeseries": "Time,s2"})
    result = algorithm.run(dataSet, params)
    algorithm.write(outputPaths, result, outputTypes, outputLocation)

    # all_info_2 = {
    #     "input": ["./test_in.csv"],
    #     "inputFormat": ["csv"],
    #     "inputLocation": ["local_fs"],
    #     "output": ["./test_out_2.csv"],
    #     "outputFormat": ["csv"],
    #     "outputLocation": ["local_fs"],
    #     "parameters": {}
    # }

    # params = all_info_2["parameters"]
    # inputPaths = all_info_2["input"]
    # inputTypes = all_info_2["inputFormat"]
    # inputLocation = all_info_2["inputLocation"]
    # outputPaths = all_info_2["output"]
    # outputTypes = all_info_2["outputFormat"]
    # outputLocation = all_info_2["outputLocation"]

    # dataSet = algorithm.read(inputPaths, inputTypes,
    #                          inputLocation, outputPaths, outputTypes)
    # from SelectTimeseries import SelectTimeseries
    # dataSet = SelectTimeseries().run(
    #     dataSet, {"timeseries": "Time,root.test.d2.s2"})
    # result = algorithm.run(dataSet, params)
    # algorithm.write(outputPaths, result, outputTypes, outputLocation)
