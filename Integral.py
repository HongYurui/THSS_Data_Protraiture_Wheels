import pandas as pd
from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame

class Integral(FlokAlgorithmLocal):
    def run(self, inputDataSets, params):
        input_data = inputDataSets.get(0)

        # header format
        value_header = 'integral(' + input_data.columns[1]
        param_list = ['unit']
        for param in param_list:
            if param in params:
                value_header += ', \'' + param + '\'=\'' + str(params[param]) + '\''
        value_header += ')'

        output_data = pd.DataFrame([[0, 0]], index=range(1), columns=['Time', value_header])
        time_data = pd.Series([pd.to_datetime(data, format="%Y-%m-%d %H:%M:%S") for data in input_data.iloc[:, 0]])
        value_data = input_data.iloc[:, 1].astype(float)

        # integration
        i = 0
        while pd.isnull(value_data[i]):
            i += 1
        while i < len(value_data) - 1:
            j = i + 1
            while pd.isnull(value_data[j]):
                j += 1
            output_data.iloc[0, 1] += (value_data[i] + value_data[j]) * (time_data[j] - time_data[i]).seconds / 2
            i = j

        # time unit conversion
        unit = params.get("unit", "1s")
        if unit == "1S":
            ratio = 0.001
        elif unit == "1s":
            ratio = 1
        elif unit == "1m":
            ratio = 60
        elif unit == "1h":
            ratio = 3600
        elif unit == "1d":
            ratio = 3600 * 24
        else:
            raise Exception("Invalid unit: " + unit)

        output_data.iloc[0, 0] = "1970-01-01 08:00:00.000"
        output_data.iloc[0, 1] /= ratio

        result = FlokDataFrame()
        result.addDF(output_data)
        return result
