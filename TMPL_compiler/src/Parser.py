"""
Given pl syntax, parse it to create abstract syntax
"""
from Syntax import *
import re

COMMENT_CHAR = '#'

class Parser:
	def __init__(self,lines: List[str]):
		self.lines = lines
		self.lindex = 0
		self.prev_indent = 0

		self.alphabet_defined = False	#the first line defines the alphabet used for the machine, the tape alphabet is inferred


	def get_within_first_open_paren(self, s:str):
		parens = []  # stack of parens
		initial_paren_idx = -1
		final_paren_idx = 0
		for ch in s:
			final_paren_idx += 1
			open = ch == '('
			close = ch == ')'

			if open:
				parens.append(ch)
				if initial_paren_idx == -1:
					initial_paren_idx = final_paren_idx - 1
			elif close:
				if len(parens) == 0:
					raise SyntaxError('Parentheses unbalanced in string: ' + s)

				parens.pop(-1)

				if (len(parens) == 0):
					return s[initial_paren_idx:final_paren_idx]

		return s[initial_paren_idx:]

	'''
	Check if this string is in the balanced paren language (ignoring non alphabet chars)
	'''
	def paren(self,s:str):
		paren_inv_map = {')': '(',
						 '}': '{',
						 ']': '['}

		parens = []  # stack of parens
		for ch in s:
			open = ch in {'(', '{', '['}
			close = ch in {')', '}', ']'}

			if open:
				parens.append(ch)
			elif close:
				if (len(parens) == 0) or (parens[-1] != paren_inv_map[ch]):
					return False

				parens.pop(-1)

		return len(parens) == 0



	def get_boolstr_subexp(self,boolstr:str):
		#first try for parens
		parens = re.match(r'\(.*',boolstr)
		if parens:
			#get the interior
			subexp = self.get_within_first_open_paren(boolstr)
			return subexp
		else:
			#no luck, we need to get it directly
			subexp = re.match(r'((?:\w+)|(?:[!=]\s*=\s*["\']([^"\']*)["\'])|(?:.*?\s+(?:or|and)))',boolstr).group(1)
			trim = re.match(r'(.*)\s+(?:or|and)',subexp)
			if trim is not None:
				return trim.group(1)
			return subexp

	'''
	== 'a' or == 'b' is not ambiguous
	the only things that would be are like p or q and r... they involve ors or ands 
	'''
	def parseBoolean(self,boolstr:str,check_paren=True) -> BooleanExpr:
		if check_paren:
			if not self.paren(boolstr):
				raise SyntaxError('Parentheses/brackets unbalanced in string: ' + boolstr)

		eq_re = re.match(r'=\s*=\s*["\']([^"\']*)["\']$',boolstr)
		if eq_re:
			st = String(eq_re.group(1))
			return Equal(st)

		neq_re = re.match(r'!\s*=\s*["\']([^"\']*)["\']$',boolstr)
		if neq_re:
			st = String(neq_re.group(1))
			return NotEqual(st)

		begin_re = re.match('begin$',boolstr)
		if begin_re:
			return Begin()

		end_re = re.match('end$',boolstr)
		if end_re:
			return End()

		true_re = re.match('true$',boolstr,re.IGNORECASE)
		if true_re:
			return BooleanTrue()

		false_re = re.match('false$', boolstr, re.IGNORECASE)
		if false_re:
			return BooleanFalse()

		or_and_re = re.match(r'.*?\s+(?:or|and)\s+.*(?:\s+(?:or|and)\s+.*)*',boolstr)

		if or_and_re:
			#both or and and can chain together any number of subexpressions, so we need to handle that here
			subexps = []#it has to be one of or or and though, so we need to get all the subexps
			expr_type = None
			sidx = 0
			while sidx < len(boolstr):
				subexp = self.get_boolstr_subexp(boolstr[sidx:])
				sidx += len(subexp)
				#drop the parens if they're there
				if self.get_within_first_open_paren(subexp) == subexp:#then this is in a single paren block, drop the outer ones
					subexp = subexp[1:-1]
				expr_type_re = re.match(r'(\s*)(\S+)(\s+)\S',boolstr[sidx:])
				if expr_type_re:
					expr_type_temp = expr_type_re.group(2)
					sidx += len(expr_type_re.group(1)) + len(expr_type_temp) + len(expr_type_re.group(3))
					if expr_type is not None:
						if expr_type_temp != expr_type:
							raise SyntaxError('Two different expression types chained (' + str(expr_type) + ' and ' + str(expr_type_temp) + ') in ' + boolstr)
					else:
						expr_type = expr_type_temp

				subexps.append(self.parseBoolean(subexp,check_paren=False))

			if expr_type == 'or':
				return BooleanOrExpr(subexps)
			elif expr_type == 'and':
				return BooleanAndExpr(subexps)
			else:
				raise SyntaxError('Unknown chainable boolean expression type: ' + expr_type)

		not_re = re.match(r'(?:(?:not\s+)|(?:!\s*))([^=].*)',
						  boolstr)  # we don't need to be too careful with the ! operator since notequals has already been checked for
		if not_re:
			# grab the applicable expr
			subexp = self.get_boolstr_subexp(not_re.group(1))
			return BooleanNotExpr(self.parseBoolean(subexp, check_paren=False))




	def parseDirection(self,dir):
		if dir == 'L':
			return MovementLeft()
		elif dir == 'R':  # dir is 'R'
			return MovementRight()

		return None

	def get_line_indent(self,lindex=None):
		if lindex is None:
			lindex = self.lindex

		if (lindex < 0) or (lindex >= len(self.lines)):
			return 0
		m = re.match(r'\s*',self.lines[lindex])
		return len(m.group(0))

	def read_line(self):
		self.prev_indent = self.get_line_indent()
		ret = self.lines[self.lindex]
		self.lindex += 1
		return ret

	def parseline(self) -> Expr:
		#line should be pruned of all whitespace and comments
		raw_line = self.read_line()
		line_clean_re = re.match(r'\s*((?:[^#\s]*\s*)*[^#\s])\s*(?:#.*)?',raw_line)
		line = None
		if line_clean_re:
			line = line_clean_re.group(1)

		if line:
			label_re = re.match(r':(\S*)',line)
			if label_re:
				if not self.alphabet_defined:
					raise SyntaxError("The first line must define the alphabet (e.g. 'ab' defines alphabet {'a','b'})")
				return LabelExpr(label_re.group(1))

			movement_re = re.match(r'[LR]',line)
			if movement_re:
				if not self.alphabet_defined:
					raise SyntaxError("The first line must define the alphabet (e.g. 'ab' defines alphabet {'a','b'})")
				dir = movement_re.group(0)
				return self.parseDirection(dir)

			goto_re = re.match(r'goto\s+(\S*)',line)
			if goto_re:
				if not self.alphabet_defined:
					raise SyntaxError("The first line must define the alphabet (e.g. 'ab' defines alphabet {'a','b'})")
				return GotoExpr(goto_re.group(1))

			write_re = re.match(r'write\s+(?:["\']([^"\']+)["\']|_)\s+([LR])?',line)
			if write_re:
				if not self.alphabet_defined:
					raise SyntaxError("The first line must define the alphabet (e.g. 'ab' defines alphabet {'a','b'})")
				wst = write_re.group(1)
				if wst is None:
					writestr = Blank()
				else:
					writestr = String(wst)
				dir = write_re.group(2)
				mvdir = self.parseDirection(dir)
				return WriteExpr(writestr,mvdir)#mvdir may be none if group 2 is none

			accept_re = re.match('accept',line)
			if accept_re:
				if not self.alphabet_defined:
					raise SyntaxError("The first line must define the alphabet (e.g. 'ab' defines alphabet {'a','b'})")
				return Accept()

			reject_re = re.match('reject',line)
			if reject_re:
				if not self.alphabet_defined:
					raise SyntaxError("The first line must define the alphabet (e.g. 'ab' defines alphabet {'a','b'})")
				return Reject()

			scan_re = re.match(r'scan\s+([LR])\s+until\s+(.*)',line)
			if scan_re:
				if not self.alphabet_defined:
					raise SyntaxError("The first line must define the alphabet (e.g. 'ab' defines alphabet {'a','b'})")
				mvdir = self.parseDirection(scan_re.group(1))
				boolstr = scan_re.group(2)
				bexp = self.parseBoolean(boolstr)

				return Scan(mvdir,bexp)

			if not self.alphabet_defined:
				#then this line must define the alphabet
				alph_str = re.match(r'(?:[^,],?)+',line).group(0)
				self.alphabet_defined = True
				return AlphabetExpr(list(alph_str))

			#all else fails it has to be a conditional
			bexp = self.parseBoolean(line)
			indent_level =  self.get_line_indent()
			if indent_level <= self.prev_indent:
				raise SyntaxError("Expected indent after line: " + line)
			#get the exprs for it
			exprs = []
			while (self.lindex < len(self.lines)) and (self.get_line_indent() >= indent_level):
				if self.get_line_indent() == indent_level:#let each conditional do its own lines in parseline
					lparse = self.parseline()
					if lparse:
						exprs.append(lparse)

			return ConditionalExpr(bexp,exprs)

	def parse_all(self) -> List[Expr]:
		ret = []
		while self.lindex < len(self.lines):
			lparse = self.parseline()
			if lparse:
				ret.append(lparse)

		return ret