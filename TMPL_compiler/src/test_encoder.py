from unittest import TestCase

from Compiler import *

class TestEncoder(TestCase):

	def test_encode_full_width_int(self):
		M = TM({'a','b'},set())
		e = Encoder(M)

		e.encode_full_width_int(0)
		assert(e.encoding == '0'*32)
		e.encoding = ''

		e.encode_full_width_int(10)
		assert(e.encoding == '0'*28 + '1010')

	def test_encode_preprocessor_ints(self):
		M = TM({'a','b'},set())
		e = Encoder(M)

		e.encode_preprocessor_ints()

		assert(e.encoding == '0'*32 + ('0'*30 + '11'))

	def test_encode_alphabets(self):
		M = TM({'a'},set())
		e = Encoder(M)

		e.encode_alphabets()

		assert(len(e.encoding) == 64)

		bytea = []
		for i in range(0,len(e.encoding),8):
			bytea.append(e.encoding[i:i+8])

		assert(bytea[0] == '01100001')
		assert(bytea[1] == FIELD_DELIM)
		remaining_symbols = {'00111100','00111110','01011111'}#respectively, <, >, and _
		assert(bytea[2] in remaining_symbols)
		remaining_symbols.remove(bytea[2])
		assert(bytea[3] == CHAR_DELIM)
		assert(bytea[4] in remaining_symbols)
		remaining_symbols.remove(bytea[4])
		assert(bytea[5] == CHAR_DELIM)
		assert(bytea[6] in remaining_symbols)
		assert(bytea[7] == FIELD_DELIM)

		#now check to make sure all the maps are looking good
		assert(len(e.symbol_index_map) == 4)
		assert(e.symbol_index_map['a'] == 0)

	def test_encode_single_transition(self):
		M = TM({'a','b'},set())
		M.transition_function[-1] = {'a':(-1,'a',1),
									 '<':(-2,'<',0),
									 '_':(-1,'a',0),
									 '>':(-3,'>',1)}
		e = Encoder(M)

		e.encode_alphabets()

		e.encode_single_transition(-1,'a')

		encoding = e.encoding[80:]

		assert(encoding in ['1110001','1110011'])

		e.encode_single_transition(-1,'>')

		encoding = e.encoding[80+len(encoding):]

		assert(encoding == '1011101')