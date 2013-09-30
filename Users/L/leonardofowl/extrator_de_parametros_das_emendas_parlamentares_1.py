# Demoulidor Python Extrator de parâmetros das Emendas Parlamentares do DF 2012 para o "DeOlhoNasEmendas" no www.adoteumdistrital.com.br
import scraperwiki
#html = scraperwiki.scrape("http://thacker.diraol.eng.br/thackerdf/emendasDistritais/2012/txt/dcl-2011-11-23-suplemento1.txt")
#print html
# my first string
myString = "Hello there ABCDbobCDA@"

#my sub string
mySubString=myString[myString.find("D")+1:myString.find("CDA")]
#print mySubString

print "Extract a substring located between two given substrings, here the quotes:"
 
def extract(text, sub1, sub2):
#"""extract a substring between two substrings sub1 and sub2 in text"""
    return text.split(sub1)[-1].split(sub2)[0]
 
str3 = 'I bought the "Python Cookbook" and could not find one single recipe about cooking the slithery beast!'
# notice that here beginning and trailing spaces can be included with the quotes
str4 = extract(str3, 'bought the ', 'and could')
print str3
print str4
# Demoulidor Python Extrator de parâmetros das Emendas Parlamentares do DF 2012 para o "DeOlhoNasEmendas" no www.adoteumdistrital.com.br
import scraperwiki
#html = scraperwiki.scrape("http://thacker.diraol.eng.br/thackerdf/emendasDistritais/2012/txt/dcl-2011-11-23-suplemento1.txt")
#print html
# my first string
myString = "Hello there ABCDbobCDA@"

#my sub string
mySubString=myString[myString.find("D")+1:myString.find("CDA")]
#print mySubString

print "Extract a substring located between two given substrings, here the quotes:"
 
def extract(text, sub1, sub2):
#"""extract a substring between two substrings sub1 and sub2 in text"""
    return text.split(sub1)[-1].split(sub2)[0]
 
str3 = 'I bought the "Python Cookbook" and could not find one single recipe about cooking the slithery beast!'
# notice that here beginning and trailing spaces can be included with the quotes
str4 = extract(str3, 'bought the ', 'and could')
print str3
print str4
