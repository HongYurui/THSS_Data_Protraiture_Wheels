from importlib import import_module
from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame
import pandas as pd
import numpy as np
from datetime import datetime


class Histogram(FlokAlgorithmLocal):
    def run(self, inputDataSets, params):
        input_data = inputDataSets.get(0)
        output_data = input_data
        column = input_data.columns[1]
        max_value = float(np.max(output_data[column]))
        min = params.get("min", -max_value)
        max = params.get("max", max_value)
        count = params.get("count", 1)
        if isinstance(min, str):
            min = float(min)
        if isinstance(max, str):
            max = float(max)
        if isinstance(count, str):
            count = int(count)
        value_header = 'histogram(' + column
        param_list = ['min', 'max', 'count']
        for param in param_list:
            if param in params:
                value_header += ', \'' + param + \
                    '\'=\'' + str(params[param]) + '\''
        value_header += ')'
        bucket = [0]*count
        Time = []
        print(type(output_data[column][0]))
        for j in range(len(output_data[column])):
            if output_data[column][j] < min:
                bucket[0] += 1
            elif output_data[column][j] >= max:
                bucket[-1] += 1
            else:
                for i in range(1, count+1):
                    if (output_data[column][j] >= min+(i-1)*(max-min)/count
                            and output_data[column][j] < min+i*(max-min)/count):
                        bucket[i-1] += 1
        for i in range(count):
            Time.append(datetime.fromtimestamp((i+1)/1000.0))
        Time = pd.Series([t.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                         for t in Time])
        #j = 'histogram({},\'min\'=\'{}\',\'max\'=\'{}\',\'count\'=\'{}\')'.format(column, min, max_, count)
        data = {'Time': Time, value_header: bucket}
        output_data = pd.DataFrame(data)
        result = FlokDataFrame()
        result.addDF(output_data)
        return result


