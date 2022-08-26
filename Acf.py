from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame
import numpy as np
import pandas as pd
from datetime import datetime

class Acf(FlokAlgorithmLocal):
    def run_acf(x):
        len_x = len(x)
        q = ([0]*len_x)
        p = []
        for i in range(len_x):
            q = (x[i:len_x+1])
            if len(q) < len_x:
                q += [0]*(len_x-len(q))
            p.append(np.dot(q, x))
        #wp.reverse()
        for i in range(1, len_x):
            p.insert(i-1,p[-i])
            #p.append(p[len_x-2-i])
        return list(p)

    def run(self, inputDataSets, params):
        input_data = inputDataSets.get(0)
        output_data = input_data
        column = input_data.columns[1]
        output_data.fillna(0, inplace=True)
        output_data.dropna(axis=0,inplace=True)
        value = output_data[column]
        end_value = output_data[column].values[-1]
        if end_value:
            acf_value = list(Acf.run_acf(list(value))/end_value)
        else:
            acf_value = Acf.run_acf(list(value))
        Time = []
        for i in range(0, 2*len(value)-1):
            q = datetime.fromtimestamp((i+1)/1000.0)
            Time.append(q)
        Time = pd.Series([t.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                         for t in Time])
        j = 'acf({f})'.format(f=column)
        data = {'Time': Time, j: acf_value}
        output_data = pd.DataFrame(data)

        result = FlokDataFrame()
        result.addDF(output_data)
        return result


