from datetime import datetime
from math import nan
import pandas as pd
from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame

class Mode(FlokAlgorithmLocal):
    def run(self, inputDataSets, params):
        input_data = inputDataSets.get(0)
        input_data = input_data.dropna()
        # header format
        value_header = 'mode(' + input_data.columns[1]
        value_header += ')'
        output_data = pd.DataFrame([[0, 0]], index=range(1), columns=['Time', value_header])
        input_type = type(input_data.iloc[1, 1])
        
        # calculation via pd.DataFrame.mode()
        nannum = input_data.iloc[:, 1].isna().sum()
        if nannum > (input_data.iloc[:, 1] == input_data.iloc[:, 1].astype(input_type).mode()[0]).sum():
                output_data.iloc[0, 1] = nan
        else:
            output_data.iloc[0, 1] = input_data.iloc[:, 1].mode()[0]
        output_data.iloc[0, 0] = datetime.strptime('1970-01-01 08:00:00', "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d 08:00:00")
        
        result = FlokDataFrame()
        result.addDF(output_data)
        return result
        
if __name__ == "__main__":
    algorithm = Mode()

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
