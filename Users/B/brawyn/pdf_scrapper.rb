#################################################################
# Extract text from a PDF file
#################################################################
# This scraper uses the pdf-reader gem.
# Documentation is at https://github.com/yob/pdf-reader#readme
# If you have problems you can ask for help at http://groups.google.com/group/pdf-reader
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

pdf = open('http://www.domstol.dk/om/talogfakta/statistik/Documents/Tvangsauktioner/2011/Hel%C3%A5r/Tvangsauktioner%20-%20afsluttede%20sager%20-%202011.pdf')

#######  Instantiate the receiver and the reader
receiver = PageTextReceiver.new
pdf_reader = PDF::Reader.new 
#######  Now you just need to make the call to parse...
pdf_reader.parse(pdf, receiver)
#######  ...and do whatever you want with the text.  
#######  This just outputs it.
receiver.content.each {|r| puts r.strip}
