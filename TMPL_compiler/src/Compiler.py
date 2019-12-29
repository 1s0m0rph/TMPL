"""
Given abstract syntax from parser, compile down into bytecode
"""

from typing import Set

import numpy as np
from Syntax import *

FIELD_DELIM = '00011111'	#read as utf 8 char 32 (unit separator)
START = -1					#in 2's complement, -1, or all 1s
ACCEPT = -2					#in 2's complement, -2, or all 1s except the lowest bit
REJECT = -3
BLANK = -1					#in 2's complement
LEFT_ENDMARKER = -2
RIGHT_ENDMARKER = -3
MOVE_LEFT = 0
MOVE_RIGHT = 1

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
Abstract representation of a TM with functions to build it up incrementally
"""
class TM:

	BEGIN_MARKER = '>'
	END_MARKER = '<'
	BLANK_CHAR = '_'

	def __init__(self,alphabet:Set[str],tape_alphabet:Set[str]):
		self.alphabet = alphabet
		self.tape_alphabet = tape_alphabet.union(alphabet)
		self.tape_alphabet = self.tape_alphabet.union({self.BEGIN_MARKER,self.END_MARKER,self.BLANK_CHAR})
		self.transition_function = {START:{},
									ACCEPT:{c:(ACCEPT,self.BLANK_CHAR,MOVE_RIGHT) for c in self.tape_alphabet},
									REJECT:{c:(REJECT,self.BLANK_CHAR,MOVE_RIGHT) for c in self.tape_alphabet}
									}#maps states onto maps from symbols to transition tuples (to state,write symbol,direction)

		#logical stuff
		self.current_state = START#this is q in the semantics description
		self.TF_assoc = {}#points from an input boolean node to its dummy T/F nodes (list with 0 being false, 1 being true)

		self.next_state_counter = 0	#what is the index of the next state to be added?

	def get_next_state(self):
		self.transition_function.update({self.next_state_counter:{}})
		self.next_state_counter += 1
		return self.next_state_counter - 1

	'''
	Add a new state such that there is no movement going into state p; return that state
	'''
	def add_nomov(self,p: int):
		nstate = self.get_next_state()
		self.transition_function[nstate] = {c:(p,c,MOVE_LEFT) for c in self.tape_alphabet}
		return nstate

	def get_TF_from_dummy(self,p:int):
		dummyF,dummyT = self.TF_assoc[p]
		T = self.transition_function[dummyT][self.BLANK_CHAR][0]
		F = self.transition_function[dummyF][self.BLANK_CHAR][0]
		return T,F

	def add_conditional(self,bexpr:BooleanExpr):
		cond_body_start = self.get_next_state()	#this is the body of the conditional
		cond_body_start_dummy = self.add_nomov(cond_body_start)
		cond_after = self.get_next_state()		#this is the statement immediately after (where both false and the last statement in the conditional go)
		cond_after_dummy = self.add_nomov(cond_after)
		self.add_boolean(bexpr)
		T,F = self.get_TF_from_dummy(self.current_state)

		self.transition_function[T] = {c:(cond_body_start_dummy,c,MOVE_RIGHT) for c in self.tape_alphabet}
		self.transition_function[F] = {c:(cond_after_dummy,c,MOVE_RIGHT) for c in self.tape_alphabet}

		return cond_body_start,cond_after

	'''
	Make the current state a movement one
	'''
	def add_movement(self,dir:MovementExpr):
		p = self.get_next_state()
		#all transitions write nothing and move in that dir
		mvd = MOVE_LEFT if type(dir) == MovementLeft else MOVE_RIGHT
		self.transition_function[self.current_state] = {c:(p,c,mvd) for c in self.tape_alphabet}

		return p

	def add_scan(self,dir:MovementExpr,bexpr:BooleanExpr):
		mvd = MOVE_LEFT if type(dir) == MovementLeft else MOVE_RIGHT
		boolean_entry_state = self.get_next_state()
		boolean_entry_state_dummy = self.add_nomov(boolean_entry_state)
		self.transition_function[self.current_state] = {c:(boolean_entry_state_dummy,c,MOVE_RIGHT) for c in self.tape_alphabet}

		this_state = self.current_state
		self.current_state = boolean_entry_state
		self.add_boolean(bexpr)
		self.current_state = this_state

		T,F = self.get_TF_from_dummy(boolean_entry_state)

		scan_complete = self.get_next_state()
		scan_complete_dummy = self.add_nomov(scan_complete)

		self.transition_function[T] = {c:(scan_complete_dummy,c,MOVE_RIGHT) for c in self.tape_alphabet}
		self.transition_function[F] = {c:(self.current_state,c,mvd) for c in self.tape_alphabet}
		#except for END/BEGIN, which are different
		if mvd == MOVE_LEFT:
			#then the begin transition needs to reject
			self.transition_function[F].update({self.BEGIN_MARKER:REJECT})
		else:
			self.transition_function[F].update({self.END_MARKER:REJECT})

		return scan_complete

	def add_write(self,sym:str):
		assert(sym in self.tape_alphabet)
		p = self.get_next_state()
		dummy = self.add_nomov(p)#this actually acts like p for us, but p actually is p
		self.transition_function[self.current_state] = {c:(dummy,sym,MOVE_RIGHT) for c in self.tape_alphabet}

		return p

	'''
	Cause this state to go immediately to p, no questions asked
	'''
	def add_goto(self,p:int):
		assert(p in self.transition_function)
		dummy = self.add_nomov(p)
		self.transition_function[self.current_state] = {c:(dummy,c,MOVE_RIGHT) for c in self.tape_alphabet}

		return p#TODO: what should the current state be after a goto statement?

	def add_accept(self):
		self.transition_function[self.current_state] = {c:(ACCEPT,c,MOVE_RIGHT) for c in self.tape_alphabet}

	def add_reject(self):
		self.transition_function[self.current_state] = {c:(REJECT,c,MOVE_RIGHT) for c in self.tape_alphabet}

	"""
	Now for the boolean parsing
	
	all of these require as input their true state and their false state (rather, the dummy state that leads there with no movement)
	"""

	def add_boolean(self,bexpr:BooleanExpr):
		T = self.get_next_state()
		F = self.get_next_state()
		dummyT = self.add_nomov(T)
		dummyF = self.add_nomov(F)
		#associate the current state with these
		self.TF_assoc.update({self.current_state : (dummyF,dummyT)})
		#evaluate this expr
		if type(bexpr) == Equal:
			self.add_boolean_equal(bexpr.subExpr[0].string,dummyT,dummyF)
		elif type(bexpr) == NotEqual:
			self.add_boolean_notequal(bexpr.subExpr[0].string,dummyT,dummyF)
		elif type(bexpr) == Begin:
			self.add_boolean_begin(dummyT,dummyF)
		elif type(bexpr) == End:
			self.add_boolean_end(dummyT,dummyF)
		elif type(bexpr) == BooleanTrue:
			self.add_boolean_true(dummyT,dummyF)
		elif type(bexpr) == BooleanFalse:
			self.add_boolean_false(dummyT,dummyF)
		elif type(bexpr) == BooleanNotExpr:
			this_state = self.current_state
			substate = self.get_next_state()
			self.current_state = substate
			self.add_boolean(bexpr.subExpr[0])
			self.current_state = this_state
			self.add_boolean_not(dummyT,dummyF,substate)
		elif type(bexpr) == BooleanOrExpr:
			this_state = self.current_state
			substates = []
			for subexp in bexpr.subExpr:
				substates.append(self.get_next_state())
				self.current_state = substates[-1]
				self.add_boolean(subexp)
				self.current_state = this_state

			self.add_boolean_or(dummyT,dummyF,substates)
		elif type(bexpr) == BooleanAndExpr:
			this_state = self.current_state
			substates = []
			for subexp in bexpr.subExpr:
				substates.append(self.get_next_state())
				self.current_state = substates[-1]
				self.add_boolean(subexp)
				self.current_state = this_state

			self.add_boolean_and(dummyT,dummyF,substates)
		else:
			raise SyntaxError("Unkown boolean expression type: " + str(type(bexpr)))


	def add_boolean_equal(self,sym:str,dummyT:int,dummyF:int):
		self.transition_function[self.current_state] = {c:(dummyF,c,MOVE_RIGHT) for c in self.tape_alphabet}
		self.transition_function[self.current_state].update({sym:(dummyT,sym,MOVE_RIGHT)})

	def add_boolean_notequal(self,sym:str,dummyT:int,dummyF:int):
		self.transition_function[self.current_state] = {c:(dummyT,c,MOVE_RIGHT) for c in self.tape_alphabet}
		self.transition_function[self.current_state].update({sym:(dummyF,sym,MOVE_RIGHT)})

	def add_boolean_begin(self,dummyT:int,dummyF:int):
		self.transition_function[self.current_state] = {c:(dummyF,c,MOVE_RIGHT) for c in self.tape_alphabet}
		self.transition_function[self.current_state].update({self.BEGIN_MARKER:(dummyT,self.BEGIN_MARKER,MOVE_RIGHT)})

	def add_boolean_end(self,dummyT:int,dummyF:int):
		self.transition_function[self.current_state] = {c:(dummyF,c,MOVE_RIGHT) for c in self.tape_alphabet}
		self.transition_function[self.current_state].update({self.END_MARKER:(dummyT,self.END_MARKER,MOVE_RIGHT)})

	def add_boolean_true(self,dummyT:int,dummyF:int):
		self.transition_function[self.current_state] = {c:(dummyT,c,MOVE_RIGHT) for c in self.tape_alphabet}

	def add_boolean_false(self,dummyT:int,dummyF:int):
		self.transition_function[self.current_state] = {c:(dummyF,c,MOVE_RIGHT) for c in self.tape_alphabet}

	def add_boolean_not(self,dummyT:int,dummyF:int,src:int):
		src_dummy = self.add_nomov(src)
		self.transition_function[self.current_state] = {c:(src_dummy,c,MOVE_RIGHT) for c in self.tape_alphabet}

		src_T,src_F = self.get_TF_from_dummy(src)
		self.transition_function[src_T] = {c:(dummyF,c,MOVE_RIGHT) for c in self.tape_alphabet}
		self.transition_function[src_F] = {c:(dummyT,c,MOVE_RIGHT) for c in self.tape_alphabet}

	def add_boolean_or(self,dummyT:int,dummyF:int,srcs:List[int]):
		#add the entry point in
		src_dummy = self.add_nomov(srcs[0])
		self.transition_function[self.current_state] = {c:(src_dummy,c,MOVE_RIGHT) for c in self.tape_alphabet}

		for i,src in enumerate(srcs):
			src_dummyF, src_dummyT = self.TF_assoc[src]
			src_T = self.transition_function[src_dummyT][self.BLANK_CHAR][0]#all transitions go to this node, so we'll just use the blank transition
			src_F = self.transition_function[src_dummyF][self.BLANK_CHAR][0]

			self.transition_function[src_T] = {c:(dummyT,c,MOVE_RIGHT) for c in self.tape_alphabet}
			if i == len(srcs) - 1:
				#then this needs to go to F
				self.transition_function[src_F] = {c:(dummyF,c,MOVE_RIGHT) for c in self.tape_alphabet}
			else:
				#then chain it along to the next one's dummy state
				src_dummy = self.add_nomov(srcs[i+1])
				self.transition_function[src_F] = {c:(src_dummy,c,MOVE_RIGHT) for c in self.tape_alphabet}

	def add_boolean_and(self,dummyT:int,dummyF:int,srcs:List[int]):
		#add the entry point in
		src_dummy = self.add_nomov(srcs[0])
		self.transition_function[self.current_state] = {c:(src_dummy,c,MOVE_RIGHT) for c in self.tape_alphabet}

		for i,src in enumerate(srcs):
			src_dummyF,src_dummyT = self.TF_assoc[src]
			src_T = self.transition_function[src_dummyT][self.BLANK_CHAR][0]  #all transitions go to this node, so we'll just use the blank transition
			src_F = self.transition_function[src_dummyF][self.BLANK_CHAR][0]

			self.transition_function[src_F] = {c:(dummyF,c,MOVE_RIGHT) for c in self.tape_alphabet}
			if i == len(srcs)-1:
				#then this needs to go to T
				self.transition_function[src_T] = {c:(dummyT,c,MOVE_RIGHT) for c in self.tape_alphabet}
			else:
				#then chain it along to the next one's dummy state
				src_dummy = self.add_nomov(srcs[i+1])
				self.transition_function[src_T] = {c:(src_dummy,c,MOVE_RIGHT) for c in self.tape_alphabet}


	"""
	Code for simulating this TM (mostly for debugging purposes, but the effect is that this language is effectively runnable interpreted)
	"""

	'''
	nsteps allows the TM to be simulated for only a certain number of steps
	ret_config set to true means that simulate will return the full current TM config as opposed to a simple 'yes' or 'no'
	'''
	def simulate(self,inp:str,verbose=False,include_endmarker=True,nsteps=-1,ret_config=False):
		def end_check(current_state,step_count):
			if nsteps != -1:
				if step_count >= nsteps:
					return False

			return current_state not in [ACCEPT,REJECT]

		if include_endmarker:
			tape = list(self.BEGIN_MARKER + inp + self.END_MARKER)#list because it's easier
		else:
			tape = list(self.BEGIN_MARKER + inp + self.BLANK_CHAR)  #list because it's easier
		read_head_loc = 1	#index on the tape
		current_state = START

		step_count = 0
		while end_check(current_state,step_count):
			read_symbol = tape[read_head_loc]
			to_state,write_sym,dir = self.transition_function[current_state][read_symbol]
			tape[read_head_loc] = write_sym
			if dir == MOVE_LEFT:
				read_head_loc = max(0,read_head_loc-1)
			else:
				read_head_loc += 1
				#maybe add a blank
				if read_head_loc >= len(tape):
					tape.append(self.BLANK_CHAR)

			if verbose:
				print(''.join(tape))
				print(' '*read_head_loc + '^')

			current_state = to_state
			step_count += 1

		if ret_config:
			return tape,read_head_loc,current_state
		else:
			return current_state == ACCEPT


class Compiler:

	def __init__(self):
		pass

	#TODO: first thing we need to do is handle labels since prereferencing is allowed