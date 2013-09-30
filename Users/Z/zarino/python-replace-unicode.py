# testing replacement of unicode characters

# note the elipsis character (typed using alt-; on a Mac)
t = 'hello…'

# this should print out "hello world"
print t.replace('…', ' world')

# if we use a unicode string…
u = u'hello…'

# …we need to search for a unicode string
print u.replace(u'…', ' world')# testing replacement of unicode characters

# note the elipsis character (typed using alt-; on a Mac)
t = 'hello…'

# this should print out "hello world"
print t.replace('…', ' world')

# if we use a unicode string…
u = u'hello…'

# …we need to search for a unicode string
print u.replace(u'…', ' world')