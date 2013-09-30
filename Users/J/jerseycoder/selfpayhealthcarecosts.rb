# Blank Ruby
require 'pdf-reader'
require 'open-uri'

io     = open('http://www.jcdcinfo.com/Forms/JCDC-Self-Pay_Price-List.pdf')
reader = PDF::Reader.new(io)

#puts reader.pdf_version
#puts reader.info
#puts reader.metadata
#puts reader.page_count

text = reader.pages.first.text
#puts page.fonts
lines=text.split('\n')
puts lines[0]
#puts page.raw_content

# Blank Ruby
require 'pdf-reader'
require 'open-uri'

io     = open('http://www.jcdcinfo.com/Forms/JCDC-Self-Pay_Price-List.pdf')
reader = PDF::Reader.new(io)

#puts reader.pdf_version
#puts reader.info
#puts reader.metadata
#puts reader.page_count

text = reader.pages.first.text
#puts page.fonts
lines=text.split('\n')
puts lines[0]
#puts page.raw_content

