import random
import pandas as pd
from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame

class Median(FlokAlgorithmLocal):
    def run(self, inputDataSets, params):
        input_data = inputDataSets.get(0)
        input_data.dropna(inplace=True)

        # get error
        error = params.get("error", 0)
        if isinstance(error, str):
            error = float(error)
        if error < 0 or error > 1:
            raise ValueError("error must be between 0 and 1")

        # header format
        value_header = 'median(' + input_data.columns[1]
        param_list = ['error']
        for param in param_list:
            if param in params:
                value_header += ', \'' + param + '\'=\'' + str(params[param]) + '\''
        value_header += ')'

        output_data = pd.DataFrame([[0, 0]], index=range(1), columns=['Time', value_header])

        # calculation
        output_data.iloc[0, 0] = "1970-01-01 08:00:00.000"
        output_data.iloc[0, 1] = self.median(list(input_data.iloc[:, 1].astype(float)), error)

        result = FlokDataFrame()
        result.addDF(output_data)
        return result

    # partition
    def randomized_partition(self, data):
        r = len(data) - 1
        p = random.randint(0, r)
        data[p], data[r] = data[r], data[p]
        p = 0
        for j in range(r):
            if data[j] <= data[r]:
                data[p], data[j] = data[j], data[p]
                p += 1
        data[p], data[r] = data[r], data[p]
        return p, data

    # find a single number of certain rank
    def odd_find_rank(self, data, rank, error=0):
        p, data = self.randomized_partition(data)
        if p > rank + error:
            return self.odd_find_rank(data[:p], rank, error)
        if p < rank - error:
            return self.odd_find_rank(data[p + 1:], rank - p - 1, error)
        return data[p]

    # find two adjacent numbers of certain rank
    def even_find_rank(self, data, left_rank, error=0):
        p, data = self.randomized_partition(data)
        if left_rank > p + error:
            return self.even_find_rank(data[p + 1:], left_rank - p - 1, error)
        if left_rank + 1 < p - error:
            return self.even_find_rank(data[:p], left_rank, error)
        if error == 0:
            if left_rank == p:
                return (data[p] + self.odd_find_rank(data[p + 1:], 0, error)) / 2
            if left_rank + 1 == p:
                return (self.odd_find_rank(data[:p], left_rank, error) + data[p]) / 2
        else:
            return (data[p - 1] + data[p]) / 2

    # find median through even and odd rank-finding methods
    def median(self, data, error=0):
        assert 0 <= error <= 1
        length = len(data)
        if length % 2 == 0:
            return self.even_find_rank(data, (length - 1) // 2, int(error * length))
        else:
            return self.odd_find_rank(data, (length - 1) // 2, int(error * length))
