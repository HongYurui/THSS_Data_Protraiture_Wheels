from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame
import pandas as pd

class Acf(FlokAlgorithmLocal):
    def run_acf(x):
        len_x = len(x)
        q = ([0] * len_x)
        p = []
        for i in range(len_x):
            q = (x[i:len_x + 1])
            if len(q) < len_x:
                q += [0] * (len_x - len(q))
            p.append(sum(a * b for a, b in zip(q, x)))
        for i in range(1, len_x):
            p.insert(i-1, p[-i])
        return list(p)

    def run(self, inputDataSets, params):
        input_data = inputDataSets.get(0)
        output_data = input_data
        column = input_data.columns[1]
        output_data.fillna(0, inplace=True)
        output_data.dropna(axis=0, inplace=True)
        value = output_data[column]
        end_value = output_data[column].values[-1]
        if end_value:
            acf_value = list(Acf.run_acf(list(value)) / end_value)
        else:
            acf_value = Acf.run_acf(list(value))
        Time = [pd.to_datetime((i + 1) / 1000.0, unit='s', utc=True).tz_convert("Asia/Shanghai") .strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] for i in range(2 * len(value) - 1)]
        j = 'acf({f})'.format(f=column)
        data = {'Time': Time, j: acf_value}
        output_data = pd.DataFrame(data)

        result = FlokDataFrame()
        result.addDF(output_data)
        return result
