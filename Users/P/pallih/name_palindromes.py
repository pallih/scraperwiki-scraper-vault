# -*- coding: utf-8 -*-
import scraperwiki

scraperwiki.sqlite.attach("gotur") 
 
boys = scraperwiki.sqlite.select("* from gotur.boys")   
girls = scraperwiki.sqlite.select("* from gotur.girls")   
print len(girls)
def IsPalindromeString(n):
    myLen = len(n)
    i = 0
    while i <= myLen/2:
        if n[i] != n[myLen-1-i]:
            return False
        i += 1
    return True

def is_palindrome(s):
    return s == s[::-1]


for name in boys:
    #print name['name'].lower()
    if IsPalindromeString(name["name"].lower()) == True:
        print name['name']  


for name in girls:
    
    #print name['name']
    #print name["name"].lower()
    #print repr(name["name"].lower())
    #print IsPalindromeString(name["name"].lower())
    #print name['name'].encode('utf-8')
    if IsPalindromeString(name["name"].lower()) == True:
        print name['name']  

# -*- coding: utf-8 -*-
import scraperwiki

scraperwiki.sqlite.attach("gotur") 
 
boys = scraperwiki.sqlite.select("* from gotur.boys")   
girls = scraperwiki.sqlite.select("* from gotur.girls")   
print len(girls)
def IsPalindromeString(n):
    myLen = len(n)
    i = 0
    while i <= myLen/2:
        if n[i] != n[myLen-1-i]:
            return False
        i += 1
    return True

def is_palindrome(s):
    return s == s[::-1]


for name in boys:
    #print name['name'].lower()
    if IsPalindromeString(name["name"].lower()) == True:
        print name['name']  


for name in girls:
    
    #print name['name']
    #print name["name"].lower()
    #print repr(name["name"].lower())
    #print IsPalindromeString(name["name"].lower())
    #print name['name'].encode('utf-8')
    if IsPalindromeString(name["name"].lower()) == True:
        print name['name']  

