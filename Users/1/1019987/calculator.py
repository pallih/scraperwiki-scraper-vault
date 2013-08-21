
import turtle
print "Welcome to my calculator!"
print "Press 1 for Add 2 number"
print "Press 2 for Subtract 2 number"
print "Press 3 for Multiplication of 2 numbers"
print "Press 4 for Division of 2 numbers"
print "Press 5 for get the power one number to the power of another"
print "Press 6 for quit from the calculator"
a = input("Please enter the first number: ")
b = input("Please enter the second number: ")
m = a+b
n = a-b
o = a*b
p = float(a/b)
q = pow (a, b)

output =input("what do you want ")
if output==1:
   print "Your answer is",m
if output==2:
    print "Your answer is",n
if output==3:
    print "Your anwer is",o
if output==4:
    print "Your answer is", p
if output==5:
    print "Your answer is", q
if output==6:
    print "You are successfully exit!"



