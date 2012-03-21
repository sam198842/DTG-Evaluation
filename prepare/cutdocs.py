#!/usr/bin/python -tt
# Copyright 2010 UCLA
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Weizhe Shi sam198842@gmail.com
# Bin Bi
# 2/1/2012 UCLA CSD

"""
Cut the docs with tags less than 5
"""

import sys
import re
import time
import os
from os import path

doc_limit = 5

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
	
	print 'Start processing %s: (\'.\' means 10k lines)' % filename
	
	last_id = None
	row = []
	cnt = 0
	for line in fin:
		if cnt % 10000 == 0:
			print '.',
		cnt += 1
		# get the 4 tokens: date, hash, URL, tag      
		tokens = line.split()
		if len(tokens) == 4:
			id = tokens[2]
			tag = re.sub(r'[^a-z0-9]', '', tokens[3].lower())
			# tag maybe empty after stripe
			if tag == '':
				# print 'empty str'
				continue
          
			# just once
			if not last_id:
				last_id = id

			# finish process a URL
			if id != last_id:
				if len(row) >= doc_limit:
					row.insert(0, last_id)
					writeDoc(fout, row)
				row = []
			
			# still the same URL
			row.append(tag)
			last_id = id
	
	# deal with the last URL
	if len(row) >= doc_limit:
		row.insert(0, last_id)
		writeDoc(fout, row)
	
	print '\nFinish processing the data.\n'
	closeFiles(fin, fout)


# Entry point
def main():
	# Get the name from the command line
	if len(sys.argv) >= 3:
		time.clock()
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
		
		print 'Cost %.03f sec' % time.clock()
	else:
		print 'Usage: python cutdoc.py input_dir output_dir'


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
	main()

