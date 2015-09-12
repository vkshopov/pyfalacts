"""
This module convert raw data from csv file
to sets with left side e.g [1,2,3] and right side as 4
"""

import csv

# read data and build data sets---------------------------------------


class Data(object):

    """
    This class convert raw data from csv file
    to sets with left side e.g [1,2,3] and right side as 4
    """

    @staticmethod
    def read_raw_data(input_file):

        """
        Read data from input_file
        and returns raw_data_set
        """

        # input csv file with facts
        # output list with integers

        raw_data_set = []    # raw data set
        with open(input_file, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in reader:
                raw_data_set.append(int(row[0]))

        return raw_data_set

    @staticmethod
    def get_set_of_facts(raw_data_set):

        """
        Get raw data set
        returns python set_of_facts with unique data smaples
        """

        # sof   - set of unique facts
        tmp_list = raw_data_set[:]
        sof = set(tmp_list)

        return sof

    @staticmethod
    def build_disc_data(raw_data_set, size_of_window):

        """
        Builds discrete data
        gets raw data set [1,2,3,4,5,6,7,8,9...100]  and size of window e.g. 3
        returns data set as [[1,2,3]
                             [4,5,6]
                             ...
                             [98,99,100]]
        """

        sod = len(raw_data_set) - (size_of_window - 1)
        # print sod
        data_set = []
        for i in range(sod):
            tmp = []
            for j in range(size_of_window):
                tmp.append(raw_data_set[i+j])
            data_set.append(tmp)

        return data_set

    @staticmethod
    def build_observed_data_set(data_set):

        """
        From data set of subsequences
        construct two data sets one witk left side with length sow-1
        and one with the last sample of subseq that represents the right side
        """

        # if numpy used the we could do the following:
        # right_side_data_set = data_set[1:,-1]
        # left_side_data_set = data_set[:-1,:]
        # however with plain pthon list we use the following:

        nrows = len(data_set)  # number of rows
        # ncols = len(data_set[0]) we dont need it
        right_side_data_set = []
        for i in range(1, nrows):
            right_side_data_set.append(data_set[i][-1])
        left_side_data_set = []
        for i in range(0, nrows-1):
            tmp = data_set[i]
            left_side_data_set.append(tmp)

        return (left_side_data_set, right_side_data_set)

import unittest


class TestData(unittest.TestCase):  # pylint: disable=R0904

    """
    This is testing class for Data class
    """

    def setUp(self):

        """
        prepare some generic members
        """

        self.testfile = "./data/data_test2.csv"
        self.paragon = [1, 2, 3, 4, 5, 6]
        self.sow = 3
        self.my_data = Data

        # pass

    def test_read_raw_data(self):

        """
        tests Data.read_raw_data with correct input_file
        """

        result_must_be = self.paragon
        my_data = Data()

        self.assertEqual(result_must_be, my_data.read_raw_data(self.testfile))

        # TODO
        # should tests Data.read_raw_data when input_file can not be found

    def test_get_set_of_facts(self):

        """
        tests Data.get_set_of_facts(data_set)
        TODO
        it should not rely on d.read_raw_data(self.testfile)
        """

        dat = Data()
        result_must_be = set(self.paragon)

        self.assertEqual(result_must_be,
                         dat.get_set_of_facts
                         (dat.read_raw_data(self.testfile)))

        # TODO
        # should tests Data.get_set_of_facts(data_set)
        # when data_set is empty or incorrect

    def test_build_disc_data(self):

        """
        tests Data.build_disc_data(raw_data_set) when raw_data_set is ok
        """

        result_must_be = [[1, 2, 3],
                          [2, 3, 4],
                          [3, 4, 5],
                          [4, 5, 6]]
        raw_data_set = [1, 2, 3, 4, 5, 6]
        data = Data()

        self.assertItemsEqual(result_must_be,
                              data.build_disc_data(raw_data_set, 3))

        # TODO
        # should tests Data.build_disc_data(raw_data_set)
        # when raw_data_set is empty or incorrect

    def test_build_observed_ds_left(self):

        """
        tests Data.build_observed_data_set(data_set)
        comapre left side data sets
        when data_set is ok
        """

        data_set = [[1, 2, 3],
                    [2, 3, 4],
                    [3, 4, 5],
                    [4, 5, 6]]
        must_be_left_side_data_set = [[1, 2, 3],
                                      [2, 3, 4],
                                      [3, 4, 5]]
        data = Data()
        left_data_set = data.build_observed_data_set(data_set)[0]

        self.assertEqual(must_be_left_side_data_set, left_data_set)

    def test_build_observed_ds_iright(self):

        """
        tests Data.build_observed_data_set(data_set)
        comprae right side data sets
        when data_set is ok
        """

        data_set = [[1, 2, 3],
                    [2, 3, 4],
                    [3, 4, 5],
                    [4, 5, 6]]
        must_be_right_side_data_set = [4, 5, 6]
        data = Data()
        right_data_set = data.build_observed_data_set(data_set)[1]

        self.assertEqual(must_be_right_side_data_set, right_data_set)

if __name__ == '__main__':
    unittest.main()
