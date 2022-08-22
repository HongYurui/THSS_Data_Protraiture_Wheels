from datetime import datetime
import pandas as pd
from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame

class Period(FlokAlgorithmLocal):
    def run(self, inputDataSets, params):
        input_data = inputDataSets.get(0)
        output_data = pd.DataFrame([[0] * input_data.shape[1]], index=range(1), columns=input_data.columns)
        time_data = pd.Series([datetime.strptime(data, "%Y-%m-%d %H:%M:%S") for data in input_data.iloc[:, 0].values])
        
        period = input_data.shape[0]
        flag = 1
        for column in range(1, input_data.shape[1]):
            for i in range(1, input_data.shape[0]-1):
                if input_data.iloc[i, column] == input_data.iloc[0, column]:
                    if input_data.shape[0] % i != 0:
                        flag = 0
                        break
                    flag = 1
                    j = 0
                    k = j
                    while k+2*i < input_data.shape[0]:
                        for j in range(k, k+i):
                            if input_data.iloc[j, column] != input_data.iloc[j+i, column]:
                                flag = 0
                                break
                        k = k+i
                        if flag == 0:
                            break
                else:
                    flag = 0
                    break
            if flag == 1:
                period = i
                break
            print(period)
            output_data[0, column] = period
                
        output_data.iloc[0, 0] = time_data[0].strftime("%Y-%m-%d 00:00:00")
        result = FlokDataFrame()
        result.addDF(output_data)
        return result
        
if __name__ == "__main__":
    algorithm = Period()

    all_info_1 = {
        "input": ["./test_in.csv"],
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

    dataSet = algorithm.read(inputPaths, inputTypes, inputLocation, outputPaths, outputTypes)
    result = algorithm.run(dataSet, params)
    algorithm.write(outputPaths, result, outputTypes, outputLocation)