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

		#now tests on partial runs (this allows us to test that certain state configurations work how we expect them to)

		assert(machine.simulate('abc',include_endmarker=False,nsteps=1,ret_config=True) == (['>','a','b','c','_'],2,-1))
		assert(machine.simulate('a',include_endmarker=False,nsteps=2,ret_config=True) == (['>','a','<'],1,3))
		assert(machine.simulate('abc',include_endmarker=False,nsteps=5,ret_config=True) == (['>','a','b','_','<'],2,4))

	def test_add_movement(self):
		machine = TM({'a'},set())
		machine.add_movement(MovementRight())

		#one step on this machine should result in just going right once
		assert(machine.simulate('aa',nsteps=1,ret_config=True) == (['>','a','a','<'],2,0))

		machine.current_state = 0
		machine.add_movement(MovementLeft())

		#two steps should now result in being back at the start

		assert(machine.simulate('aa',nsteps=2,ret_config=True) == (['>','a','a','<'],1,1))

		machine.current_state = 1
		machine.add_movement(MovementLeft())

		#three should have us at the left endmarker
		assert(machine.simulate('aa',nsteps=3,ret_config=True) == (['>','a','a','<'],0,2))


	def test_add_scan(self):
		machine = TM({'a','b'},set())
		eqb = Equal(String('b'))
		machine.add_scan(MovementRight(),eqb)

		#this should scan right until we hit the first b
		_,pos,_ = machine.simulate('aaabbb',nsteps=21,ret_config=True)
		assert(pos == 4)

	def test_add_write(self):
		machine = TM({'a','b'},set())
		machine.add_write('a')

		tape,pos,_ = machine.simulate('ba',nsteps=2,ret_config=True)
		assert(tape == ['>','a','a','<'])
		assert(pos == 1)

	def test_add_goto(self):
		machine = TM({'a','b'},set())
		machine.current_state = machine.add_movement(MovementRight())
		machine.add_goto(-1)#trivial loop

		_,pos,state = machine.simulate('ab',nsteps=3,ret_config=True)#3 steps since there's a dummy
		assert(pos == 2)
		assert(state == -1)

	def test_add_accept(self):
		machine = TM({'a','b'},set())
		machine.add_accept()#accepts sigma* optimally

		assert(machine.simulate('aababbababbababab'))
		assert(machine.simulate(''))

	def test_add_reject(self):
		machine = TM({'a','b'},set())
		machine.add_reject()  #accepts {} optimally

		assert(not machine.simulate('aababbababbababab'))
		assert(not machine.simulate(''))

	def test_add_boolean(self):
		machine = TM({'a','b'},set())
		#let the start state be the entry state
		bexpr = BooleanNotExpr(BooleanOrExpr([BooleanAndExpr([NotEqual(String('b')),Equal(String('a'))]),End()]))#not ((!='b' and =='a') or end)
		machine.add_boolean(bexpr)
		T,F = machine.get_TF_from_dummy(-1)

		_,_,state = machine.simulate('b',nsteps=18,ret_config=True)
		assert(state == T)

		_,_,state = machine.simulate('',nsteps=22,ret_config=True)
		assert(state == F)

		_,_,state = machine.simulate('a',nsteps=18,ret_config=True)
		assert(state == F)

	def test_add_boolean_equal(self):
		machine = TM({'a','b'},set())
		#let the start state be the entry state
		T = machine.get_next_state()
		F = machine.get_next_state()
		dummyT = machine.add_nomov(T)
		dummyF = machine.add_nomov(F)
		machine.add_boolean_equal('b',dummyT,dummyF)

		_,pos,state = machine.simulate('b',nsteps=2,ret_config=True)#2 steps, one to go to the dummy and one to go back
		assert(state == T)
		assert(pos == 1)

		_,pos,state = machine.simulate('a',nsteps=2,ret_config=True)
		assert(state == F)
		assert(pos == 1)

	def test_add_boolean_notequal(self):
		machine = TM({'a','b'},set())
		#let the start state be the entry state
		T = machine.get_next_state()
		F = machine.get_next_state()
		dummyT = machine.add_nomov(T)
		dummyF = machine.add_nomov(F)
		machine.add_boolean_notequal('b',dummyT,dummyF)

		_,pos,state = machine.simulate('b',nsteps=2,ret_config=True)
		assert(state == F)
		assert(pos == 1)

		_,pos,state = machine.simulate('a',nsteps=2,ret_config=True)
		assert(state == T)
		assert(pos == 1)

	def test_add_boolean_begin(self):
		machine = TM({'a','b'},set())
		#let the start state be the entry state
		T = machine.get_next_state()
		F = machine.get_next_state()
		dummyT = machine.add_nomov(T)
		dummyF = machine.add_nomov(F)
		machine.add_boolean_begin(dummyT,dummyF)

		_,pos,state = machine.simulate('b',nsteps=2,ret_config=True)
		assert(state == F)
		assert(pos == 1)

		#do it again with a movement left so we can actually see a success
		machine = TM({'a','b'},set())
		T = machine.get_next_state()
		F = machine.get_next_state()
		dummyT = machine.add_nomov(T)
		dummyF = machine.add_nomov(F)
		machine.current_state = machine.add_movement(MovementLeft())
		machine.add_boolean_begin(dummyT,dummyF)

		_,pos,state = machine.simulate('a',nsteps=3,ret_config=True)
		assert(state == T)
		assert(pos == 0)

	def test_add_boolean_end(self):
		machine = TM({'a','b'},set())
		#let the start state be the entry state
		T = machine.get_next_state()
		F = machine.get_next_state()
		dummyT = machine.add_nomov(T)
		dummyF = machine.add_nomov(F)
		machine.add_boolean_end(dummyT,dummyF)

		_,pos,state = machine.simulate('b',nsteps=2,ret_config=True)
		assert(state == F)
		assert(pos == 1)

		#do it again with a movement right so we can actually see a success
		machine = TM({'a','b'},set())
		T = machine.get_next_state()
		F = machine.get_next_state()
		dummyT = machine.add_nomov(T)
		dummyF = machine.add_nomov(F)
		machine.current_state = machine.add_movement(MovementRight())
		machine.add_boolean_end(dummyT,dummyF)

		_,pos,state = machine.simulate('a',nsteps=3,ret_config=True)
		assert(state == T)
		assert(pos == 2)

	def test_add_boolean_not(self):
		machine = TM({'a','b'},set())
		entry = machine.get_next_state()
		machine.current_state = entry
		src_T = machine.get_next_state()
		src_F = machine.get_next_state()
		src_dummyT = machine.add_nomov(src_T)
		src_dummyF = machine.add_nomov(src_F)
		machine.add_boolean_equal('b',src_dummyT,src_dummyF)
		machine.TF_assoc.update({entry:(src_dummyF,src_dummyT)})

		machine.current_state = -1
		T = machine.get_next_state()
		F = machine.get_next_state()
		dummyT = machine.add_nomov(T)
		dummyF = machine.add_nomov(F)

		machine.add_boolean_not(dummyT,dummyF,entry)

		_,pos,state = machine.simulate('b',nsteps=6,ret_config=True)
		assert(state == F)
		assert(pos == 1)

		_,pos,state = machine.simulate('a',nsteps=6,ret_config=True)
		assert(state == T)
		assert(pos == 1)

	def test_add_boolean_or(self):
		machine = TM({'a','b'},set())
		entry0 = machine.get_next_state()
		machine.current_state = entry0
		src_T0 = machine.get_next_state()
		src_F0 = machine.get_next_state()
		src_dummyT0 = machine.add_nomov(src_T0)
		src_dummyF0 = machine.add_nomov(src_F0)
		machine.add_boolean_equal('b',src_dummyT0,src_dummyF0)
		machine.TF_assoc.update({entry0:(src_dummyF0,src_dummyT0)})
		entry1 = machine.get_next_state()
		machine.current_state = entry1
		src_T1 = machine.get_next_state()
		src_F1 = machine.get_next_state()
		src_dummyT1 = machine.add_nomov(src_T1)
		src_dummyF1 = machine.add_nomov(src_F1)
		machine.add_boolean_end(src_dummyT1,src_dummyF1)
		machine.TF_assoc.update({entry1:(src_dummyF1,src_dummyT1)})

		machine.current_state = START
		T = machine.get_next_state()
		F = machine.get_next_state()
		dummyT = machine.add_nomov(T)
		dummyF = machine.add_nomov(F)

		machine.add_boolean_or(dummyT,dummyF,[entry0,entry1])

		_,pos,state = machine.simulate('b',nsteps=6,ret_config=True)
		assert(state == T)
		assert(pos == 1)

		_,pos,state = machine.simulate('',nsteps=10,ret_config=True)
		assert(state == T)
		assert(pos == 1)

		_,pos,state = machine.simulate('a',nsteps=10,ret_config=True)
		assert(state == F)
		assert(pos == 1)

	def test_add_boolean_and(self):
		machine = TM({'a','b'},set())
		entry0 = machine.get_next_state()
		machine.current_state = entry0
		src_T0 = machine.get_next_state()
		src_F0 = machine.get_next_state()
		src_dummyT0 = machine.add_nomov(src_T0)
		src_dummyF0 = machine.add_nomov(src_F0)
		machine.add_boolean_equal('b',src_dummyT0,src_dummyF0)
		machine.TF_assoc.update({entry0:(src_dummyF0,src_dummyT0)})
		entry1 = machine.get_next_state()
		machine.current_state = entry1
		src_T1 = machine.get_next_state()
		src_F1 = machine.get_next_state()
		src_dummyT1 = machine.add_nomov(src_T1)
		src_dummyF1 = machine.add_nomov(src_F1)
		machine.add_boolean_notequal('a',src_dummyT1,src_dummyF1)#kinda dumb but it works
		machine.TF_assoc.update({entry1:(src_dummyF1,src_dummyT1)})

		machine.current_state = START
		T = machine.get_next_state()
		F = machine.get_next_state()
		dummyT = machine.add_nomov(T)
		dummyF = machine.add_nomov(F)

		machine.add_boolean_and(dummyT,dummyF,[entry0,entry1])

		_,pos,state = machine.simulate('b',nsteps=10,ret_config=True)
		assert(state == T)
		assert(pos == 1)

		_,pos,state = machine.simulate('',nsteps=6,ret_config=True)
		assert(state == F)
		assert(pos == 1)

		_,pos,state = machine.simulate('a',nsteps=6,ret_config=True)
		assert(state == F)
		assert(pos == 1)
