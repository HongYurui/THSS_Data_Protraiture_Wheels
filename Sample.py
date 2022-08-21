import pandas as pd
import random
from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame

class Sample(FlokAlgorithmLocal):
    def run(self, inputDataSets, params):
        input_data = inputDataSets.get(0)

        # get parameters
        method = params.get("method", "reservoir")
        k = params.get("k", 1)
        if isinstance(k, str):
            k = int(k)

        # header format
        value_header = 'sample(' + input_data.columns[1]
        param_list = ['method', 'k']
        for param in param_list:
            if param in params:
                value_header += ', \'' + param + '\'=\'' + str(params[param]) + '\''
        value_header += ')'

        output_data = pd.DataFrame(index=range(k), columns=['Time', value_header])

        # reservoir sampling
        if method == "reservoir":
            for i in range(len(input_data)):
                if i < k:
                    output_data.iloc[i] = input_data.iloc[i]
                else:
                    random_int = random.randint(0, i)
                    if random_int < k:
                        output_data.iloc[random_int] = input_data.iloc[i]
        # isometric sampling
        elif method == "isometric":
            step = int(len(input_data) / k)
            for i in range(k):
                output_data.iloc[i] = input_data.iloc[i * step]
        else:
            raise Exception("Invalid parameter 'method'")

        result = FlokDataFrame()
        result.addDF(output_data)
        return result

if __name__ == "__main__":
    algorithm = Sample()

    all_info_1 = {
        "input": ["./test_in.csv"],
        "inputFormat": ["csv"],
        "inputLocation": ["local_fs"],
        "output": ["./test_out_1.csv"],
        "outputFormat": ["csv"],
        "outputLocation": ["local_fs"],
        "parameters": {"method": "reservoir", "k": 5}
    }

    params = all_info_1["parameters"]
    inputPaths = all_info_1["input"]
    inputTypes = all_info_1["inputFormat"]
    inputLocation = all_info_1["inputLocation"]
    outputPaths = all_info_1["output"]
    outputTypes = all_info_1["outputFormat"]
    outputLocation = all_info_1["outputLocation"]

    dataSet = algorithm.read(inputPaths, inputTypes, inputLocation, outputPaths, outputTypes)
    from SelectTimeseries import SelectTimeseries
    dataSet = SelectTimeseries().run(dataSet, {"timeseries": "Time,root.test.d2.s2"})
    result = algorithm.run(dataSet, params)
    algorithm.write(outputPaths, result, outputTypes, outputLocation)

    # all_info_2 = {
    #     "input": ["./test_in.csv"],
    #     "inputFormat": ["csv"],
    #     "inputLocation": ["local_fs"],
    #     "output": ["./test_out_2.csv"],
    #     "outputFormat": ["csv"],
    #     "outputLocation": ["local_fs"],
    #     "parameters": {"timeseries": "Time,root.test.d2.s2"}
    # }

    # params = all_info_2["parameters"]
    # inputPaths = all_info_2["input"]
    # inputTypes = all_info_2["inputFormat"]
    # inputLocation = all_info_2["inputLocation"]
    # outputPaths = all_info_2["output"]
    # outputTypes = all_info_2["outputFormat"]
    # outputLocation = all_info_2["outputLocation"]

    # dataSet = algorithm.read(inputPaths, inputTypes, inputLocation, outputPaths, outputTypes)
    # result = algorithm.run(dataSet, params)
    # algorithm.write(outputPaths, result, outputTypes, outputLocation)