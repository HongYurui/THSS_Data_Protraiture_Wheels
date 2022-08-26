from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame
import math
import pandas as pd


class Skew(FlokAlgorithmLocal):
    def run(self, inputDataSets, params):
        input_data = inputDataSets.get(0)
        output_data = input_data
        column = input_data.columns[1]
        output_data.dropna(inplace=True)
        mean = sum(output_data[column])/len(output_data[column])
        std = math.sqrt(sum((output_data[column]-mean) **
                        2)/len(output_data[column]))
        skew = sum(((output_data[column]-mean)/std)** 3)/len(output_data[column])
        j = 'skew({})'.format(column)
        data = {'Time': '1970-01-01 08:00:00.000', j: skew}
        output_data = pd.DataFrame(data, index=[0])

        result = FlokDataFrame()
        result.addDF(output_data)
        return result


