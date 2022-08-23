import pandas as pd
from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame
from statsmodels.tsa.stattools import acf
from scipy.stats import chi2

class Qlb(FlokAlgorithmLocal):
    def run(self, inputDataSets, params):
        input_data = inputDataSets.get(0)
        time_data = pd.Series([pd.to_datetime(data, format="%Y-%m-%d %H:%M:%S") for data in input_data.iloc[:, 0].values])
        value_data = input_data.iloc[:, 1].astype(float)
        n = len(time_data)

        # get lag
        lag = params.get("lag", n - 2)
        if isinstance(lag, str):
            lag = int(lag)

        # header format
        value_header = 'qlb(' + input_data.columns[1]
        param_list = ['lag']
        for param in param_list:
            if param in params:
                value_header += ', \'' + param + '\'=\'' + str(params[param]) + '\''
        value_header += ')'

        # time format
        output_data = pd.DataFrame(index=range(lag), columns=['Time', value_header])
        timestamp = pd.to_datetime("1970-01-01 08:00:00", format="%Y-%m-%d %H:%M:%S")
        timedelta = pd.to_timedelta(0.001, unit="s")

        # calculate square acf
        # acf_data = Acf().run(inputDataSets, {}).get(0).iloc[:, 1].values
        # acf_data /= max(acf_data)
        # print(acf_data)
        acf_data = acf(value_data)[1:]
        square_acf = [x ** 2 / (n - i - 1) for i, x in enumerate(acf_data)]

        for i in range(lag):
            timestamp += timedelta
            output_data.iloc[i, 0] = timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            # LB Q-test
            output_data.iloc[i, 1] = 1 - chi2.cdf(n * (n + 2) * sum(square_acf[:(i + 1)]), i + 1)

        result = FlokDataFrame()
        result.addDF(output_data)
        return result

if __name__ == "__main__":
    algorithm = Qlb()

    all_info_1 = {
        "input": ["root_test_d1"],
        "inputFormat": ["csv"],
        "inputLocation": ["local_fs"],
        "output": ["./test_out_1.csv"],
        "outputFormat": ["csv"],
        "outputLocation": ["local_fs"],
        "parameters": {'lag': 18}
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
    dataSet = SelectTimeseries().run(dataSet, {"timeseries": "Time,s13"})
    tmp = FlokDataFrame()
    tmp.addDF(dataSet.get(0).iloc[:20, :])
    dataSet = tmp
    result = algorithm.run(dataSet, params)
    # algorithm.write(outputPaths, result, outputTypes, outputLocation)
    print(result.get(0))

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