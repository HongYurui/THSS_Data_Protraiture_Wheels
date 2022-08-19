from pandasql import sqldf
from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame
from SelectTimeseries import SelectTimeseries
from Resample import Resample

algorithm = Resample()

all_info_1 = {
    "input": ["./test_in.csv"],
    "inputFormat": ["csv"],
    "inputLocation": ["local_fs"],
    "output": ["./test_out_1.csv"],
    "outputFormat": ["csv"],
    "outputLocation": ["local_fs"],
    "parameters": {'every': '1.0s', 'interp': 'BFill', 'aggr': 'Min', "start": "2022-01-01 00:00:05", "end": "2022-01-01 00:00:20"}
}

params = all_info_1["parameters"]
inputPaths = all_info_1["input"]
inputTypes = all_info_1["inputFormat"]
inputLocation = all_info_1["inputLocation"]
outputPaths = all_info_1["output"]
outputTypes = all_info_1["outputFormat"]
outputLocation = all_info_1["outputLocation"]

dataSet = algorithm.read(inputPaths, inputTypes, inputLocation, outputPaths, outputTypes)
input_data = SelectTimeseries().run(dataSet, {"timeseries": "Time,root.test.d2.s2"})
result = algorithm.run(input_data, params)
algorithm.write(outputPaths, result, outputTypes, outputLocation)

df = algorithm.run(input_data, params).next()
resample = algorithm.run

# data_sql = sqldf("select Time, \"resample(root.test.d2.s2, 'every'='1.0s', 'interp'='BFill', 'aggr'='Min', 'start'='2022-01-01 00:00:05', 'end'='2022-01-01 00:00:20')\" from df;")

data_sql = sqldf(input(">>> "))
print(data_sql.head())
