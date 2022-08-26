from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame
import pandas as pd


class Distinct(FlokAlgorithmLocal):
    def run(self, inputDataSets, params):
        input_data = inputDataSets.get(0)
        output_data = input_data
        column = input_data.columns[1]
        q = len(set(output_data[column]))
        j = 'distinct({})'.format(column)
        Time = [pd.to_datetime((i + 1) / 1000.0, unit='s', utc=True).tz_convert("Asia/Shanghai") .strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] for i in range(q)]
        data = {'Time': Time, j: list(
            set(output_data[column]))}
        output_data = pd.DataFrame(data)

        result = FlokDataFrame()
        result.addDF(output_data)
        return result
