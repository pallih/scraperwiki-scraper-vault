import jellyfish
print jellyfish.levenshtein_distance('jellyfish', 'smellyfish')
#2
print jellyfish.jaro_distance('jellyfish', 'smellyfish')
#0.89629629629629637
print jellyfish.damerau_levenshtein_distance('jellyfish', 'jellyfihs')
#1

print jellyfish.metaphone('Jellyfish')
#'JLFX'
print jellyfish.soundex('Jellyfish')
#'J412'
print jellyfish.nysiis('Jellyfish')
#'JALYF'
print jellyfish.match_rating_codex('Jellyfish')
#'JLLFSH'
