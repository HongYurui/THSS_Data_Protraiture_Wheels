import pandas as pd
from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame
from Median import Median

class Mad(FlokAlgorithmLocal):
    def run(self, inputDataSets, params):
        input_data = inputDataSets.get(0)
        input_data.dropna(inplace=True)

        # get error
        error = params.get("error", 0)
        if isinstance(error, str):
            error = float(error)
        if error < 0 or error > 1:
            raise ValueError("error must be between 0 and 1")

        # header format
        value_header = 'mad(' + input_data.columns[1]
        param_list = ['error']
        for param in param_list:
            if param in params:
                value_header += ', \'' + param + '\'=\'' + str(params[param]) + '\''
        value_header += ')'

        output_data = pd.DataFrame([[0, 0]], index=range(1), columns=['Time', value_header])

        # calculation via pd.DataFrame.mad()
        output_data.iloc[0, 0] = pd.to_datetime(input_data.iloc[0, 0], format="%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d 00:00:00")
        median = Median()
        mid = median.median(list(input_data.iloc[:, 1].astype(float)))
        output_data.iloc[0, 1] = median.median([abs(x - mid) for x in input_data.iloc[:, 1].astype(float)])


        result = FlokDataFrame()
        result.addDF(output_data)
        return result
