import csv
import numpy as np

#read data and build data sets---------------------------------------
class Data(object):
	def read_raw_data(self,file):
		# input csv file with facts
		# output list with integers
		
		rds=[] #raw data set
		
		with open(file, 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
			for row in reader:
				rds.append(int(row[0]))
		
		return rds

	def get_set_of_facts(self,data):
		# get unique facts
		# data 	- data set with integer facts
		# sof	- set of unique facts
		
		tmp_list = data[:]
		sof = set(tmp_list)

		return sof

	def build_disc_data(self,rds,sow):
		sod = len(rds) - (sow - 1)
		#print sod
		
		ods = []
		for i in range(sod):
			tmp = []
			for j in range(sow):
				tmp.append(rds[i+j])
			ods.append(tmp)

		return ods

	def build_observed_data_set(self,ods):
		#observed left 
		#observed right
		
		#odr = ods[1:,-1]
		#odl = ods[:-1,:]

		nrows = len(ods)
		ncols = len(ods[0])
		
		odr = []
		for i in range(1,nrows):
			odr.append(ods[i][-1])
		
		odl = []
		for i in range(0,nrows-1):
			tmp = ods[i]
			odl.append(tmp)

		return (odl,odr)

import unittest

class TestData(unittest.TestCase):

	def setUp(self):
		self.testfile = "./data/data_test2.csv"
		self.paragon = [1,2,3,4,5,6]
		self.sow = 3
		self.d = Data

	        #pass

	def test_read_raw_data(self):
		result_must_be = self.paragon
		d = Data()
		self.assertEqual(result_must_be, d.read_raw_data(self.testfile))

	def test_get_set_of_facts(self):
		d = Data()
		result_must_be = set(self.paragon)
		self.assertEqual(result_must_be,d.get_set_of_facts( d.read_raw_data(self.testfile)))

	def test_build_disc_data(self):
		result_must_be = [	[1,2,3],
					[2,3,4],
					[3,4,5],
					[4,5,6]]
		raw_data_set = [1,2,3,4,5,6]
		d = Data()
		self.assertItemsEqual(result_must_be,d.build_disc_data(raw_data_set,3))

	def test_build_observed_data_set_left(self):
		ods = [	[1,2,3],
        		[2,3,4],
        		[3,4,5],
        		[4,5,6]]
		must_be_odl = [	[1,2,3],
				[2,3,4],
				[3,4,5]]
		d = Data()
		(received_odl,received_odr) = d.build_observed_data_set(ods)
		self.assertEqual(must_be_odl,received_odl)

	def test_build_observed_data_set_iright(self):
		ods = [	[1,2,3],
        		[2,3,4],
        		[3,4,5],
        		[4,5,6]]
		must_be_odr = [4,5,6]
		d = Data()
		(received_odl,received_odr) = d.build_observed_data_set(ods)
		self.assertEqual(must_be_odr,received_odr)

	
if __name__ == '__main__':
	unittest.main()


