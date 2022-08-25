import pandas as pd
import random
from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame

class Sample(FlokAlgorithmLocal):
    def run(self, inputDataSets, params):
        input_data = inputDataSets.get(0)

        # get parameters
        method = params.get("method", "reservoir")
        k = params.get("k", 1)
        if isinstance(k, str):
            k = int(k)

        # header format
        value_header = 'sample(' + input_data.columns[1]
        param_list = ['method', 'k']
        for param in param_list:
            if param in params:
                value_header += ', \'' + param + '\'=\'' + str(params[param]) + '\''
        value_header += ')'

        output_data = pd.DataFrame(index=range(k), columns=['Time', value_header])

        # reservoir sampling
        if method == "reservoir":
            for i in range(len(input_data)):
                if i < k:
                    output_data.iloc[i] = input_data.iloc[i]
                else:
                    random_int = random.randint(0, i)
                    if random_int < k:
                        output_data.iloc[random_int] = input_data.iloc[i]
            output_data.sort_values(by=[value_header], inplace=True)
        # isometric sampling
        elif method == "isometric":
            step = int(len(input_data) / k)
            for i in range(k):
                output_data.iloc[i] = input_data.iloc[i * step]
        else:
            raise Exception("Invalid parameter 'method'")

        result = FlokDataFrame()
        result.addDF(output_data)
        return result
