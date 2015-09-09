import unittest

import logging 
import logging.config


logging.config.fileConfig('logging.conf')

# create logger
logger = logging.getLogger('main_freq')
logger.info("main_freq smoke starts" )


loader = unittest.TestLoader()
loader.testMethodPrefix = "test"# default value is "test"

suite1 = loader.discover('./', pattern = "learner_freq.py")
suite2 = loader.discover('./', pattern = "data.py")

alltests = unittest.TestSuite((suite1, suite2))
unittest.TextTestRunner(verbosity=2).run(alltests)

logger.info("main_freq smoke finished" )

