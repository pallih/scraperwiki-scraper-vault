import scraperwiki

# Demoulidor Python Experimentos para Extrator de palavras entre expressões contidas em arquivos .txt

#Experimentando busca literal e extração simples
print "Extrai o texto existente entre dois pedaços de texto localizados num texto completo:"
 
def extraia(texto, subtexto1, subtexto2):
#Extrai o texto existente entre dois pedaços de texto (subtexto1 e subtexto2) localizados num texto completo
    return texto.split(subtexto1)[-1].split(subtexto2)[0]
 
textoCompleto = "The alien wheezes, 'Darn, this is it. I will die now! \n"\
"Tell my 2.4 million larvae that I esteem them ... \n"\
"Good-bye, truculent universe.'"

textoExtraido = extraia(textoCompleto, 'Tell my', 'larvae')
print textoCompleto
print textoExtraido

# how to create a multiline string ...
print "This is a multiline string:"
mlStr = """Noses are running.
Feet are smelling.
Park on driveway.
Drive on parkway.
Recite at a play.
Play at a recital.
"""
print mlStr
print "Show the line that starts with Park:"
# find Park index/position
pos1 = mlStr.find("Park")
print pos1
# find index of the end of that line
pos2 = mlStr.find("\n", pos1)
print pos2
# slice the line from the string
line = mlStr[pos1:pos2]
print line

data = [ {"a":x*x} for x in range(99) ]
scraperwiki.sqlite.save(["a"], data)

a = " i am very fine "
print a
b="Nada"

def strcompress(mystring):
    mystring_compressed = ''.join(mystring.split())
    return mystring_compressed

#b="".join([x.strip() for x in a.split(' ')])
b=a.replace(' ','')
print b
print b
print "Fim"

s = 'a123'
if s.isdigit():
    print  "É número: "+s
else:
    print  "Não é número: "+s


import scraperwiki

# Demoulidor Python Experimentos para Extrator de palavras entre expressões contidas em arquivos .txt

#Experimentando busca literal e extração simples
print "Extrai o texto existente entre dois pedaços de texto localizados num texto completo:"
 
def extraia(texto, subtexto1, subtexto2):
#Extrai o texto existente entre dois pedaços de texto (subtexto1 e subtexto2) localizados num texto completo
    return texto.split(subtexto1)[-1].split(subtexto2)[0]
 
textoCompleto = "The alien wheezes, 'Darn, this is it. I will die now! \n"\
"Tell my 2.4 million larvae that I esteem them ... \n"\
"Good-bye, truculent universe.'"

textoExtraido = extraia(textoCompleto, 'Tell my', 'larvae')
print textoCompleto
print textoExtraido

# how to create a multiline string ...
print "This is a multiline string:"
mlStr = """Noses are running.
Feet are smelling.
Park on driveway.
Drive on parkway.
Recite at a play.
Play at a recital.
"""
print mlStr
print "Show the line that starts with Park:"
# find Park index/position
pos1 = mlStr.find("Park")
print pos1
# find index of the end of that line
pos2 = mlStr.find("\n", pos1)
print pos2
# slice the line from the string
line = mlStr[pos1:pos2]
print line

data = [ {"a":x*x} for x in range(99) ]
scraperwiki.sqlite.save(["a"], data)

a = " i am very fine "
print a
b="Nada"

def strcompress(mystring):
    mystring_compressed = ''.join(mystring.split())
    return mystring_compressed

#b="".join([x.strip() for x in a.split(' ')])
b=a.replace(' ','')
print b
print b
print "Fim"

s = 'a123'
if s.isdigit():
    print  "É número: "+s
else:
    print  "Não é número: "+s


