from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame
import pandas as pd
from datetime import datetime


class Distinct(FlokAlgorithmLocal):
    def run(self, inputDataSets, params):
        input_data = inputDataSets.get(0)
        output_data = input_data
        column = input_data.columns[1]
        q = len(set(output_data[column]))
        j = 'distinct({})'.format(column)
        Time = []
        for i in range(q):
            Time.append(datetime.fromtimestamp((i+1)/1000.0))
        Time = pd.Series([t.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                         for t in Time])
        data = {'Time': Time, j: list(
            set(output_data[column]))}
        output_data = pd.DataFrame(data)

        result = FlokDataFrame()
        result.addDF(output_data)
        return result


