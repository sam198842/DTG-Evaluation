#!/usr/bin/python -tt
# Copyright 2010 UCLA
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Weizhe Shi sam198842@gmail.com
# Bin Bi
# 2/2/2012 UCLA CSD

"""
Stemming the tags
"""

import sys
import re
import time
import os
from os import path
from nltk.stem.porter import PorterStemmer

st = PorterStemmer()

def openFiles(filename, outdir):
	if not path.isfile(filename):
		print '%s is not a file' % filename
		return False
	if not path.exists(outdir):
		print '%s is not a valid path' % outdir
		return False
	try:
		fin = open(filename, 'r')
		fout = open(outdir + '/' + path.basename(filename), 'w')
		return [fin, fout]
	except IOError:
		return False

def closeFiles(fin ,fout):
	try:
		fin.close()
		fout.close()
	except AttributeError:
		print 'Files not opened when trying to close'

def writeDoc(f, row):
	line = ' '.join(row) + '\n'
	line = str(len(row) - 1) + ' ' + line
	# print line
	f.write(line)

def scan(filename, outdir):
	ret = openFiles(filename, outdir)
	if ret:
		fin, fout = ret
	else:
		return False
	
	print '\nStart stemming %s: (\'.\' means 1k lines)' % filename
	start = time.time()
	
	cnt = 0
	for line in fin:
		if cnt % 1000 == 0:
			print '.',
		cnt += 1
		# get the all the tokens: # of tags, URL, tag, tag, tag, ...
		tokens = line.split()
		row = set()
		# stemming the tags
		for tag in tokens[2:]:
			row.add(st.stem(tag))
		# insert the URL and write to file
		row = list(row)
		row.insert(0, tokens[1])
		writeDoc(fout, row)
	
	print '\nFinish stemming.\n'
	print 'Cost %.01f sec' % (time.time() - start)

	closeFiles(fin, fout)


# Program Entry point
def main():
	# Get the name from the command line
	if len(sys.argv) >= 3:
		start = time.time()
		input_dir = sys.argv[1]	
		output_dir = sys.argv[2]
		
		if not path.exists(input_dir):
			print "%s doesn't exist" % input_dir
			return False

		if not path.exists(output_dir):
			print "%s doesn't exist" % output_dir
			return False

		for filename in os.listdir(input_dir):
			scan(path.join(input_dir, filename), output_dir)
		
		print 'Cost %.01f sec in total.' % (time.time() - start)

	else:
		print 'Usage: python stemming.py input_dir output_dir'


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
	main()

