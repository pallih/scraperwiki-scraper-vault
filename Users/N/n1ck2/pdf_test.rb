#################################################################
# Extract text from a PDF file
# This scraper takes about 2 minutes to run and no output
# appears until the end.
#################################################################
# This scraper uses the pdf-reader gem.
# Documentation is at https://github.com/yob/pdf-reader#readme
# If you have problems you can ask for help at http://groups.google.com/group/pdf-reader

ScraperWiki.attach("lcc_links_to_most_recent_planning_dept_press_notic")
pdf_url = ScraperWiki.select("URL from lcc_links_to_most_recent_planning_dept_press_notic.swdata limit 1")
str = pdf_url[0].to_s
strLength = str.length
newStr = str[3,strLength]
puts newStr

#MAINTENANCE The URL needs editing to remove the first three letters. Don't know the Ruby equivalent for substr() method

#lcc_links_to_most_recent_planning_dept_press_notic

require 'pdf-reader'   
require 'open-uri'


##########  This section contains the callback code that processes the PDF file contents  ######
class PageTextReceiver
  attr_accessor :content, :page_counter
  def initialize
    @content = []
    @page_counter = 0
  end
  # Called when page parsing starts
  def begin_page(arg = nil)
    @page_counter += 1
    @content << ""
  end
  # record text that is drawn on the page
  def show_text(string, *params)
    @content.last << string
  end
  # there's a few text callbacks, so make sure we process them all
  alias :super_show_text :show_text
  alias :move_to_next_line_and_show_text :show_text
  alias :set_spacing_next_line_show_text :show_text
  # this final text callback takes slightly different arguments
  def show_text_with_positioning(*params)
    params = params.first
    params.each { |str| show_text(str) if str.kind_of?(String)}
  end
end
################  End of TextReceiver #############################

pdf = open(newStr) 


#######  Instantiate the receiver and the reader
#receiver = PageTextReceiver.new
receiver = PageTextReceiver.new
pdf_reader = PDF::Reader.new 
#######  Now you just need to make the call to parse...
pdf_reader.parse(pdf, receiver)
#######  ...and do whatever you want with the text.  
#######  This just outputs it.

data = receiver.content.each {|r| puts r.strip}

ScraperWiki.save_sqlite(unique_keys=["a"], data={"a"=>data})
