from unittest import TestCase

from Parser import *


class TestParser(TestCase):

	def test_get_within_first_open_paren(self):
		stest = '\t\t  \t(st(ri+n)g( =!a)(())s  \tdf)\t\t (ano(ther) str(ing()))'

		p = Parser([])

		sret = p.get_within_first_open_paren(stest)

		assert(sret == '(st(ri+n)g( =!a)(())s  \tdf)')

	def test_paren(self):
		stest0 = '\t\t  \t(st(ri+n)g( =!a)(())s  \tdf)\t\t (ano(ther) str([{([]){}}]ing({})))'
		stest1 = '\t\t  \t(st(ri+n)g( =!a)(())s  \tdf)\t\t (ano(ther) str([{([]){}}]ing({}))'
		stest2 = '\t\t  \t(st(ri+n)g( =!a)(())s  \tdf)\t\t (ano(ther) str([{([]}{}}]ing({})))'
		stest3 = '\t\t  \t(st(ri+n)g( =!a)(())s ))(( \tdf)\t\t (ano(ther) str([{([]){}}]ing({})))'
		p = Parser([])

		assert(p.paren(stest0))
		assert(not p.paren(stest1))
		assert(not p.paren(stest2))
		assert(not p.paren(stest3))

	def test_get_boolstr_subexp(self):
		stest0 = "==\t'str' or == 'st2'"
		stest1 = "(true and (=='a')) or false"
		stest2 = "= = 'bR'"

		p = Parser([])

		assert(p.get_boolstr_subexp(stest0) == "==\t'str'")
		assert(p.get_boolstr_subexp(stest1) == "(true and (=='a'))")
		assert(p.get_boolstr_subexp(stest2) == stest2)

	def test_parseBoolean(self):
		stest0 = "==\t'str' or == 'st2'"
		stest1 = "(true and (=='a')) or false"
		stest2 = "!=   'b' and (!!='asdf' or end)"
		stest3 = "true or =='b' or begin or (!end)"
		stest4 = "(end) or (== 'aR') or = = 'bR'"

		p = Parser([])

		r0 = p.parseBoolean(stest0)
		r1 = p.parseBoolean(stest1)
		r2 = p.parseBoolean(stest2)
		r3 = p.parseBoolean(stest3)
		r4 = p.parseBoolean(stest4)

		assert(type(r0) == BooleanOrExpr)
		assert(type(r0.subExpr[0]) == Equal)
		assert(r0.subExpr[0].subExpr[0].string == 'str')
		assert(type(r0.subExpr[1]) == Equal)
		assert(r0.subExpr[1].subExpr[0].string == 'st2')

		assert(type(r1) == BooleanOrExpr)
		assert(type(r1.subExpr[0]) == BooleanAndExpr)
		assert(type(r1.subExpr[0].subExpr[0]) == BooleanTrue)
		assert(type(r1.subExpr[0].subExpr[1]) == Equal)
		assert(r1.subExpr[0].subExpr[1].subExpr[0].string == 'a')
		assert(type(r1.subExpr[1]) == BooleanFalse)

		assert(type(r2) == BooleanAndExpr)
		assert(type(r2.subExpr[0]) == NotEqual)
		assert(r2.subExpr[0].subExpr[0].string == 'b')
		assert(type(r2.subExpr[1]) == BooleanOrExpr)
		assert(type(r2.subExpr[1].subExpr[0]) == BooleanNotExpr)
		assert(type(r2.subExpr[1].subExpr[0].subExpr[0]) == NotEqual)
		assert(r2.subExpr[1].subExpr[0].subExpr[0].subExpr[0].string == 'asdf')
		assert(type(r2.subExpr[1].subExpr[1]) == End)

		assert(type(r3) == BooleanOrExpr)
		assert(type(r3.subExpr[0]) == BooleanTrue)
		assert(type(r3.subExpr[1]) == Equal)
		assert(r3.subExpr[1].subExpr[0].string == 'b')
		assert(type(r3.subExpr[2]) == Begin)
		assert(type(r3.subExpr[3]) == BooleanNotExpr)
		assert(type(r3.subExpr[3].subExpr[0]) == End)

		assert(type(r4) == BooleanOrExpr)

	def test_get_line_indent(self):
		stest = '\t\t  \t asdf\t\t#comment here'
		p = Parser([stest])

		assert(p.get_line_indent() == 6)

	def test_parseline(self):
		stest0 = "(== 'aR') or (== 'bR')\t\t #comment testing"
		stest1 = "\tL"
		stest2 = "\t\t   \t#this is a blank line"
		stest3 = ":begin"
		stest4 = "goto begin"
		stest5 = "\tscan R until (end) or (== 'aR') or = = 'bR'"
		stest6 = 'accept'
		stest7 = 'reject'
		stest8 = 'write _ L'

		p0 = Parser([stest0,stest1])

		res0 = p0.parseline()

		assert(type(res0) == ConditionalExpr)
		assert(type(res0.subExpr[0]) == MovementLeft)

		p1 = Parser([stest2,stest3,stest4,stest5,stest6,stest7,stest8])

		res2 = p1.parseline()
		assert(res2 is None)

		res3 = p1.parseline()
		assert(type(res3) == LabelExpr)
		assert(res3.label == 'begin')

		res4 = p1.parseline()
		assert(type(res4) == GotoExpr)
		assert(res4.ident == 'begin')

		res5 = p1.parseline()
		assert(type(res5) == Scan)
		assert(type(res5.subExpr[0]) == MovementRight)
		assert(type(res5.subExpr[1]) == BooleanOrExpr)
		assert(len(res5.subExpr[1].subExpr) == 3)

		res6 = p1.parseline()
		assert(type(res6) == Accept)

		res7 = p1.parseline()
		assert(type(res7) == Reject)

		res8 = p1.parseline()
		assert(type(res8) == WriteExpr)
		assert(type(res8.subExpr[0]) == Blank)
		assert(type(res8.subExpr[1]) == MovementLeft)

	def test_parse_all(self):
		prog = """:entry
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
accept""".split('\n')

		p = Parser(prog)

		res = p.parse_all()

		pass
