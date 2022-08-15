from datetime import datetime, timedelta
import re
from time import time
import pandas as pd
from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame

class Resample(FlokAlgorithmLocal):
    def run(self, inputDataSets, params):
        input_data = inputDataSets.get(0)
        time_data = pd.Series([datetime.strptime(data, "%Y-%m-%d %H:%M:%S") for data in input_data.iloc[:, 0].values])
        value_data = input_data.iloc[:, 1].astype(float)
        
        # get parameters
        every = params.get("every")
        try:
            if every[-2:] == "ms":
                freq = int(every[:-2])
                unit = "ms"
            else:
                freq = int(every[:-1])
                unit = every[-1]
        except:
            raise Exception("Invalid parameter 'every'")
        interp = params.get("interp", "NaN")
        aggr = params.get("aggr", "Mean")
        start = params.get("start", next(time_data[i] for i in range(len(time_data)) if not pd.isnull(value_data[i])))
        end = params.get("end", next(time_data[i] for i in range(len(time_data)-1,-1,-1) if not pd.isnull(value_data[i])))
        
        # unit conversion
        if unit == "ms":
            freq *= 0.001
        elif unit == "m":
            freq *= 60
        elif unit == "h":
            freq *= 3600
        elif unit == "d":
            freq *= 3600 * 24
        elif unit != "s":
            raise Exception("Invalid unit: " + unit)
        
        prev_freq = (time_data.iloc[-1] - time_data[0]).seconds / (len(time_data) - 1)
        output_data = pd.DataFrame(index=range(int((end - start).seconds / freq) + 1), columns=input_data.columns)
        
        # set timestamp
        timedelta = pd.Timedelta(seconds=freq)
        timestamp = start
        i = 0
        while timestamp < end + pd.Timedelta(milliseconds=1e-6):
            output_data.iloc[i, 0] = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            timestamp += timedelta
            i += 1
        
        
        
        print(output_data)
            
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
        "parameters": {'every': '2s', 'interp': 'linear'}
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