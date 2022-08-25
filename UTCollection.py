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

"""
"Pacf",
"""

if __name__ == "__main__":
    suite = unittest.TestSuite()
    for func in ["Acf", "Distinct", "Histogram", "Integral", "Integralavg", "Mad", "Median", "Minmax", "Mode", "Mvavg",  "Percentile", "Period", "Qlb", "Resample", "Sample", "Segment", "SelectTimeseries", "Skew", "Spline", "Spread", "Stddev", "Zscore"]:
        for i in range(1, 100):
            if hasattr(globals()[func + "UT"], "test_" + func.lower() + "_" + str(i)):
                suite.addTest(globals()[func + "UT"]("test_" + func.lower() + "_" + str(i)))
            else:
                break
    r = unittest.TextTestRunner()
    r.run(suite)
