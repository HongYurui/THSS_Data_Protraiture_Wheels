import re
import os
from pandas import merge
from pandasql import sqldf
from FlokAlgorithmLocal import FlokAlgorithmLocal, FlokDataFrame
from Acf import Acf
from Distinct import Distinct
from Histogram import Histogram
from Integral import Integral
from Integralavg import Integralavg
from Mad import Mad
from Median import Median
from Mode import Mode
from Percentile import Percentile
from Period import Period
from Qlb import Qlb
from Resample import Resample
from Sample import Sample
from Segment import Segment
from SelectTimeseries import SelectTimeseries
from Skew import Skew

inputTypes = ['csv']
inputLocation = ['local_fs']
outputPaths = ['./test_out.csv']
outputTypes = ['csv']

input_params_pairs: dict = {}

while True:
    # terminal control
    command = input(">>> ")
    if command in ["exit", "quit", "q"]:
        break
    elif command in ["help", "h"]:
        print("""
        exit, quit, q: exit
        help, h: print this help
        clear, clc, cls: clear screen
        ls [path]: list files in path
        cat [path]: print file content
        select timeseries from dataframe [where condition]: perform a SQL query
        """)
    elif command in ["clear", "clc", "cls"]:
        os.system("clear")
    elif command == "ls" or command[:3] == "ls " or command[:4] == "cat ":
        os.system(command)
    elif command == "cd" or command[:3] == "cd ":
        print("changing directory is not supported")
    elif command  == "":
        continue
    else:
        try:
            # preprocess the command by extracting patterns
            pattern = re.findall(r"select\s+(?:\w+,\s*[\"\'](\w+)\((\w+)(?:,\s*(.*))?\)[\"\']|\w+|\*)\s*from\s+(.*?)[\s;]+.*", command)[0]
            
            # input the data
            inputPath = pattern[-1]
            inputPaths = [inputPath]
            originalInput = "orig_" + inputPath
            if originalInput not in globals().keys():
                globals()[originalInput] = FlokAlgorithmLocal().read(inputPaths, inputTypes, inputLocation, outputPaths, outputTypes).get(0)
                
            # handle queries for original data
            if pattern[0] == '':
                globals()[inputPath] = globals()[originalInput].copy()
                print(sqldf(command))
                continue

            # handle queries for function results
            funcName = pattern[0].capitalize()
            params = dict(re.findall(r"\'(\w+)\'\s*=\s*\'([\w\s\-\.:]+)\'", pattern[2]))
            if funcName == 'Sample' and params.get('method') == 'reservoir':
                raise Exception("Sample method 'reservoir' is not supported in SQL query due to the randomness.")
            
            # renew function name and parameters
            if input_params_pairs.get(inputPath) != [funcName, params]:
                input_params_pairs[inputPath] = [funcName, params]
                if inputPath in globals().keys():
                    del globals()[inputPath]

                # run the algorithm
                algorithm = globals()[funcName]()
                for series in globals()[originalInput].columns[1:]:
                    flokdataframe = FlokDataFrame()
                    flokdataframe.addDF(globals()[originalInput].loc[:, ['Time', series]])
                    dataframe = algorithm.run(flokdataframe, params).get(0)
                    if inputPath not in globals().keys():
                        globals()[inputPath] = dataframe
                    else:
                        globals()[inputPath] = merge(globals()[inputPath], dataframe, on='Time')

            # run the SQL query
            print(sqldf(command))

        except Exception as e:
            print(e)
            print("error")