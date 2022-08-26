import pandas as pd
from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame

class Minmax(FlokAlgorithmLocal):
    def run(self, inputDataSets, params):
        input_data = inputDataSets.get(0)
        compute = params.get("compute", "batch")
        min = params.get("min", 0)
        max = params.get("max", 1)
        if min > max:
            temp = max
            max = min
            min = temp

        # header format
        value_header = 'minmax(' + input_data.columns[1]
        param_list = ['compute', 'min', 'max']
        if compute == "stream":
            for param in param_list:
                if param in params:
                    value_header += ', \'' + param + '\'=\'' + str(params[param]) + '\''
        value_header += ')'
        
        output_data = pd.DataFrame(index=range(input_data.shape[0]), columns=['Time', value_header], dtype=object)
        MAX = input_data.iloc[:, 1].max()
        MIN = input_data.iloc[:, 1].min()
        for i in range(0, input_data.shape[0]):
            if compute == "stream":
                output_data.iloc[i, 1] = (input_data.iloc[i, 1] - MIN)/(MAX - MIN)*(max - min) + min
            else:
                output_data.iloc[i, 1] = (input_data.iloc[i, 1] - MIN)/(MAX - MIN)
        output_data.iloc[:, 0] = input_data.iloc[:, 0]

        result = FlokDataFrame()
        result.addDF(output_data)
        return result
        
