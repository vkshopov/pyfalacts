"""
# simple freq learner -----------------------------
"""

class FreqLearner(object):
    """
    Frequency learner class
    use a simple frequncy of matching lef_side->right_side
    as a best attribute
    """
    #add coefficients of learniong and amnesia
    #coa - coefficient of amnesia
    coa = 0.04
    #col - coefficient of learning
    col = 0.2

    @staticmethod
    def create_learner():

        """
        create empty leaner
        not quate usefull yet ...
        """

        lrn = {}

        return lrn

    def train_one_sample(self, lrn, left_side, right_side):

        """
        train a learner
        well it train the learner
        with only one sample
        it could be useful for adaptive(ONLINE) training
        """

        ls_key = self.encode_key(left_side)
        if not ls_key in lrn:
            lrn[ls_key] = {}
        if not right_side in lrn[ls_key]:
            lrn[ls_key][right_side] = 0.0

        lrn[ls_key][right_side] += self.col
        if lrn[ls_key][right_side] > 1.0:
            lrn[ls_key][right_side] = 1.0

    @staticmethod
    def encode_key(left_side):

        """
        encodes left side from [1,2,3] to a string '1_2_3_'
        because lists can not be keys in python dictionary
        """

        str_key = ""
        for i in left_side:
            str_key += str(int(i))+"_"
        return str_key

    @staticmethod
    def decode_key(key_str):


        """
        decode a dict key from string '1_2_3_' to list [1,2,3]
        why is this function exists?
        nobody seems to use it ?

        """

        #lst = []
        #lst = map(int,str.split("_"))
        key_str = key_str[0:-1] #strip last delimiter
                        #becouse after split we get
                        #"error: '' is not an integer"
        lst = [int(n) for n in key_str.split('_')]
        return lst

    def train_all_samples(self, left_data_set, right_data_set):

        """
        Use train_one sample to batch the learning process
        """

        lrn = self.create_learner()
        #print right_data_set
        for i in range(len(left_data_set)):
            self.train_one_sample(lrn, left_data_set[i], right_data_set[i])
            self.decrease_other_samples(lrn, left_data_set[i])
        return lrn

    def decrease_other_samples(self, lrn, ls_positive):

        """
        Process "amnesia" to all other samples exept the ls_positve
        """

        ls_pos_key = self.encode_key(ls_positive)
        for ls_key in lrn:
            if ls_key != ls_pos_key:
                self.decrease_one_sample(lrn, ls_key)

    def decrease_one_sample(self, lrn, ls_key):

        """
        Process "amnesia" to all to the sample coded with ls_key in leaner
        """

        for right_side in lrn[ls_key]:
            lrn[ls_key][right_side] -= self.coa
            if lrn[ls_key][right_side] < 0.0:
                lrn[ls_key][right_side] = 0.0


    #simple freq classifier-------------------------------------------

    def classify_one_sample(self, left_side, lrn):

        """
        classifies one sampple
        gets its left_side left side
        and returns the forecasted right side
        """

        tmp_rs = {}
        tmp_rs = self.get_all_rs(left_side, lrn)
        frs = max(tmp_rs, key=tmp_rs.get)
        return frs

    def get_all_rs(self, left_side, lrn):

        """
        #returns sub dictionary with all right sides(facts)
        #and their frequency e.g. {1:12, 2:4, 3:8}
        """

        tmp_rs = {}
        ls_key = self.encode_key(left_side)
        tmp_rs = lrn[ls_key]
        #print tmp_rs
        return tmp_rs


import unittest

class TetFreqLearner(unittest.TestCase): #pylint: disable=R0904

    """
    Test class for FreqLearner
    """

    def setUp(self):

        """
        Sets some internal FreqLearner variables
        """

        self.fl1 = FreqLearner()

    def test_train_one_sample(self):

        """
        tests FreqLearner.train_one_sample
        TODO ?
        """

        lrn = {'5_1_2_': {3: 0},
               '1_2_3_': {4: 0},
               '3_4_5_': {1: 0}}
        left_side = [1, 2, 3]
        right_side = 4
        #nof = 4
        test_fl = FreqLearner()
        test_fl.train_one_sample(lrn, left_side, right_side)
        must_be_lrn = {'5_1_2_': {3: 0},
                       '1_2_3_': {4: 0},
                       '3_4_5_': {1: 0}}
        must_be_lrn['1_2_3_'][4] += test_fl.col

        self.assertEqual(must_be_lrn, lrn)

    def test_encode_key(self):

        """
        Tests FreqLearner.encode_key(ls)
        when ls ois ok
        """

        lef_side = [1, 2, 3]
        test_fl = FreqLearner()

        self.assertEqual("1_2_3_", test_fl.encode_key(lef_side))

        #"""
        #TODO Tests FreqLearner.encode_key(ls) when ls is BAD!
        #"""

    def test_decode_key(self):

        """
        Tests FreqLearner.decode_key(key_str)
        when key_str is ok
        """

        key_str = "1_2_3_"
        test_fl = FreqLearner()

        self.assertEqual([1, 2, 3], test_fl.decode_key(key_str))

        #"""
        #TODO Tests FreqLearner.decode_key(key_str)  when key_str is BAD!
        #"""

    def test_train_all_samples(self):

        """
        Tests FreqLearner.train_all_samples
        where left_data_set and righrt_data_set are ok
        """

        left_data_set = [[1, 2, 3],
                         [1, 2, 3],
                         [2, 3, 4],
                         [3, 4, 1]]
        right_data_set = [4, 4, 1, 2]
        #nof = 0

        test_fl = FreqLearner()
        lrn_must_be = {'1_2_3_': {4: 0}, '3_4_1_': {2: 0}, '2_3_4_': {1: 0}}
        lrn_must_be['1_2_3_'][4] += test_fl.col
        lrn_must_be['1_2_3_'][4] += test_fl.col

        lrn_must_be['2_3_4_'][1] += test_fl.col
        lrn_must_be['1_2_3_'][4] -= test_fl.coa

        lrn_must_be['3_4_1_'][2] += test_fl.col
        lrn_must_be['1_2_3_'][4] -= test_fl.coa
        lrn_must_be['2_3_4_'][1] -= test_fl.coa

        self.assertEqual(lrn_must_be,
                         test_fl.train_all_samples(left_data_set,
                                                   right_data_set))

        #"""
        #TODO Tests FreqLearner.train_all_samples
        #where left_data_set and righrt_data_set are BAD!
        #"""

    def test_decrease_other_samples(self):

        """
        Tests decrease_other_samples(lrn, ls_positive)
        where lrn, ls_positive are ok
        """

        test_fl = FreqLearner()
        #nof = 4
        test_fl.col = 0.1
        test_fl.coa = 0.02
        ls_pos = [3, 4, 1]
        lrn = {'1_2_3_': {4: 1.0},
               '3_4_1_': {2: 1.0},
               '2_3_4_': {1: 1.0}}
        lrn_must_be = {'1_2_3_': {4: 0.98},
                       '3_4_1_': {2: 1.0},
                       '2_3_4_': {1: 0.98}}
        test_fl.decrease_other_samples(lrn, ls_pos)

        self.assertEqual(lrn_must_be, lrn)

        #"""
        #TODO  Tests FreqLearner.decrease_other_samples(lrn, ls_positive)
        #where lrn, ls_positive are BAD!
        #"""


    def test_decrease_one_sample(self):

        """
        Test FreqLearner.decrease_one_sample(lrn,ls_key)
        when lrn,ls_key are ok
        """

        test_fl = FreqLearner()
        #nof = 4
        test_fl.col = 0.1
        test_fl.coa = 0.02
        ls_key = '1_2_3_'
        lrn = {'1_2_3_': {4: 1.0},
               '3_4_1_': {2: 1.0},
               '2_3_4_': {1: 1.0}}
        lrn_must_be = {'1_2_3_': {4: 0.98},
                       '3_4_1_': {2: 1.0},
                       '2_3_4_': {1: 1.0}}
        test_fl.decrease_one_sample(lrn, ls_key)

        self.assertEqual(lrn_must_be, lrn)

        #"""
        #TODO FreqLearner.Learner.decrease_one_sample(lrn,ls_key)
        #when lrn,ls_key are BAD!
        #"""

    def test_classify_one_sample(self):

        """
        Test FreqLearner.classify_one_sample(left_side, lrn)
        when left_side, lrn are ok
        """

        left_side = [1, 2, 3]
        lrn = {'1_2_3_': {4: 2, 1:1},
               '3_4_1_': {2: 1},
               '2_3_4_': {1: 1}}
        test_fl = FreqLearner()
        rs_must_be = 4

        #"""
        #Test FreqLearner.classify_one_sample(left_side, lrn)
        #when left_side, lrn are BAD!
        #"""

        self.assertEqual(rs_must_be,
                         test_fl.classify_one_sample(left_side, lrn))

    def test_get_all_rs(self):

        """
        Tests FreqLearner.get_all_rs(ls,lrn)
        when ls lrn are ok
        """

        lef_side = [1, 2, 3]
        lrn = {'1_2_3_': {4: 2, 1:1},
               '3_4_1_': {2: 1},
               '2_3_4_': {1: 1}}
        test_fl = FreqLearner()
        rs_must_be = {4: 2, 1:1}

        self.assertEqual(rs_must_be, test_fl.get_all_rs(lef_side, lrn))

        #"""
        #TODO Tests FreqLearner.get_all_rs(ls,lrn)
        #when ls lrn are BAD!
        #"""


if __name__ == '__main__':
    unittest.main()
