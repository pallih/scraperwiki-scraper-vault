require 'nokogiri'
require 'open-uri'
require 'pdf/reader'

@BASE_URL = 'http://www.nyc.gov/html/nypd/html/crime_prevention/crime_statistics.shtml'
starting_url = @BASE_URL

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
  def move_text_position(*params)
  end
end
################  End of TextReceiver #############################

def parseCompStat (precinct, url)
  if precinct == "Manhattan South" then
    puts "Manhattan PDF info: (" + url + ")"
    pdf=open(url)    

    receiver = PageTextReceiver.new
    pdf_reader = PDF::Reader.new 

    pdf_reader.parse(pdf, receiver)
    receiver.move_text_position
    #receiver.content.each {|r| puts r.strip}
  end #if
end #def

def scrape_table(page)
  els=page.search "[text()*='Borough and Precinct Crime Statistics']"
  tbl1 = els.first.parent.parent.next_element
  tbl2 = tbl1.next_element.next_element

  tbl1.search("a").each do |borough|
    precinct = borough.inner_text
    precinctPDFurl = (URI.parse(@BASE_URL) + borough['href']).to_s
    parseCompStat(precinct,precinctPDFurl)
  end

  #  ScraperWiki.save_sqlite(unique_keys=['Link', 'Title', 'Episode', 'Appraiser', 'Value'], data=data)

end

## scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url)
    page = Nokogiri::HTML(open(url))
    scrape_table(page)
end

# ---------------------------------------------------------------------------
# START HERE
# ---------------------------------------------------------------------------
scrape_and_look_for_next_link(starting_url)