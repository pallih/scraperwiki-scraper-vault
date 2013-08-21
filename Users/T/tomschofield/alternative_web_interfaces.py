#don't worry about these lines - these are for importing libraries - libraries are collections of code written by others to help you do jobs
import scraperwiki           
import lxml.html   

#in python like all programming languages spelling is really important, upper/lowercase makes a difference too

#print makes things appear in the console make sure you put anything that's not a command in inverted commas 'like this' or "like this"
print 'hello world'

#now lets make a variable - a variable is like a pocket for information
my_number_pocket = 5
print my_number_pocket

#we can add stuff to it like this
my_number_pocket += 3

print 'my_number_pocket now = ',my_number_pocket

#we can also test it like this
if my_number_pocket == 3:
    print 'wow it really is 8!'
else:
    print 'oh darn its a different number'

#ok no this is a really tricky bit! we need to be able to make lists sometimes
aList = [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
print aList[4]

#lists can be lists of words too!
list_of_words = ['flip', 'flap', 'fly']
print list_of_words[0]

#what happens when you try to go past the end of a list?
list_of_words = ['flip', 'flap', 'fly']
print list_of_words[2]

#now try this!
try:
    print list_of_words[3]
except:
    print 'this list is only '+str(len(list_of_words))+' long!'


#now lets try some web scraping! don't worry about exactly what's happening here - I don't know either
html = scraperwiki.scrape('http://www.corriere.it/')
root = lxml.html.fromstring(html)

#paragraphs in html are supposed to live in a tag called <p> lets looks at some html source
#paragraphs = root.cssselect('p')
#for one_paragraph in paragraphs:
 #   print one_paragraph.text

#with scraperwiki we can easily find all the links on the page! great!
#for el in lxml.html.iterlinks(html):
#    print el

#we just want the link please not a whole list of crap
#for el in lxml.html.iterlinks(html):
#    print el[2]

#now we want to learn how to just get the links to articles we are interested in
#for el in lxml.html.iterlinks(html):
#    try:
#        exploded = el[2].split('/')
#        print exploded
#    except:
#        print 'problem exploding this url'

#now we want to check if this exploded stuff is what we want
#for el in lxml.html.iterlinks(html):
#    try:
#        exploded = el[2].split('/')
#        for part in exploded:
#            if part == 'cronache' or part == 'esteri':
#                print 'great this link is a match', el[2]
#                
#    except:
#        print 'problem exploding this url'

