from datetime import datetime
import pandas as pd
import numpy as np
import math
from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame

class Percentile(FlokAlgorithmLocal):
    def run(self, inputDataSets, params):
        input_data = inputDataSets.get(0)
        input_data = input_data.dropna()
        rank = params.get("rank", 0.5)
        error = params.get("error", 0)
        # header format
        value_header = 'percentile(' + input_data.columns[1]
        param_list = ['rank', 'error']
        for param in param_list:
            if param in params:
                value_header += ', \'' + param + '\'=\'' + str(params[param]) + '\''
        value_header += ')'
        output_data = pd.DataFrame([[0, 0]], index=range(1), columns=['Time', value_header])
          
        data = np.array(input_data.iloc[:,1])
        data.sort()
        i = math.ceil(len(data)*rank)
        if i > 1 :
            quantile = float(data[i-1])
        else :
            quantile = float(data[0])       
        if error==0:
            quantile = np.percentile(data, rank*100)
        else:
            a = len(data) * (rank + error)
            b = len(data) * (rank - error)
            for j in range(0, len(data)):
                if j<a and j>b:
                    i = j
                    if i > 1 :
                        quantile = float(data[i-1])
                    else :
                        quantile = float(data[0])
        output_data.iloc[0, 1] = quantile
        output_data.iloc[0, 0] = datetime.strptime('1970-01-01 08:00:00', "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d 08:00:00")

        result = FlokDataFrame()
        result.addDF(output_data)
        return result
        
if __name__ == "__main__":
    algorithm = Percentile()

    all_info_1 = {
        "input": ["./test_in.csv"],
        "inputFormat": ["csv"],
        "inputLocation": ["local_fs"],
        "output": ["./test_out_1.csv"],
        "outputFormat": ["csv"],
        "outputLocation": ["local_fs"],
        "parameters": {'rank' : 0.5, 'error' : 0}
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
