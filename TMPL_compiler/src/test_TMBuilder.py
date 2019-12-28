from unittest import TestCase

from Compiler import *

class TestTMBuilder(TestCase):

	def test_simulate(self):#this is how we're going to test it; by just simulating its output for known machines
		verbose = False
		#test on the machine from kozen, pg 212, accepting a^nb^nc^n
		machine = TM({'a','b','c'},set())
		machine.get_next_state()	#eat the 0-state so our numbers line up with the ones in the table
		tf_as_table = [
			[(START,TM.BEGIN_MARKER,MOVE_RIGHT),(START,'a',MOVE_RIGHT),(1,'b',MOVE_RIGHT),(2,'c',MOVE_RIGHT),(3,TM.END_MARKER,MOVE_LEFT),(REJECT,TM.BLANK_CHAR,MOVE_RIGHT)],
			[(REJECT,TM.BLANK_CHAR,MOVE_RIGHT),(REJECT,TM.BLANK_CHAR,MOVE_RIGHT),(1,'b',MOVE_RIGHT),(2,'c',MOVE_RIGHT),(3,TM.END_MARKER,MOVE_LEFT),(REJECT,TM.BLANK_CHAR,MOVE_RIGHT)],
			[(REJECT,TM.BLANK_CHAR,MOVE_RIGHT),(REJECT,TM.BLANK_CHAR,MOVE_RIGHT),(REJECT,TM.BLANK_CHAR,MOVE_RIGHT),(2,'c',MOVE_RIGHT),(3,TM.END_MARKER,MOVE_LEFT),(REJECT,TM.BLANK_CHAR,MOVE_RIGHT)],
			[(ACCEPT,TM.BLANK_CHAR,MOVE_RIGHT),(REJECT,TM.BLANK_CHAR,MOVE_RIGHT),(REJECT,TM.BLANK_CHAR,MOVE_RIGHT),(4,TM.BLANK_CHAR,MOVE_LEFT),(3,TM.BLANK_CHAR,MOVE_LEFT),(REJECT,TM.BLANK_CHAR,MOVE_RIGHT)],
			[(REJECT,TM.BLANK_CHAR,MOVE_RIGHT),(REJECT,TM.BLANK_CHAR,MOVE_RIGHT),(5,TM.BLANK_CHAR,MOVE_LEFT),(4,'c',MOVE_LEFT),(4,TM.BLANK_CHAR,MOVE_LEFT),(REJECT,TM.BLANK_CHAR,MOVE_RIGHT)],
			[(REJECT,TM.BLANK_CHAR,MOVE_RIGHT),(6,TM.BLANK_CHAR,MOVE_LEFT),(5,'b',MOVE_LEFT),(REJECT,TM.BLANK_CHAR,MOVE_RIGHT),(5,TM.BLANK_CHAR,MOVE_LEFT),(REJECT,TM.BLANK_CHAR,MOVE_RIGHT)],
			[(7,TM.BEGIN_MARKER,MOVE_RIGHT),(6,'a',MOVE_LEFT),(REJECT,TM.BLANK_CHAR,MOVE_RIGHT),(REJECT,TM.BLANK_CHAR,MOVE_RIGHT),(6,TM.BLANK_CHAR,MOVE_LEFT),(REJECT,TM.BLANK_CHAR,MOVE_RIGHT)],
			[(REJECT,TM.BLANK_CHAR,MOVE_RIGHT),(8,TM.BLANK_CHAR,MOVE_RIGHT),(REJECT,TM.BLANK_CHAR,MOVE_RIGHT),(REJECT,TM.BLANK_CHAR,MOVE_RIGHT),(7,TM.BLANK_CHAR,MOVE_RIGHT),(ACCEPT,TM.BLANK_CHAR,MOVE_RIGHT)],
			[(REJECT,TM.BLANK_CHAR,MOVE_RIGHT),(8,'a',MOVE_RIGHT),(9,TM.BLANK_CHAR,MOVE_RIGHT),(REJECT,TM.BLANK_CHAR,MOVE_RIGHT),(8,TM.BLANK_CHAR,MOVE_RIGHT),(REJECT,TM.BLANK_CHAR,MOVE_RIGHT)],
			[(REJECT,TM.BLANK_CHAR,MOVE_RIGHT),(REJECT,TM.BLANK_CHAR,MOVE_RIGHT),(9,'b',MOVE_RIGHT),(10,TM.BLANK_CHAR,MOVE_RIGHT),(9,TM.BLANK_CHAR,MOVE_RIGHT),(REJECT,TM.BLANK_CHAR,MOVE_RIGHT)],
			[(REJECT,TM.BLANK_CHAR,MOVE_RIGHT),(REJECT,TM.BLANK_CHAR,MOVE_RIGHT),(REJECT,TM.BLANK_CHAR,MOVE_RIGHT),(10,'c',MOVE_RIGHT),(10,TM.BLANK_CHAR,MOVE_RIGHT),(3,TM.END_MARKER,MOVE_LEFT)]
		]
		for _ in range(10):
			machine.get_next_state()

		for i,state in enumerate([START] + list(range(1,11))):
			for j,sym in enumerate([TM.BEGIN_MARKER,'a','b','c',TM.BLANK_CHAR,TM.END_MARKER]):
				machine.transition_function[state].update({sym:tf_as_table[i][j]})

		#now we *should* have a functional machine for a^nb^nc^n. make sure it works
		assert(machine.simulate('',include_endmarker=False,verbose=verbose))
		assert(machine.simulate('abc',include_endmarker=False,verbose=verbose))
		assert(machine.simulate('aaabbbccc',include_endmarker=False,verbose=verbose))
		assert(machine.simulate('aaaaaaaabbbbbbbbcccccccc',include_endmarker=False,verbose=verbose))
		assert(not machine.simulate('a',include_endmarker=False,verbose=verbose))
		assert(not machine.simulate('b',include_endmarker=False,verbose=verbose))
		assert(not machine.simulate('c',include_endmarker=False,verbose=verbose))
		assert(not machine.simulate('ab',include_endmarker=False,verbose=verbose))
		assert(not machine.simulate('ac',include_endmarker=False,verbose=verbose))
		assert(not machine.simulate('aaaaaaaabbbbbbbcccccccc',include_endmarker=False,verbose=verbose))
		assert(not machine.simulate('abab',include_endmarker=False,verbose=verbose))
		assert(not machine.simulate('abbccbabc',include_endmarker=False,verbose=verbose))


	def test_get_TF_from_dummy(self):
		self.fail()

	def test_add_conditional(self):
		self.fail()

	def test_add_movement(self):
		self.fail()

	def test_add_scan(self):
		self.fail()

	def test_add_write(self):
		self.fail()

	def test_add_goto(self):
		self.fail()

	def test_add_accept(self):
		self.fail()

	def test_add_reject(self):
		self.fail()

	def test_add_boolean(self):
		self.fail()

	def test_add_boolean_equal(self):
		self.fail()

	def test_add_boolean_notequal(self):
		self.fail()

	def test_add_boolean_begin(self):
		self.fail()

	def test_add_boolean_end(self):
		self.fail()

	def test_add_boolean_true(self):
		self.fail()

	def test_add_boolean_false(self):
		self.fail()

	def test_add_boolean_not(self):
		self.fail()

	def test_add_boolean_or(self):
		self.fail()

	def test_add_boolean_and(self):
		self.fail()
