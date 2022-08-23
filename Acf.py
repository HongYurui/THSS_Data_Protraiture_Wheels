from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame
import numpy as np
import pandas as pd
import time
from datetime import datetime

class Acf(FlokAlgorithmLocal):
    def run_acf(x,end_value):
        len_x = len(x)
        q = ([0]*len_x)
        p = []
        for i in range(len_x):
            q = (x[i:len_x+1])
            if len(q) < len_x:
                q+=[0]*(len_x-len(q))
            p.append(np.dot(q, x))
        p.reverse()
        for i in range(0, len_x-1):
            p.append(p[len_x-2-i])
        return list(p/end_value)
    def run(self, inputDataSets, params):
        input_data = inputDataSets.get(0)
        output_data = input_data
        column=input_data.columns[1]
        #time_ = params.get("time_", None)
        time0_ = time.mktime(time.strptime(
            '1970-01-01 08:00:00', '%Y-%m-%d %H:%M:%S'))
        #count = int(time.mktime(time.strptime(time_, '%Y-%m-%d %H:%M:%S'))-time0_)
        output_data.fillna(0, inplace=True)
        a = output_data[column]
        end_value=output_data[column].values[-1]
        c=Acf.run_acf(list(a),end_value)
        Time = []
        for i in range(0, 2*len(a)-1):
            #q = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time0_+i/1000.0))
            q=datetime.fromtimestamp((i+1)/1000.0)
            Time.append(q)
        Time = pd.Series([t.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] for t in Time])
        j = 'acf({f})'.format(f=column)
        data = {'Time': Time, j: c}
        output_data = pd.DataFrame(data)

        result = FlokDataFrame()
        result.addDF(output_data)
        return result


if __name__ == "__main__":
    algorithm = Acf()

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
    '''
    all_info_2 = {
        "input": ["root_test_d1"],
        "inputFormat": ["csv"],
        "inputLocation": ["local_fs"],
        "output": ["./test_out_2.csv"],
        "outputFormat": ["csv"],
        "outputLocation": ["local_fs"],
        "parameters": {"timeseries": "Time,s2"}
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
