# simple freq learner -----------------------------
class FreqLearner(object):

	#add coefficients of learniong and amnesia
	#coa - coefficient of amnesia
	#col - coefficient of learning

	coa = 0.04
	col = 0.2

	def create_learner(self):
		lrn = {}

		return lrn

	def train_one_sample(self, lrn, ls,rs,nof):
		#print ls,rs
		ls_key = self.encode_key(ls)
		if (not(ls_key in lrn)):
			lrn[ls_key] = {}
		
		#print ls_key
		#print rs
		if (not rs in lrn[ls_key]):
			lrn[ls_key][rs] = 0.0

		lrn[ls_key][rs] += self.col
		if lrn[ls_key][rs] > 1.0:
			lrn[ls_key][rs] =1.0

	def encode_key(self,ls):
		str_key =""
		for i in ls:
			str_key +=str(int(i))+"_"
		
		return str_key

	def decode_key(self,str):
		#lst = []
		#lst = map(int,str.split("_"))
		str = str[0:-1]# strip last delimiter becouse after split we get "error: '' is not an integer" 
		lst = [int(n) for n in str.split('_')]
		
		return lst

	def train_all_samples(self,odl,odr,nof):

		lrn = self.create_learner()
		#print odr
		for i in range(len(odl)):
			self.train_one_sample( lrn, odl[i],odr[i],nof)
			self.decrease_other_samples( lrn, odl[i], nof)
		return lrn

	def decrease_other_samples(self,lrn,ls_positive, nof):
		ls_pos_key = self.encode_key(ls_positive)
		for ls_key in lrn:
			if( ls_key != ls_pos_key):
				self.decrease_one_sample(lrn,ls_key,nof)
	
	def decrease_one_sample(self,lrn,ls_key,nof):
		for rs in lrn[ls_key]:
			lrn[ls_key][rs] -= self.coa
			if lrn[ls_key][rs] < 0.0:
				lrn[ls_key][rs] = 0.0



	#simple freq classifier------------------------------------------------------------

	def classify_one_sample(self,ls,lrn):
		tmp_rs = {}
		tmp_rs = self.get_all_rs(ls,lrn)
		frs = max(tmp_rs, key=tmp_rs.get)
		return frs

	def get_all_rs(self,ls,lrn):
		#returns sub dictionary with all right sides(facts) and their frequency e.g. {1:12, 2:4, 3:8} 
		tmp_rs = {}
		ls_key = self.encode_key(ls)
		
		tmp_rs = lrn[ls_key]
		#print tmp_rs
		return tmp_rs


import unittest

class TestFreqLearner(unittest.TestCase):

	def setUp(self):
		self.fl1 = FreqLearner()
	        #pass

	def test_train_one_sample(self):
		lrn = {'5_1_2_': {3: 0}, '1_2_3_': {4: 0}, '3_4_5_': {1: 0}}
		ls = [1,2,3]
		rs = 4
		nof = 4
		fl = FreqLearner()
		fl.train_one_sample(lrn,ls,rs,nof)
		must_be_lrn = {'5_1_2_': {3: 0}, '1_2_3_': {4: 0}, '3_4_5_': {1: 0}}
		must_be_lrn['1_2_3_'][4] += fl.col
		self.assertEqual(must_be_lrn,lrn)

	def test_encode_key(self):
		ls = [1,2,3]
		fl = FreqLearner()
		
		self.assertEqual("1_2_3_",fl.encode_key(ls)) 

	def test_decode_key(self):
		str = "1_2_3_"
		fl = FreqLearner()
		
		self.assertEqual([1,2,3],fl.decode_key(str))
		
	def test_train_all_samples(self):
		odl = [[1,2,3],
				[1,2,3],
				[2,3,4],
				[3,4,1]]
		odr = [4,4,1,2]
		nof = 0

		fl = FreqLearner()
		lrn_must_be = {'1_2_3_': {4: 0}, '3_4_1_': {2: 0},'2_3_4_': {1: 0}}
		lrn_must_be['1_2_3_'][4] += fl.col
		lrn_must_be['1_2_3_'][4] += fl.col

		lrn_must_be['2_3_4_'][1] += fl.col
		lrn_must_be['1_2_3_'][4] -= fl.coa

		lrn_must_be['3_4_1_'][2] += fl.col
		lrn_must_be['1_2_3_'][4] -= fl.coa
		lrn_must_be['2_3_4_'][1] -= fl.coa

		self.assertEqual( lrn_must_be ,fl.train_all_samples(odl,odr,nof))

	def test_decrease_other_samples(self):
		fl = FreqLearner()
		nof = 4
		fl.col = 0.1
		fl.coa = 0.02
		ls_pos = [3,4,1]
		lrn = {'1_2_3_': {4: 1.0}, '3_4_1_': {2: 1.0},'2_3_4_': {1: 1.0}}
		lrn_must_be = {'1_2_3_': {4: 0.98}, '3_4_1_': {2: 1.0},'2_3_4_': {1: 0.98}}
		fl.decrease_other_samples(lrn,ls_pos,nof)
		self.assertEqual( lrn_must_be, lrn)

	def test_decrease_one_sample(self):
		fl = FreqLearner()
		nof = 4
		fl.col = 0.1
		fl.coa = 0.02
		ls_key = '1_2_3_'
		lrn = {'1_2_3_': {4: 1.0}, '3_4_1_': {2: 1.0},'2_3_4_': {1: 1.0}}
		lrn_must_be = {'1_2_3_': {4: 0.98}, '3_4_1_': {2: 1.0},'2_3_4_': {1: 1.0}}
		fl.decrease_one_sample(lrn,ls_key,nof)
		self.assertEqual( lrn_must_be, lrn)

		#self.assertTrue(False)

	def test_classify_one_sample(self):
		ls = [1,2,3]
		lrn = {'1_2_3_': {4: 2, 1:1}, '3_4_1_': {2: 1},'2_3_4_': {1: 1}}
				
		fl = FreqLearner()
		rs_must_be = 4

		self.assertEqual(rs_must_be ,fl.classify_one_sample(ls,lrn))
	
	def test_get_all_rs(self):
		ls = [1,2,3]
		lrn = {'1_2_3_': {4: 2, 1:1}, '3_4_1_': {2: 1},'2_3_4_': {1: 1}}
				
		fl = FreqLearner()
		rs_must_be = {4: 2, 1:1}

		self.assertEqual(rs_must_be ,fl.get_all_rs(ls,lrn))
	
if __name__ == '__main__':
	unittest.main()
