# Blank Python
fruits = ['apple', 'pear', 'orange']
target = 'this is not a kiwi fruit'

def avoids(l, target):
    """Return true when *none* of the items in *l* are in target."""
    for i in l:
        if i in target:
            return False
    return True

# obscure feature of for loop
v = False
for i in fruits:
    if i in target:
        break
else:
    v = True


max(i in target for i in fruits) == False # same as not max blah blah blah

all(i not in target for i in fruits) # ***

not any(i in target for i in fruits)


matches = [i for i in fruits if i in target]
if not matches: # same as if not empty list