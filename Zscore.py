from datetime import date, datetime
from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame
import math
import pandas as pd
from datetime import datetime
import numpy as np

class Zscore(FlokAlgorithmLocal):
    def run(self, inputDataSets, params):
        input_data = inputDataSets.get(0)
        output_data = input_data
        output_data.dropna(inplace=True)
        column = input_data.columns[1]
        compute = params.get('compute', 'batch')
        Time = []
        for i in range(len(output_data)):
            Time.append(datetime.fromtimestamp((i+1)/1000))
        Time = pd.Series([t.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                         for t in Time])
        if compute == 'stream':
            avg = params.get("avg", 0)
            std = params.get("std", 1)
            if isinstance(avg, str):
                avg = float(avg)
            if isinstance(std, str):
                std = float(std)
            if std == 0 :
                raise ValueError("std must not be 0")
            output_data[column] = (output_data[column]-avg)/std
            j = 'zscore({},\'compute\'=\'{}\',\'avg\'=\'{}\',\'std\'=\'{}\')'.format(
                column, compute,avg, std)
            data = {'Time': Time, j: output_data[column]}
            output_data = pd.DataFrame(data)
        else:
            mean = sum(output_data[column])/len(output_data[column])
            std = math.sqrt(
                sum((output_data[column]-mean) ** 2)/len(output_data[column]))
            output_data[column] = (output_data[column]-mean)/std
            j = 'zscore('+str(column)+')'
            data = {'Time': Time, j: output_data[column]}
            output_data = pd.DataFrame(data)

        result = FlokDataFrame()
        result.addDF(output_data)
        return result


