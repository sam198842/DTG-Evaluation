#!/usr/bin/python -tt
# Copyright 2010 UCLA
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Weizhe Shi sam198842@gmail.com
# Bin Bi
# 1/25/2012 UCLA CSD

"""
Analyze the delicious data:
Distribution of # of tags for each URL
"""

import sys
import time

def analyze(file):
	try:
		f = open(file, 'r')
	except IOError:
		return False

	distr = [0.0] * 500

	cnt = 0
	for line in f:
		distr[int(line.split()[0])] += 1
		cnt += 1

	f.close()

	print cnt
	# print distr[0:10]
	print ['%.1f%%' % (item*100/cnt) for item in distr][0:10]

# Entry point
def main():
	# Get the name from the command line
	if len(sys.argv) >= 2:
		start = time.time()
		argv_file = sys.argv[1]
		analyze(argv_file)
		print 'Cost %.03f sec' % (time.time() - start)
	else:
		print 'Usage: ...'
    
# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
	main()
