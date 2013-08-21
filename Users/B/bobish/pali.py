import scraperwiki

# Blank Python

s = "malayalam"
r= ""

i = len(s)-1

while i < len(s):

    r += s[i]
    
    i = i-1

    if i < 0:

        break



if s == r:
    print "Pali"
else:
    print "not pali"
