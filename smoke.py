import unittest

loader = unittest.TestLoader()
loader.testMethodPrefix = "test"# default value is "test"
"""
suite1 = loader.discover('Test1', pattern = "Test*.py") 
suite2 = loader.discover('Test2', pattern = "Test*.py")
"""
suite1 = loader.discover('./', pattern = "learner_freq.py")
suite2 = loader.discover('./', pattern = "data.py")
alltests = unittest.TestSuite((suite1, suite2))
unittest.TextTestRunner(verbosity=2).run(alltests)


