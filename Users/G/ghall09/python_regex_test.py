import re

f = "abcdefghijklmnop"

strtosearch = ''

for line in f:
    strtosearch += line

print(strtosearch)

patfinder1 = re.compile('def')
findpat1 = re.search(patfinder1, strtosearch)

print(findpat1.group())
print(findpat1.start())
print(findpat1.end())
print(findpat1.span())

findpat1 = re.findall(patfinder1, strtosearch)

for i in findpat1:
    print(i)import re

f = "abcdefghijklmnop"

strtosearch = ''

for line in f:
    strtosearch += line

print(strtosearch)

patfinder1 = re.compile('def')
findpat1 = re.search(patfinder1, strtosearch)

print(findpat1.group())
print(findpat1.start())
print(findpat1.end())
print(findpat1.span())

findpat1 = re.findall(patfinder1, strtosearch)

for i in findpat1:
    print(i)