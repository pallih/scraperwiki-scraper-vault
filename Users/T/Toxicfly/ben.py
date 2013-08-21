import urllib

html = urllib.urlopen("http://eliteadultwebmasters.com/stats/stats.php?user=3573&pass=question1269&csv=1&page=tracking_csv&days_back=1").read()
print(html)

MyArray =  html.split('\n')
T2 = '0'
for i in range(5,len(MyArray)):
 
 try:
  Val = MyArray[i].split(',')
  if Val[2].upper() == 'EXORON':
   T2 = int(T2) + int(Val[4])
 except IndexError:
  Val = ''

Total = T2*50
print "$"+ str(Total)