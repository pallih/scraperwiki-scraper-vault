# Blank Ruby
require "rubygems"

a = Array.new(9)


a = [8,3,14]

len = a.length-1


#max[0] = a[0]

for i in 0..len
  for j in 0..len-i-1
   if a[j] > a[j+1] 
    max = a[j]
    a[j] = a[j+1]
    a[j+1] = max
     
    end  

  end
end

for k in 0..len
 puts a[k]
end

# Blank Ruby
require "rubygems"

a = Array.new(9)


a = [8,3,14]

len = a.length-1


#max[0] = a[0]

for i in 0..len
  for j in 0..len-i-1
   if a[j] > a[j+1] 
    max = a[j]
    a[j] = a[j+1]
    a[j+1] = max
     
    end  

  end
end

for k in 0..len
 puts a[k]
end

