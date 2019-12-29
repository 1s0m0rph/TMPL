from unittest import TestCase

from Compiler import *
from Parser import *

class TestCompiler(TestCase):
	p = Parser("""ab
	:entry
	(== 'aR') or (== 'bR')
		L
		goto equality
	== 'a'
		write 'aL' R
	== 'b'
		write 'bL' R
	scan R until (end) or (== 'aR') or (== 'bR')
	L
	== 'a'
		write 'aR' L
	== 'b'
		write 'aR' L
	scan L until (== 'aL') or (== 'bL')
	R
	goto entry

	:equality
	== 'aL'
		write _ R
		scan R until (end) or (== 'aR') or (== 'bR')
		== 'aR'
			write _ L
			scan L until (== 'aL') or (== 'bL')
			goto equality
		end
			accept
		reject
	== 'bL'
		write _ R
		scan R until (begin) or (== 'aR') or (== 'bR')
		== 'bR'
			write _ L
			scan L until (== 'aL') or (== 'bL')
			goto equality
		begin
			accept
		reject
	accept""".split('\n'))

	def test_infer_tape_alphabet_extra(self):
		ast = self.p.parse_all()
		c = Compiler(ast)
		res = c.infer_tape_alphabet_extra()
		assert({'a','b','aR','aL','bL','_'}.issubset(res))

	def test_compile_remaining_gotos(self):
		self.fail()

	def test_compile_line(self):
		self.fail()

	def test_create_TM_from_bytecode(self):
		self.fail()
