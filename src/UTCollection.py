import unittest

from AcfUT import AcfUT
from DistinctUT import DistinctUT
from HistogramUT import HistogramUT
from IntegralUT import IntegralUT
from IntegralavgUT import IntegralavgUT
from MadUT import MadUT
from MedianUT import MedianUT
from MinmaxUT import MinmaxUT
from ModeUT import ModeUT
from MvavgUT import MvavgUT
from PacfUT import PacfUT
from PercentileUT import PercentileUT
from PeriodUT import PeriodUT
from QlbUT import QlbUT
from ResampleUT import ResampleUT
from SampleUT import SampleUT
from SegmentUT import SegmentUT
from SelectTimeseriesUT import SelectTimeseriesUT
from SkewUT import SkewUT
from SplineUT import SplineUT
from SpreadUT import SpreadUT
from StddevUT import StddevUT
from ZscoreUT import ZscoreUT

if __name__ == "__main__":
    suite = unittest.TestSuite()
    for func in ["Acf", "Distinct", "Histogram", "Integral", "Integralavg", "Mad", "Median", "Minmax", "Mode", "Mvavg", "Percentile", "Period", "Qlb", "Resample", "Sample", "Segment", "SelectTimeseries", "Skew", "Spline", "Spread", "Stddev", "Zscore"]:
        func_ut = globals()[func + "UT"]
        i = 1
        while True:
            specific_test = "test_" + func.lower() + "_" + str(i)
            if hasattr(func_ut, specific_test):
                suite.addTest(func_ut(specific_test))
                i += 1
            else:
                break
    r = unittest.TextTestRunner()
    r.run(suite)
