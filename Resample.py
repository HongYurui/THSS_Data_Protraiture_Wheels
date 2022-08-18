import pandas as pd
from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame

class Resample(FlokAlgorithmLocal):
    def run(self, inputDataSets, params):
        input_data = inputDataSets.get(0)
        time_data = pd.Series([pd.to_datetime(data, format="%Y-%m-%d %H:%M:%S") for data in input_data.iloc[:, 0].values])
        value_data = input_data.iloc[:, 1].astype(float)
        
        # get parameters
        every = params.get("every")
        try:
            if every[-2:] == "ms":
                period = float(every[:-2])
                unit = "ms"
            else:
                period = float(every[:-1])
                unit = every[-1]
        except:
            raise Exception("Invalid parameter 'every'")
            
        interp = params.get("interp", "NaN")
        aggr = params.get("aggr", "Mean")
        left = next(time_data[i] for i in range(len(time_data)) if not pd.isnull(value_data[i]))
        right = next(time_data[i] for i in range(len(time_data)-1,-1,-1) if not pd.isnull(value_data[i]))
        start = pd.to_datetime(params.get('start'), format="%Y-%m-%d %H:%M:%S") if params.get('start') is not None else left
        end = pd.to_datetime(params.get('end'), format="%Y-%m-%d %H:%M:%S") if params.get('end') is not None else right
        
        # unit conversion
        if unit == "ms":
            period *= 0.001
        elif unit == "m":
            period *= 60
        elif unit == "h":
            period *= 3600
        elif unit == "d":
            period *= 3600 * 24
        elif unit != "s":
            raise Exception("Invalid unit: " + unit)
        
        orig_period = (time_data.iloc[-1] - time_data[0]).seconds / (len(time_data) - 1)
        output_data = pd.DataFrame(index=range(int((end - start).seconds / period) + 1), columns=input_data.columns)
        timedelta = pd.Timedelta(seconds=period)
        time_tol = pd.Timedelta(milliseconds=0.001)
        
        # resample function definitions
        # upsample
        if period <= orig_period:
            if interp == "NaN":
                def resample_func(timestamp, orig_idx):
                    if time_data[orig_idx] < timestamp - time_tol:
                        orig_idx += 1
                    return orig_idx, value_data[orig_idx] if time_data[orig_idx] < timestamp + time_tol else pd.NA
            elif interp == "FFill":
                def resample_func(timestamp, orig_idx):
                    if time_data[orig_idx] < timestamp + time_tol:
                        orig_idx += 1
                    return orig_idx, value_data[orig_idx - 1]
            elif interp == "BFill":
                def resample_func(timestamp, orig_idx):
                    if time_data[orig_idx] < timestamp - time_tol:
                        orig_idx += 1
                    return orig_idx, value_data[orig_idx]
            elif interp == "Linear":
                def resample_func(timestamp, orig_idx):
                    if time_data[orig_idx + 1] < timestamp - time_tol:
                        orig_idx += 1
                    return orig_idx, value_data[orig_idx] + (timestamp - time_data[orig_idx]).total_seconds() / orig_period * (value_data[orig_idx + 1] - value_data[orig_idx])
            else:
                raise Exception("Invalid parameter 'interp'")
        # downsample
        else:
            if aggr == "Max":
                def resample_func(timestamp, orig_idx):
                    max = value_data[orig_idx]
                    while time_data[orig_idx + 1] < timestamp:
                        orig_idx += 1
                        if value_data[orig_idx] > max:
                            max = value_data[orig_idx]
                    return orig_idx, max
            elif aggr == "Min":
                def resample_func(timestamp, orig_idx):
                    min = value_data[orig_idx + 1]
                    while time_data[orig_idx + 1] < timestamp:
                        orig_idx += 1
                        if value_data[orig_idx] < min:
                            min = value_data[orig_idx]
                    return orig_idx, min
            elif aggr == "First":
                def resample_func(timestamp, orig_idx):
                    res = value_data[orig_idx + 1]
                    while time_data[orig_idx + 1] < timestamp:
                        orig_idx += 1
                    return orig_idx, res
            elif aggr == "Last":
                def resample_func(timestamp, orig_idx):
                    while time_data[orig_idx + 1] < timestamp:
                        orig_idx += 1
                    return orig_idx, value_data[orig_idx]
            elif aggr == "Mean":
                def resample_func(timestamp, orig_idx):
                    sum = value_data[orig_idx]
                    count = 1
                    while time_data[orig_idx + 1] < timestamp:
                        orig_idx += 1
                        sum += value_data[orig_idx]
                        count += 1
                    return orig_idx, sum / count
            elif aggr == "Median":
                def resample_func(timestamp, orig_idx):
                    data = []
                    while time_data[orig_idx + 1] < timestamp:
                        orig_idx += 1
                        data.append(value_data[orig_idx])
                    return orig_idx, pd.Series(data).median()
            else:
                raise Exception("Invalid parameter 'aggr'")

        # resample
        timestamp = start
        new_idx = 0
        orig_idx = int((start - left).total_seconds() / orig_period)
        while timestamp < end + time_tol:
            output_data.iloc[new_idx, 0] = timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            orig_idx, output_data.iloc[new_idx, 1] = resample_func(timestamp, orig_idx)
            timestamp += timedelta
            new_idx += 1
        
        result = FlokDataFrame()
        result.addDF(output_data)
        return result
        
if __name__ == "__main__":
    algorithm = Resample()

    all_info_1 = {
        "input": ["./test_in.csv"],
        "inputFormat": ["csv"],
        "inputLocation": ["local_fs"],
        "output": ["./test_out_1.csv"],
        "outputFormat": ["csv"],
        "outputLocation": ["local_fs"],
        "parameters": {'every': '1.0s', 'interp': 'BFill', 'aggr': 'Min', "start": "2022-01-01 00:00:05", "end": "2022-01-01 00:00:20"}
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