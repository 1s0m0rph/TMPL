from unittest import TestCase

from Compiler import *

class TestMiscUtils(TestCase):

	def test_int_to_binstr(self):
		assert(int_to_binstr(-1,1) == '1')
		assert(int_to_binstr(-2,2) == '10')
		assert(int_to_binstr(1,2) == '01')
		assert(int_to_binstr(-4,3) == '100')
		assert(int_to_binstr(-1,5) == '11111')
		assert(int_to_binstr(5,4) == '0101')
		self.assertRaises(AttributeError,int_to_binstr,1,1)
		self.assertRaises(AttributeError,int_to_binstr,5,3)

	def test_complement_binstr(self):
		assert(complement_binstr('0010') == '1101')
		assert(complement_binstr('100100100') == '011011011')

	def test_increment_binstr(self):
		assert(increment_binstr('1') == '10')
		assert(increment_binstr('01') == '10')
		assert(increment_binstr('1101') == '1110')
		assert(increment_binstr('0') == '1')
