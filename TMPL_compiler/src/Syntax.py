"""
Holds all of the syntax classes
"""
from typing import List

class Expr:
	def __init__(self,subExpr:list):
		self.subExpr = subExpr	#list of subexpressions

class AlphabetExpr(Expr):
	def __init__(self,alpha:List[str]):
		super().__init__([])
		self.alpha = alpha

class LabelExpr(Expr):
	def __init__(self,label:str):
		super().__init__([])
		self.label = label

class StrExpr(Expr):
	def __init__(self, string:str):
		super().__init__([])
		self.string = string

class String(StrExpr):
	def __init__(self,string:str):
		super().__init__(string)

class Blank(StrExpr):
	def __init__(self):
		super().__init__("_")#TODO: does this make sense?

class BooleanExpr:
	def __init__(self, subExpr: list):
		self.subExpr = subExpr	#list of subexpressions

class Equal(BooleanExpr):
	def __init__(self,str_expr:StrExpr):
		super().__init__([str_expr])

class NotEqual(BooleanExpr):
	def __init__(self, str_expr: StrExpr):
		super().__init__([str_expr])

class BooleanOrExpr(BooleanExpr):
	def __init__(self, exprs: List[BooleanExpr]):
		super().__init__(exprs)

class BooleanAndExpr(BooleanExpr):
	def __init__(self, exprs: List[BooleanExpr]):
		super().__init__(exprs)

class BooleanNotExpr(BooleanExpr):
	def __init__(self, a: BooleanExpr):
		super().__init__([a])

class BooleanTrue(BooleanExpr):
	def __init__(self):
		super().__init__([])

class BooleanFalse(BooleanExpr):
	def __init__(self):
		super().__init__([])

class Begin(BooleanExpr):
	def __init__(self):
		super().__init__([])

class End(BooleanExpr):
	def __init__(self):
		super().__init__([])

class ConditionalExpr(Expr):
	def __init__(self,condition:BooleanExpr,body:List[Expr]):
		super().__init__(body)
		self.condition = condition

class MovementExpr(Expr):
	def __init__(self,subExpr):
		super().__init__(subExpr)

class MovementLeft(MovementExpr):
	def __init__(self):
		super().__init__([])

class MovementRight(MovementExpr):
	def __init__(self):
		super().__init__([])

class Scan(Expr):
	def __init__(self,movement:MovementExpr,cond:BooleanExpr):
		super().__init__([movement,cond])

class WriteExpr(Expr):
	def __init__(self,wstr:StrExpr,movement:MovementExpr=None):
		if movement is not None:
			super().__init__([wstr,movement])
		else:
			super().__init__([wstr])

class GotoExpr(Expr):
	def __init__(self,ident:str):
		super().__init__([])
		self.ident = ident

class Accept(Expr):
	def __init__(self):
		super().__init__([])

class Reject(Expr):
	def __init__(self):
		super().__init__([])