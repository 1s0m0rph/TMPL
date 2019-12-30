from Compiler import *
from Parser import *

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

e = Encoder(c.M)
e.write_to_file('../test.TM')