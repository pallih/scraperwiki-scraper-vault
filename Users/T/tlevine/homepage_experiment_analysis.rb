rscript =<<chainsaw
#!Rscript
print('hi')
chainsaw

puts rscript

File.open('homepage.r', 'w') {|f| f.write(rscript) }

`chmod +x homepage.r`
`./homepage.r`