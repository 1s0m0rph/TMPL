"""
Given abstract syntax from parser, compile down into bytecode
"""

import numpy as np
from Syntax import *

FIELD_DELIM = '00011111'	#read as utf 8 char 32 (unit separator)
ACCEPT = -1					#in 2's complement, -1, or all 1s
REJECT = -2					#in 2's complement, -2, or all 1s except the lowest bit
BLANK = -1					#in 2's complement
LEFT_ENDMARKER = -2
RIGHT_ENDMARKER = -3

def increment_binstr(bst_inp:str):
	bst = list(reversed(bst_inp))
	retstr = ''
	for i in range(len(bst)):
		if bst[i] == '1':
			retstr += '0'
		else:
			retstr = '1' + retstr
			for j in range(i+1,len(bst)):
				retstr = bst[j] + retstr
			return retstr

	return '1' + retstr#carry bit

def complement_binstr(bst:str):
	retstr = ''
	for c in bst:
		if c == '0':
			retstr += '1'
		else:
			retstr += '0'

	return retstr


'''
Convert an int to a 2's complement string of equivalent value, with given width
'''
def int_to_binstr(i:int,w:int):
	if i < 0:
		if int(np.floor(np.log2(-i) + 1)) > w:
			raise AttributeError("Width insufficient to fit entire number")
	else:
		if int(np.floor(np.log2(i) + 2)) > w:
			raise AttributeError("Width insufficient to fit entire number")

	neg_flag = False
	if i < 0:
		# x is negative
		# note that (~x) + 1 = -x
		neg_flag = True
		i = -i#we're going to undo this later
	elif i == 0:
		return '0' * w

	bst = ''
	while i > 0:
		add = i & 0b1
		bst = str(add) + bst
		i >>= 1

	#pad with zeroes at the beginning
	while len(bst) < w:
		bst = '0' + bst

	if neg_flag:
		#then take complement(bst) + 1
		bst = increment_binstr(complement_binstr(bst))

	return bst

"""
Abstract representation of a TM
"""
class TM:

	BEGIN_MARKER = '>'
	END_MARKER = '<'

	def __init__(self):

		self.alphabet = set()
		self.tape_alphabet = set()
		self.transition_function = {}#maps states onto maps from symbols to transition tuples (to state,write symbol,direction)
		self.start_state = -1#states will just be ints



class Compiler:

	def __init__(self):
		pass