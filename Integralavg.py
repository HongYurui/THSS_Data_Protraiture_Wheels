import pandas as pd
from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame
from Integral import Integral

class Integralavg(FlokAlgorithmLocal):
    def run(self, inputDataSets, params):
        input_data = inputDataSets.get(0)
        integral_frame = Integral().run(inputDataSets, params).get(0)
        start = pd.to_datetime(input_data.iloc[0, 0])
        second_data = pd.to_datetime(input_data.iloc[1, 0])
        time_delta = second_data - start
        end = pd.to_datetime(input_data.iloc[-1, 0])
        while pd.isnull(start):
            start += 1
        while pd.isnull(end):
            end -= 1
        timespan = (end - start + time_delta).total_seconds()
        output_data = pd.DataFrame([[integral_frame.iloc[0, 0], integral_frame.iloc[0, 1] / timespan]], index=range(1), columns=['Time', "integralavg" + integral_frame.columns[1][8:]])

        result = FlokDataFrame()
        result.addDF(output_data)
        return result
