from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame
import time
import numpy as np
from scipy.interpolate import CubicSpline
import pandas as pd
from datetime import datetime
from typing import Tuple, List
import bisect


class Spline(FlokAlgorithmLocal):
    def compute_changes(x: List[float]) -> List[float]:
        return [x[i+1] - x[i] for i in range(len(x) - 1)]

    def create_tridiagonalmatrix(n: int, h: List[float]) -> Tuple[List[float], List[float], List[float]]:
        A = [h[i] / (h[i] + h[i + 1]) for i in range(n - 2)] + [0]
        B = [2] * n
        C = [0] + [h[i + 1] / (h[i] + h[i + 1]) for i in range(n - 2)]
        return A, B, C

    def create_target(n: int, h: List[float], y: List[float]):
        return [0] + [6 * ((y[i + 1] - y[i]) / h[i] - (y[i] - y[i - 1]) / h[i - 1]) / (h[i] + h[i-1]) for i in range(1, n - 1)] + [0]

    def solve_tridiagonalsystem(A: List[float], B: List[float], C: List[float], D: List[float]):
        c_p = C + [0]
        d_p = [0] * len(B)
        X = [0] * len(B)

        c_p[0] = C[0] / B[0]
        d_p[0] = D[0] / B[0]
        for i in range(1, len(B)):
            c_p[i] = c_p[i] / (B[i] - c_p[i - 1] * A[i - 1])
            d_p[i] = (D[i] - d_p[i - 1] * A[i - 1]) / \
                (B[i] - c_p[i - 1] * A[i - 1])

        X[-1] = d_p[-1]
        for i in range(len(B) - 2, -1, -1):
            X[i] = d_p[i] - c_p[i] * X[i + 1]

        return X

    def compute_spline(x: List[float], y: List[float]):
        n = len(x)
        if n < 3:
            raise ValueError('Too short an array')
        if n != len(y):
            raise ValueError('Array lengths are different')

        h = Spline.compute_changes(x)
        if any(v < 0 for v in h):
            raise ValueError('X must be strictly increasing')

        A, B, C = Spline.create_tridiagonalmatrix(n, h)
        D = Spline.create_target(n, h, y)

        M = Spline.solve_tridiagonalsystem(A, B, C, D)
        coefficients = [[(M[i+1]-M[i])*h[i]*h[i]/6, M[i]*h[i]*h[i]/2, (y[i+1] -
                                                                       y[i] - (M[i+1]+2*M[i])*h[i]*h[i]/6), y[i]] for i in range(n-1)]

        def spline(val):
            idx = min(bisect.bisect(x, val)-1, n-2)
            z = (val - x[idx]) / h[idx]
            C = coefficients[idx]
            return (((C[0] * z) + C[1]) * z + C[2]) * z + C[3]

        return spline

    def run(self, inputDataSets, params):
        input_data = inputDataSets.get(0)
        output_data = input_data
        points = params.get("points", None)
        if isinstance(points, str):
            points = int(points)
        if len(output_data) >= 4:
            column = input_data.columns[1]
            #output_data[column] = output_data[column]**3
            Time = []
            time0 = time.mktime(time.strptime(
                output_data['Time'][0], "%Y-%m-%d %H:%M:%S"))
            for i in range(len(output_data)):
                Time.append(time.mktime(time.strptime(
                    output_data['Time'][i], "%Y-%m-%d %H:%M:%S"))-time0)
            value = output_data[column]
            # （t，c，k）包含节点向量、B样条曲线系数和样条曲线阶数的元组。
            #tck = interpolate.splrep(Time, value, k=3)
            #c = CubicSpline(Time, value, bc_type=((1, 4.9), (1, 9.9)))
            spline = Spline.compute_spline(Time, value)
            x = (np.linspace(min(Time), max(Time), points)).tolist()
            y = [spline(t) for t in x]
            # y=list(c(x))
            #y = (interpolate.splev(x, tck, der=0)).tolist()
            for i in range(0, len(x)):
                x[i] = datetime.fromtimestamp(x[i])
                # print(type(x[i]))
            Time = pd.Series(
                [t.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] for t in x])
            j = 'spline({},\'points\'=\'{}\')'.format(column, points)
            data = {'Time': x, j: y}
            output_data = pd.DataFrame(data)
        else:
            pass

        result = FlokDataFrame()
        result.addDF(output_data)
        return result


if __name__ == "__main__":
    algorithm = Spline()
    all_info_1 = {
        "input": ["./test_in.csv"],
        "inputFormat": ["csv"],
        "inputLocation": ["local_fs"],
        "output": ["./test_out_1.csv"],
        "outputFormat": ["csv"],
        "outputLocation": ["local_fs"],
        "parameters": {'points': 150}
    }

    params = all_info_1["parameters"]
    inputPaths = all_info_1["input"]
    inputTypes = all_info_1["inputFormat"]
    inputLocation = all_info_1["inputLocation"]
    outputPaths = all_info_1["output"]
    outputTypes = all_info_1["outputFormat"]
    outputLocation = all_info_1["outputLocation"]

    dataSet = algorithm.read(inputPaths, inputTypes,
                             inputLocation, outputPaths, outputTypes)
    from SelectTimeseries import SelectTimeseries
    dataSet = SelectTimeseries().run(
        dataSet, {"timeseries": "Time,root.test.d2.s2"})
    result = algorithm.run(dataSet, params)
    algorithm.write(outputPaths, result, outputTypes, outputLocation)
    '''
    all_info_2 = {
        "input": ["./test_in.csv"],
        "inputFormat": ["csv"],
        "inputLocation": ["local_fs"],
        "output": ["./test_out_2.csv"],
        "outputFormat": ["csv"],
        "outputLocation": ["local_fs"],
        "parameters": {'points':200}
    }

    params = all_info_2["parameters"]
    inputPaths = all_info_2["input"]
    inputTypes = all_info_2["inputFormat"]
    inputLocation = all_info_2["inputLocation"]
    outputPaths = all_info_2["output"]
    outputTypes = all_info_2["outputFormat"]
    outputLocation = all_info_2["outputLocation"]

    dataSet = algorithm.read(inputPaths, inputTypes,
                             inputLocation, outputPaths, outputTypes)
    from SelectTimeseries import SelectTimeseries
    dataSet = SelectTimeseries().run(
        dataSet, {"timeseries": "Time,root.test.d2.s2"})
    result = algorithm.run(dataSet, params)
    algorithm.write(outputPaths, result, outputTypes, outputLocation)
    '''
