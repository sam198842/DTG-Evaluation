#!/usr/bin/python -tt
# Copyright 2010 UCLA
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Weizhe Shi sam198842@gmail.com
# Bin Bi
# 2/3/2012 UCLA CSD

"""
Stemming the tags
"""

import sys
import re
import time
import os
from os import path

output_filename = '2007'

def openFiles(filename, mode):
	try:
		f = open(filename, mode)
		return f
	except IOError:
		print 'Failed to open %s' % filename
		return False

def closeFiles(fin):
	try:
		fin.close()
	except AttributeError:
		print 'Files not opened when trying to close'

def scan(filename, fout):
	fin = openFiles(filename, 'r')
	if not fin:
		return
	
	print '\nStart combining %s: (\'.\' means 10k lines)' % filename
	start = time.time()
	
	cnt = 0
	for line in fin:
		if cnt % 10000 == 0:
			print '.',
		cnt += 1
		fout.write(line)
	
	print '\nFinish combining.\n'
	print 'Cost %.01f sec' % (time.time() - start)

	closeFiles(fin)


# Program Entry point
def main():
	# Get the name from the command line
	if len(sys.argv) >= 3:
		start = time.time()
		input_dir = sys.argv[1]	
		output_dir = sys.argv[2]
		
		if not path.exists(input_dir):
			print "%s doesn't exist" % input_dir
			return

		if not path.exists(output_dir):
			print "%s doesn't exist" % output_dir
			return

		fout = openFiles(path.join(output_dir, output_filename), 'w')
		if not fout:
			return

		for filename in sorted(os.listdir(input_dir)):
			if path.isfile(path.join(input_dir, filename)):
				scan(path.join(input_dir, filename), fout)

		closeFiles(fout)
		
		print 'Cost %.01f sec in total.' % (time.time() - start)

	else:
		print 'Usage: python combine.py input_dir output_dir'


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
	main()

