from unittest import TestCase

from Compiler import *
from Parser import *

class TestCompiler(TestCase):


	def test_infer_tape_alphabet_extra(self):
		prog = """ab
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
				write 'bR' L
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
			accept""".split('\n')
		p = Parser(prog)
		ast = p.parse_all()
		c = Compiler(ast)
		res = c.infer_tape_alphabet_extra()
		assert({'a','b','aR','aL','bR','bL','_'} == res)

	def test_discover_gotos(self):
		prog = """ab
				:begin
				=='a'
					goto begin	#prelabeled goto
				R
				== 'b'
					goto after	#postlabeled
				accept
				:after
				reject""".split("\n")
		ast = Parser(prog).parse_all()

		c = Compiler(ast)
		c.M = TM({'a','b'},set())
		c.discover_gotos()

		#should have 2 gotos discovered
		assert(c.remaining_gotos.keys() == {ast[2].subExpr[0],ast[4].subExpr[0]})

	def test_compile_line(self):
		#the only complicated ones are conditionals, gotos, and labels
		prog = """ab
		:begin
		=='a'
			goto begin
		accept""".split("\n")
		ast = Parser(prog).parse_all()

		#this should be a trivial loop iff the first char is an a, else accepted
		c = Compiler(ast)
		c.M = TM({'a','b'},set())
		c.discover_gotos()#need this for the label to work

		c.compile_line(ast[1])
		#the start state should be labeled with begin
		assert(c.labels['begin'] == -1)

		c.compile_line(ast[2])
		#this should do both the conditional entry line and the line within it, but not the accept
		#we should see this goto not being there
		assert(len(c.remaining_gotos) == 0)

		#go ahead and compile that accept line so the c.M is complete
		c.compile_line(ast[3])
		for state in range(-3,len(c.M.transition_function)-3):
			if state not in c.M.transition_function:
				assert False
			for sym in c.M.tape_alphabet:
				if sym not in c.M.transition_function[state]:
					assert False

		#now simulate for the rest of the tests
		#it should accept any string not starting with an a
		assert(c.M.simulate(''))
		assert(c.M.simulate('b'))
		assert(c.M.simulate('ba'))

		#and it should loop if it starts with an a
		initial = (['>','a','b','<'],1,-1)
		back_to_start = False
		for nsteps in range(1,20):
			result = c.M.simulate('ab',nsteps=nsteps,ret_config=True)
			if result == initial:
				back_to_start = True

		assert back_to_start

	def test_compile_to_TM(self):
		prog = """abc
		end
			accept
		!='a'
			reject
		scan R until =='b'	#match pattern a*b*c*
		scan R until =='c'
		scan R until end
		:clear
		scan L until begin
		scan R until =='a'	#move to the first a
		write _ R
		scan R until =='b'
		write _ R
		scan R until =='c'
		write _ R
		end
			L				#move past the right endmarker
			scan L until != _
			begin
				accept
			reject
		goto clear""".split('\n')
		#this should be a^nb^nc^n ^^^^
		p = Parser(prog)
		ast = p.parse_all()
		c = Compiler(ast)
		c.compile_to_TM()

		assert(c.M.simulate(''))
		assert(c.M.simulate('abc'))
		assert(c.M.simulate('aaabbbccc'))
		assert(c.M.simulate('aaaaaaaabbbbbbbbcccccccc'))
		assert(not c.M.simulate('a'))
		assert(not c.M.simulate('b'))
		assert(not c.M.simulate('c'))
		assert(not c.M.simulate('ab'))
		assert(not c.M.simulate('ac'))
		assert(not c.M.simulate('aaaaaaaabbbbbbbcccccccc'))
		assert(not c.M.simulate('abab'))
		assert(not c.M.simulate('abbccbabc'))
