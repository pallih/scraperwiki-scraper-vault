# Blank Ruby

puts RUBY_VERSION

def bar()
  print "I am bar()!"
  raise "Exceptional thing happening in bar()"
end

def foo()
  print "I am foo()!"
  bar()
end

x = [1,2,3,4,5]

foo()
#x.each |c|
#  foo()
#end

# Blank Ruby

puts RUBY_VERSION

def bar()
  print "I am bar()!"
  raise "Exceptional thing happening in bar()"
end

def foo()
  print "I am foo()!"
  bar()
end

x = [1,2,3,4,5]

foo()
#x.each |c|
#  foo()
#end

