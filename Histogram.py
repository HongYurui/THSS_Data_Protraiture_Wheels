from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame
import pandas as pd


class Histogram(FlokAlgorithmLocal):
    def run(self, inputDataSets, params):
        input_data = inputDataSets.get(0)
        output_data = input_data
        column = input_data.columns[1]
        max_value = float(max(output_data[column]))
        min_num = params.get("min", -max_value)
        max_num = params.get("max", max_value)
        count = params.get("count", 1)
        if isinstance(min_num, str):
            min_num = float(min_num)
        if isinstance(max_num, str):
            max_num = float(max_num)
        if isinstance(count, str):
            count = int(count)
        value_header = 'histogram(' + column
        param_list = ['min', 'max', 'count']
        for param in param_list:
            if param in params:
                value_header += ', \'' + param + \
                    '\'=\'' + str(params[param]) + '\''
        value_header += ')'
        bucket = [0]*count
        print(type(output_data[column][0]))
        for j in range(len(output_data[column])):
            if output_data[column][j] < min_num:
                bucket[0] += 1
            elif output_data[column][j] >= max_num:
                bucket[-1] += 1
            else:
                for i in range(1, count+1):
                    if (output_data[column][j] >= min_num+(i-1)*(max_num-min_num)/count
                            and output_data[column][j] < min_num+i*(max_num-min_num)/count):
                        bucket[i-1] += 1
        Time = [pd.to_datetime((i + 1) / 1000.0, unit='s', utc=True).tz_convert("Asia/Shanghai") .strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] for i in range(count)]
        #j = 'histogram({},\'min\'=\'{}\',\'max\'=\'{}\',\'count\'=\'{}\')'.format(column, min, max_, count)
        data = {'Time': Time, value_header: bucket}
        output_data = pd.DataFrame(data)
        result = FlokDataFrame()
        result.addDF(output_data)
        return result
