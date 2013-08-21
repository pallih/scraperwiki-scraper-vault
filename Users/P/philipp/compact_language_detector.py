import scraperwiki
import cld

text = []
text.append('hello over there, i am from Moscow')
text.append('Привет всем, я алкоголик из Москвы')
text.append('Hola a todos, soy un alcohólico de Moscú') 


topLanguageName = []
lngCode = []

for x in range (len(text)):

    topLanguageName.append( cld.detect(text[x])[0])
    lngCode.append( cld.detect(text[x])[1])
    print topLanguageName[x]
        
