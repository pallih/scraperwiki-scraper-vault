#1b fun with strings
def count_words(string)
#names=string.downcase.split(/\W+/)
#puts names
counts = Hash.new(0)
string.downcase.split(/\W+/).each { |name| counts[name] += 1 }
puts counts
end


count_words("A man, a plan, a canal -- Panama")
count_words "Doo bee doo bee doo"