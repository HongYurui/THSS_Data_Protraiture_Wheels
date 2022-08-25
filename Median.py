import pandas as pd
from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame

class Median(FlokAlgorithmLocal):
    def run(self, inputDataSets, params):
        input_data = inputDataSets.get(0)

        # header format
        value_header = 'median(' + input_data.columns[1]
        param_list = ['error']
        for param in param_list:
            if param in params:
                value_header += ', \'' + param + '\'=\'' + str(params[param]) + '\''
        value_header += ')'

        output_data = pd.DataFrame([[0, 0]], index=range(1), columns=['Time', value_header])

        # calculation via pd.DataFrame.median()
        output_data.iloc[0, 0] = pd.to_datetime(input_data.iloc[0, 0], format="%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d 00:00:00.000")
        output_data.iloc[0, 1] = input_data.iloc[:, 1].astype(float).median()

        result = FlokDataFrame()
        result.addDF(output_data)
        return result
