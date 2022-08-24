from datetime import datetime
import pandas as pd
from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame

class Period(FlokAlgorithmLocal):
    def run(self, inputDataSets, params):
        input_data = inputDataSets.get(0)
        input_data = input_data.fillna("fillna")
        # header format
        value_header = 'period(' + input_data.columns[1]
        value_header += ')'
        output_data = pd.DataFrame([[0, 0]], index=range(1), columns=['Time', value_header])
      
        period = input_data.shape[0]
        data = input_data.iloc[:,1]
        flag = 0
        for i in range(1,int(len(data)/2)):
            if data[i] != data[0]:
                pass
            elif data[i] == data[0]:
                if len(data) % i != 0:
                    pass
                else:
                    flag = 1
                    j = 0
                    k = j
                    while k+2*i-1 < len(data):
                        for j in range(k, k+i-1):
                            if data[j] != data[j+i]:
                                flag = 0
                                break
                        if flag == 0:
                            break
                        k = k+i
            if flag == 1:
                period = i
                break
        output_data.iloc[0, 1] = period
        output_data.iloc[0, 0] = datetime.strptime('1970-01-01 08:00:00', "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d 08:00:00")
        
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
