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
        
        nannum = 0
        for j in range(0, input_data.shape[0]):
            if input_data.iloc[j, 1] == nan:
                nannum += 1
        if nannum > (input_data.iloc[:, 1] == input_data.iloc[:, 1].mode()[0]).sum():
                mode = nan
        else:
            mode = input_data.iloc[:, 1].mode()[0]
        output_data.iloc[0, 1] = mode
        output_data.iloc[0, 0] = datetime.strptime('1970-01-01 08:00:00', "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d 08:00:00")
        
        result = FlokDataFrame()
        result.addDF(output_data)
        return result
        