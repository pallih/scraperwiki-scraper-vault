# Blank Python

print "Hello"

activeList = [1,2,3,4,5,6,7,8,9]
existingList = [1,4,5,9]
print activeList + existingList

for itemIndex in range(len(activeList)-1, -1, -1) :
    print itemIndex
    if activeList[itemIndex] in existingList :
        del activeList[itemIndex]
#        itemIndex += -2
        print  "popped from list, new length = ", len(activeList)

print activeList
print "run finished"

