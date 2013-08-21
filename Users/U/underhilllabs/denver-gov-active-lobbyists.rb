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

# If you don't have two minutes to wait you might prefer this
# smaller pdf
# pdf = open('http://www.hmrc.gov.uk/factsheets/import-export.pdf')
# pdf = open('http://www.madingley.org/uploaded/Hansard_08.07.2010.pdf') 
# pdf = open('http://dl.dropbox.com/u/6928078/CLEI_2008_002.pdf')
pdf = open('http://www.denvergov.org/Portals/98/documents/Lobbyists/Public%20Record/CC_Active_Lobbyists.pdf')
#######  Instantiate the receiver and the reader
receiver = PageTextReceiver.new
pdf_reader = PDF::Reader.new 
#######  Now you just need to make the call to parse...
pdf_reader.parse(pdf, receiver)
#######  ...and do whatever you want with the text.  
#######  This just outputs it.

count = 0
receiver.content.each do |r| 
  
  # each page starts with header: TenureNo....
  # so split that off and grab the rest
  pages = r.split(/TenureNo\.NameLobbyist/)
  #pages[0] is the header, ignore that
  page = pages[1]

  # Currently this will choke on PO Boxes
  lobbyists = page.scan(/(\d{4})(.*?)(\d.*?)\; (\d{3}-\d{3}-\d{4}).*?Registered:(\S*?@\S*?\.\w{2,3}|\[not supplied\])/)
  lobbyists.each do |l|
    ScraperWiki.save_sqlite(unique_keys=["id"], data={"id"=>l[0], "name"=>l[1], "address"=>l[2], "phone"=>l[3], "email"=>l[4]})
    puts "saved #{l[1]}"   
  end
  count += lobbyists.length
end

puts "Found #{count} active lobbyists."
