from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame
import numpy as np 
import pandas as pd

class segment(FlokAlgorithmLocal):
    def calculate_error(st, seq_range):
        #print(seq_range)
        x = np.arange(seq_range[0], seq_range[1] + 1)
        y = np.array(st[seq_range[0]:seq_range[1] + 1])
        # 返回回归系数、残差
        x_, y_ = x.mean(), y.mean()
        num = ((x - x_)*(y - y_)).sum()
        den = ((x - x_)**2).sum()
        _m = num/den
        _b = y_ - _m*x_
        error = (abs(_m*x + _b-y)).sum()/len(x)
        return error


    def linear(a):
        x = np.arange(0, len(a))
        y = np.array(a)
        # 返回回归系数
        x_, y_ = x.mean(), y.mean()
        num = ((x - x_)*(y - y_)).sum()
        den = ((x - x_)**2).sum()
        _m = num/den
        _b = y_ - _m*x_
        return list(_m*x + _b)


    def Bottom_Up(T, max_error):
        seg_piece = []
        seg = []
        merge_cost = []
        for i in range(0, len(T), 2):
            seg_piece += [T[i:i + 2]]
            seg.append((i, i + 1))
        for i in range(0, len(seg_piece) - 2):
            merge_cost.insert(i, segment.calculate_error(T, (seg[i][0], seg[i + 1][1])))
        while  min(merge_cost) < max_error:
            index = merge_cost.index(min(merge_cost))
            seg_piece[index] = segment.linear(seg_piece[index] + seg_piece[index + 1])
            seg[index] = (seg[index][0], seg[index + 1][1])
            del seg_piece[index + 1]
            del seg[index + 1]
            if index > 1:
                merge_cost[index -1] = segment.calculate_error(T, (seg[index - 1][0], seg[index][1]))
            if index + 1 < len(merge_cost):
                merge_cost[index] = segment.calculate_error(T, (seg[index][0], seg[index + 1][1]))
                del merge_cost[index + 1]
            else:
                del merge_cost[index]
            seg_piece[-2] = (seg_piece[-2] + seg_piece[-1])
        del seg_piece[-1]
        return seg_piece
    def run(self, inputDataSets, params,output='first',error=0.1):
        input_data = inputDataSets.get(0)
        timeseries = params.get("timeseries", None)
        if timeseries:
            timeseries_list = timeseries.split(',')
            output_data = input_data[timeseries_list]
            column = timeseries_list[1]
            str_='segment({a},error={b})'.format(a=column,b=error)
            if all([((output_data[column][i] - output_data[column][i-1])-(output_data[column][1] - output_data[column][0]))<1e-10 for i in range(1,len(output_data))]):
                if output == 'all':
                    output_data=output_data
                else:
                    output_data=pd.DataFrame({'Time':output_data['Time'][0],str_:output_data[column][0]},index=[0])
            else:  
                seg_piece = segment.Bottom_Up(list(output_data[column]), error)
                data = []
                if output=='all':
                    for i in range(len(seg_piece)):
                        data += seg_piece[i]
                    output_data = pd.DataFrame(
                        {'Time': (output_data['Time']), str_: data})
                else:
                    for i in range(len(seg_piece)):
                        data.append(seg_piece[i][0])
                    output_data = pd.DataFrame(
                        {'Time': output_data['Time'][0:len(data)], str_: data})

        else:
            output_data = input_data
        result = FlokDataFrame()
        result.addDF(output_data)
        return result


if __name__ == "__main__":
    algorithm = segment()

    all_info_1 = {
        "input": ["./test_in.csv"],
        "inputFormat": ["csv"],
        "inputLocation": ["local_fs"],
        "output": ["./test_out_1.csv"],
        "outputFormat": ["csv"],
        "outputLocation": ["local_fs"],
        "parameters": {}
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
    result = algorithm.run(dataSet, params)
    algorithm.write(outputPaths, result, outputTypes, outputLocation)

    all_info_2 = {
        "input": ["./test_in.csv"],
        "inputFormat": ["csv"],
        "inputLocation": ["local_fs"],
        "output": ["./test_out_2.csv"],
        "outputFormat": ["csv"],
        "outputLocation": ["local_fs"],
        "parameters": {"timeseries": "Time,root.test.d2.s2"}
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
    result = algorithm.run(dataSet, params)
    algorithm.write(outputPaths, result, outputTypes, outputLocation)
