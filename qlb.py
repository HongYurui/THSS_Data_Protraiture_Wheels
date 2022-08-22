import pandas as pd
from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame
from ACF import acf

class Qlb(FlokAlgorithmLocal):
    def run(self, inputDataSets, params):
        input_data = inputDataSets.get(0)
        time_data = pd.Series([pd.to_datetime(data, format="%Y-%m-%d %H:%M:%S") for data in input_data.iloc[:, 0].values])
        value_data = input_data.iloc[:, 1].astype(float)
        n = len(time_data)

        # get lag
        lag = params.get("lag", n - 2)

        # header format
        value_header = 'qlb(' + input_data.columns[1]
        param_list = ['lag']
        for param in param_list:
            if param in params:
                value_header += ', \'' + param + '\'=\'' + str(params[param]) + '\''
        value_header += ')'

        # to be implemented
        output_data = pd.DataFrame(index=range(lag), columns=['Time', value_header])
        timestamp = time_data[0]
        timedelta = pd.to_timedelta(0.001, unit="s")
        print(acf().run(inputDataSets, {}).get(0).iloc[:-2, 1])
        square_acf = [x ** 2 / (n - i - 1) for i, x in enumerate(acf().run(inputDataSets, {}).get(0).iloc[:-2, 1])]
        # print(square_acf)
        
        for i in range(lag):
            timestamp += timedelta
            output_data.iloc[i, 0] = timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            # LB Q-test
            output_data.iloc[i, 1] = n * (n + 2) * sum(square_acf[:i + 1])
        print(output_data)
        result = FlokDataFrame()
        result.addDF(output_data)
        return result

if __name__ == "__main__":
    algorithm = Qlb()

    all_info_1 = {
        "input": ["./test_in copy.csv"],
        "inputFormat": ["csv"],
        "inputLocation": ["local_fs"],
        "output": ["./test_out_1.csv"],
        "outputFormat": ["csv"],
        "outputLocation": ["local_fs"],
        "parameters": {"lag": 18}
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
    #     "parameters": {}
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