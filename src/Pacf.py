import pandas as pd
import numpy as np
import math
from scipy.linalg import toeplitz
from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame

def yule_walker(ts, order):
    x = np.array(ts) - np.mean(ts)
    n = x.shape[0]
    r = np.zeros(order+1, np.float64)
    r[0] = x.dot(x) / n
    for k in range(1, order+1):
        r[k] = x[:-k].dot(x[k:]) / (n - k)
    R = toeplitz(r[:-1])
    return np.linalg.solve(R, r[1:])

def pacf(ts, k):
    res = [1,]
    for i in range(1, k+1):
        res.append(yule_walker(ts, i)[-1])
    return np.array(res)

class Pacf(FlokAlgorithmLocal):
    def run(self, inputDataSets, params):
        input_data = inputDataSets.get(0)
        lag = params.get("lag")
        if lag == None or lag<=0:
            params["lag"] = min(input_data.shape[0]-1, int(10*math.log10(input_data.shape[0])))
        lag = params.get("lag")
        # header format
        value_header = 'pacf(' + input_data.columns[1]
        param_list = ['lag']
        for param in param_list:
            if param in params:
                value_header += ', \'' + param + '\'=\'' + str(params[param]) + '\''
        value_header += ')'
        output_data = pd.DataFrame(index=range(lag+1), columns=['Time'], dtype=object)
        
        data = pacf(np.array(input_data.iloc[:, 1]), lag)
        output_data.insert(loc=len(output_data.columns), column=value_header, value=data)
        for i in range(0, lag+1):
            output_data.iloc[i, 0] = input_data.iloc[i, 0]

        result = FlokDataFrame()
        result.addDF(output_data)
        return result

