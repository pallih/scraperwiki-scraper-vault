from scraperwiki import swimport
csv2dict = swimport('csv2sw').csv2dict

# Write a csv
f = open('foobar.csv', 'w')
f.write('foo,bar,baz\n4,63,3')
f.close()

# Convert it to a dictionary
g = open('foobar.csv', 'r')
d = csv2dict(g)
print d