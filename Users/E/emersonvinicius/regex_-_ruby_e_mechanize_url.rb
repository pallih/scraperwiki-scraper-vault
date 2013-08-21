# ANALISANDO TEXTO COM REGEX

frase = 'Ministerio do esporte, valor R$ 4000,00 no dia 01/02/1999 em especie.'
frase_ = frase.match /(.+), valor R\$ (.+) no dia (.+) em (.+)\./

puts "Ministerio: #{frase_[1]}"
puts "Valor: #{frase_[2]}"
puts frase_[3]
puts frase_[4]

