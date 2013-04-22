import unittest
import query
import datetime

class Test(unittest.TestCase):
    def test_query(self):
        time = datetime.datetime.now()
        print time
        print query.unix_time_millis(time)
    pass

if __name__ =='__main__':
    unittest.main()
