# 1a_Fun with Strings

def palindrome?(string)
c=string.gsub(/[\s\'\,\-\!]/,'\1').downcase
b=c.reverse
result=case b<=>c
when 0 then p "True"
else p "False"
end 
end


palindrome?("A man, a plan, a canal -- Panama") 
palindrome?("Madam, I'm Adam!")  
palindrome?("Abracadabra") 
palindrome?("I'm a m'i")



# 1a_Fun with Strings

def palindrome?(string)
c=string.gsub(/[\s\'\,\-\!]/,'\1').downcase
b=c.reverse
result=case b<=>c
when 0 then p "True"
else p "False"
end 
end


palindrome?("A man, a plan, a canal -- Panama") 
palindrome?("Madam, I'm Adam!")  
palindrome?("Abracadabra") 
palindrome?("I'm a m'i")



