import unittest

class MyTest(unittest.TestCase):
    def testMe(self):
        pass

suite = unittest.TestLoader().loadTestsFromTestCase(MyTest)
unittest.TextTestRunner(verbosity=2).run(suite)

#unittest.main()
import unittest

class MyTest(unittest.TestCase):
    def testMe(self):
        pass

suite = unittest.TestLoader().loadTestsFromTestCase(MyTest)
unittest.TextTestRunner(verbosity=2).run(suite)

#unittest.main()
