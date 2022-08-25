from datetime import datetime
import pandas as pd
from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame

class Mad(FlokAlgorithmLocal):
    def run(self, inputDataSets, params):
        input_data = inputDataSets.get(0)

        # header format
        value_header = 'mad(' + input_data.columns[1]
        param_list = ['error']
        for param in param_list:
            if param in params:
                value_header += ', \'' + param + '\'=\'' + str(params[param]) + '\''
        value_header += ')'

        output_data = pd.DataFrame([[0, 0]], index=range(1), columns=['Time', value_header])

        # calculation via pd.DataFrame.mad()
        output_data.iloc[0, 0] = datetime.strptime(input_data.iloc[0, 0], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d 00:00:00")
        output_data.iloc[0, 1] = input_data.iloc[:, 1].astype(float).mad()

        result = FlokDataFrame()
        result.addDF(output_data)
        return result
