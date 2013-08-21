import scraperwiki

#trying to convert integers to strings using str function 
#(int function would convert to integer)
#this is a list of integers
gobble = [0,2]
#this is a list of strings
gobblestr = ["0","2"]
print gobble
print gobblestr
#the 'hub' variable is assigned the results of using the str function on the first item in the list variable 'gobble'
hub = str(gobble[1])
print hub
#the next two lines print the results of adding two strings, and then the results of adding two integers
print "adding '2' and '0' makes...", str(gobble[1])+str(gobble[0])
print "adding 2 and 0 makes...", gobble[1]+gobble[0]

#this list has to use strings because they will be used as labels - integers will generate an error when saving
keysint = ["item1", 2, "item3", "item4","item5"]
#if they are all integers then the next few lines can be ignored. 
#create an empty list variable called 'keys'
keys = []
#loop through each item...
for key in keysint:
    #convert the item into a string using the str function, and put in 'stringkey' variable
    stringkey = str(key)
    #use the append method on that empty list 'keys' to add 'stringkey' to it
    keys.append(stringkey)
    #print that 'keys' list so far: the first time the loop runs it should have 1 item, the 2nd time 2, etc.
    print keys
tlist = range(100,130)
record = {}

#this section creates the fields in 'record' line by line...
record[keys[0]] = tlist[0]
record[keys[1]] = tlist[1]
record[keys[2]] = tlist[2]
record[keys[3]] = tlist[3]
record[keys[4]] = tlist[4]
print "record created line by line:", record
scraperwiki.sqlite.save([keys[0]], record, 'by_lines')

#this section creates the fields by iterating through a list - the code is shorter:
record2 = {}
for i in range(0,5):
    record2[keys[i]] = tlist[i]
print "record created by for loop", record2
scraperwiki.sqlite.save([keys[0]], record2, 'by_loop')

#we could also simplify it further by not having to work out the number of items in our keys list:
print "number of keys:", len(keys)

record2 = {}
#the end of our range is now not a number, but the result of calculating the number of items in the 'keys' list
for i in range(0,len(keys)):
    record2[keys[i]] = tlist[i]
print record2
scraperwiki.sqlite.save([keys[0]], record2)

import scraperwiki

#trying to convert integers to strings using str function 
#(int function would convert to integer)
#this is a list of integers
gobble = [0,2]
#this is a list of strings
gobblestr = ["0","2"]
print gobble
print gobblestr
#the 'hub' variable is assigned the results of using the str function on the first item in the list variable 'gobble'
hub = str(gobble[1])
print hub
#the next two lines print the results of adding two strings, and then the results of adding two integers
print "adding '2' and '0' makes...", str(gobble[1])+str(gobble[0])
print "adding 2 and 0 makes...", gobble[1]+gobble[0]

#this list has to use strings because they will be used as labels - integers will generate an error when saving
keysint = ["item1", 2, "item3", "item4","item5"]
#if they are all integers then the next few lines can be ignored. 
#create an empty list variable called 'keys'
keys = []
#loop through each item...
for key in keysint:
    #convert the item into a string using the str function, and put in 'stringkey' variable
    stringkey = str(key)
    #use the append method on that empty list 'keys' to add 'stringkey' to it
    keys.append(stringkey)
    #print that 'keys' list so far: the first time the loop runs it should have 1 item, the 2nd time 2, etc.
    print keys
tlist = range(100,130)
record = {}

#this section creates the fields in 'record' line by line...
record[keys[0]] = tlist[0]
record[keys[1]] = tlist[1]
record[keys[2]] = tlist[2]
record[keys[3]] = tlist[3]
record[keys[4]] = tlist[4]
print "record created line by line:", record
scraperwiki.sqlite.save([keys[0]], record, 'by_lines')

#this section creates the fields by iterating through a list - the code is shorter:
record2 = {}
for i in range(0,5):
    record2[keys[i]] = tlist[i]
print "record created by for loop", record2
scraperwiki.sqlite.save([keys[0]], record2, 'by_loop')

#we could also simplify it further by not having to work out the number of items in our keys list:
print "number of keys:", len(keys)

record2 = {}
#the end of our range is now not a number, but the result of calculating the number of items in the 'keys' list
for i in range(0,len(keys)):
    record2[keys[i]] = tlist[i]
print record2
scraperwiki.sqlite.save([keys[0]], record2)

