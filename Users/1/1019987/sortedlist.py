

import turtle
nos=[
'25',
'1',
'5',
'4',
]
print "Before Sorting List"
print nos
print 
def numbers (x,y):
    import re
    def num(str):
     return float(re.findall(r'\d+',str)[0])
    return cmp(num(x),num(y))

nos.sort(numbers)
print "After Sorting"
print nos


