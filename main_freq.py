#!/usr/bin/env python

import sys
import getopt

import inspect, os

import data
import learner_freq 

import logging
import logging.config



#------------------------------------------------------------
def main(argv):
	
	logging.config.fileConfig('logging.conf')

	# create logger
	#logger = logging.getLogger('simpleExample')
	logger = logging.getLogger('main_freq')

	#get arguments from command line
	#parse arguments
	inputfile = ''
	outputfile = ''
	
	try:
		opts, args = getopt.getopt(argv,"hi:o:",["help","infile=","outfile="])

	except getopt.GetoptError, err:
		print str(err)
		usage()
		sys.exit(2)
	
	#print "opt =", opts
	message =''
	for i in range(0, len(opts)):
		#message = '%s:%s' % (i, opts[i].items())
		message = '%s:%s' % (i, opts[i])
		logger.debug("opts = %s", message )

	if opts  == []: # should be at least -i <input_file.csv>
		usage()
		sys.exit(2)

	for opt, arg in opts:
		if opt in ( "-h","--help"):
			usage()
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg
			#print 'Input file is "', inputfile
			#print 'Output file is "', outputfile

	load_data = data.Data()
	#read data from csv file
	rds = load_data.read_raw_data(inputfile)
	#print (rds)

	sof = load_data.get_set_of_facts(rds)
	NOF = len(sof)
	#print (NOF)
	#print (sof)

	SOW = 3
	ods = load_data.build_disc_data(rds,SOW)
	#print ods

	(odl,odr) = load_data.build_observed_data_set(ods)


	#print odr
	lf = learner_freq.FreqLearner()
	lrn = {}
	lrn = lf.train_all_samples(odl,odr,NOF)

	print lrn
	
	frs =[]
	for ls in odl:
		frs.append( lf.classify_one_sample(ls,lrn))

	for i in range(len(odl)):
		print odl[i], odr[i], frs[i]

def usage():
	script_name =  inspect.getfile(inspect.currentframe()) 
	print (str(script_name + ' -i <inputfile> -o <outputfile>'))
	print (str(script_name + ' -h'))
	return

#---------------------------------------------------
if __name__ == "__main__":
	main(sys.argv[1:])
