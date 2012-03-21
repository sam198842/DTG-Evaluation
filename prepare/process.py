# Copyright 2012 UCLA
# Weizhe Shi sam198842@gmail.com
# Bin Bi
# 1/18/2012

"""
Preprocess of the delicious files and prepare for LDA-c
"""

import sys
import re
import time
from os import path

class Scanner(object):
	def __init__(self, out_dir):
		self.tag_dict = {}
		self.out_dir = out_dir
		self.f_data = None
		self.f_vocab = None
		self.filename_data = 'data'
		self.filename_vocab = 'vocab'
		
	def openFiles(self):
		if not path.exists(self.out_dir):
			print "Dir: %s doesn't exist" % out_dir
			return False
		try:
			self.f_data = open(path.join(self.out_dir, self.filename_data), 'w')
			self.f_vocab = open(path.join(self.out_dir, self.filename_vocab), 'w')
			return True
		except IOError:
			print 'Error opening the output files'
			return False

	def closeFiles(self):
		try:
			self.f_data.close()
			self.f_vocab.close()
		except AttributeError:
			print 'Files not opened when trying to close'
			
	def writeDat(self, tagIds):
		line = str(len(tagIds)) + ' ' + ':1 '.join(tagIds) + ':1\n'
		self.f_data.write(line)
		
	def writeVocab(self):
		for tag in sorted(self.tag_dict, key = self.tag_dict.get):
			self.f_vocab.write(tag + '\n')
		
	def scan(self, filename):
		if not self.openFiles():
			return False

		try:
			f = open(filename, 'r')
		except IOError:
			print 'Error opening file: %s' % filename
			return

		print "\nStart processing: ('.' means 100k lines)"

		tag_cnt = 0
		doc_cnt = 0
		for line in f:
			if doc_cnt % 100000 == 0:
				print '.',
			doc_cnt += 1
			
			row = list()
			tokens = line.split()
			for tag in tokens[1:]:
				# add new tag into dict
				if tag not in self.tag_dict:
					self.tag_dict[tag] = tag_cnt
					tag_cnt += 1
				row.append(str(self.tag_dict[tag]))
			
			self.writeDat(row)
			del row
		
		print '\nFinish processing the data.\n'
		print 'doc_cnt: %d' % doc_cnt
		print 'tag_dict: %d' % len(self.tag_dict)
		print 'tag_cnt: %d' % tag_cnt
    
		# write the vocab (tags) file
		self.writeVocab()
		self.closeFiles()


# Entry point
def main():
	# Get the name from the command line
	if len(sys.argv) >= 3:
		argv_file = sys.argv[1]
		argv_dir = sys.argv[2]

		start = time.time()
		scanner = Scanner(argv_dir)
		scanner.scan(argv_file)
		print 'Cost %.03f sec' % (time.time() - start)
		
	else:
		print 'Usage: python process.py filename directory'
    
# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
	main()
