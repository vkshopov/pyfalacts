# simple freq learner -----------------------------
class FreqLearner(object):
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
			lrn[ls_key][rs] = 0

		lrn[ls_key][rs] +=1
		
		return

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
		return lrn

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
		lrn = {'5_1_2_': {3: 6}, '1_2_3_': {4: 7}, '3_4_5_': {1: 6}}
		ls = [1,2,3]
		rs = 4
		nof = 4
		fl = FreqLearner()
		fl.train_one_sample(lrn,ls,rs,nof)
		self.assertEqual({'5_1_2_': {3: 6}, '1_2_3_': {4: 8}, '3_4_5_': {1: 6}},lrn)

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
		lrn_must_be = {'1_2_3_': {4: 2}, '3_4_1_': {2: 1},'2_3_4_': {1: 1}}
		
		self.assertEqual( lrn_must_be ,fl.train_all_samples(odl,odr,nof))
			
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



