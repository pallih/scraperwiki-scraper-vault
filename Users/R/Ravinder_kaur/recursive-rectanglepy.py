def rectangle(n,m):
  #base case no recursion
   if m==0:
       return
   else:
       print "*" * n

 #recursive case
       rectangle(n,m-1)
if __name__== '__main__':
     length=input('Rectangle length')
     width=input('rectangle width')
     call=rectangle(length,width)
        