import pandas as pd
from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame
from statsmodels.tsa.stattools import acf
from scipy.stats import chi2

class Qlb(FlokAlgorithmLocal):
    def run(self, inputDataSets, params):
        input_data = inputDataSets.get(0)
        time_data = pd.Series([pd.to_datetime(data, format="%Y-%m-%d %H:%M:%S") for data in input_data.iloc[:, 0].values])
        value_data = input_data.iloc[:, 1].astype(float)
        n = len(time_data)

        # get lag
        lag = params.get("lag", n - 2)
        if isinstance(lag, str):
            lag = int(lag)

        # header format
        value_header = 'qlb(' + input_data.columns[1]
        param_list = ['lag']
        for param in param_list:
            if param in params:
                value_header += ', \'' + param + '\'=\'' + str(params[param]) + '\''
        value_header += ')'

        # time format
        output_data = pd.DataFrame(index=range(lag), columns=['Time', value_header])
        timestamp = pd.to_datetime("1970-01-01 08:00:00", format="%Y-%m-%d %H:%M:%S")
        timedelta = pd.to_timedelta(0.001, unit="s")

        # calculate square acf

        acf_data = acf(value_data)[1:]
        weighted_square_acf = [x ** 2 / (n - i - 1) for i, x in enumerate(acf_data)]
        sum_weighted_square_acf = 0

        for i in range(lag):
            timestamp += timedelta
            sum_weighted_square_acf += weighted_square_acf[i]
            output_data.iloc[i, 0] = timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            # LB Q-test
            output_data.iloc[i, 1] = 1 - chi2.cdf(n * (n + 2) * sum_weighted_square_acf, i + 1)

        result = FlokDataFrame()
        result.addDF(output_data)
        return result
