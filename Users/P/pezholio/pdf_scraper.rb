#################################################################
# Extract text from a PDF file
# This scraper takes about 2 minutes to run and no output
# appears until the end.
#################################################################
# This scraper uses the pdf-reader gem.
# Documentation is at https://github.com/yob/pdf-reader#readme
# If you have problems you can ask for help at http://groups.google.com/group/pdf-reader
require 'pdf-reader'   
require 'open-uri'

pdf = open('http://www.staffordshire.gov.uk/transport/staffshighways/roadworks/trafficmanagementreport.pdf')

reader = PDF::Reader.new(pdf)

reader.pages.each do |page|
  puts page.raw_content
end

