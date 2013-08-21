## BOE SEARCH RESULTS SCRAPER ##
# scraping libraries
require 'mechanize'
require 'nokogiri'
require 'open-uri'

## INPUT ARGUMENTS
# Text input argument for the BOE search scraper
TEXT = 'biblioteca'
# Title input argument for the BOE search scraper
TITLE = ''
# Date input argument for the BOE search scraper
YEAR = '2013'


# Base url for our BOE search scraper page
BASE_URL='http://www.boe.es/buscar/boe.php?'
# fixed preffix params for our scraper page
FIXED_PARAMS='frases=no&campo[1]=DOC&operador[1]=and'\
             '&campo[2]=TIT&operador[2]=and'\
             '&campo[6]=FPU&operador[6]=and'\
             '&sort_field[0]=fpu&sort_order[0]=asc'\
             '&sort_field[1]=ref&sort_order[1]=asc&accion=Buscar'

# Maximum number of hit pages returned by boe search engine
MAX_PAGE_HITS = 1000
# We will always try to get as many page_hits as possible
FIXED_SEARCH_PARAMS="accion=Mas&coleccion=boe&page_hits=#{MAX_PAGE_HITS}"

class BOESearchSpider
  attr_accessor :stext, :stitle, :syear
 
  def initialize(text,title,year)
    @agent = Mechanize.new
    @stext = text
    @stitle = title
    @syear = year
  end

  def get_search_info()
    # Get the hidden search id for this search params
    search_params="&dato[1]=#{stext}&dato[2]=#{stitle}&dato[6][0]=01/01/#{syear}&dato[6][1]=31/12/#{syear}"
    p "#{BASE_URL}#{FIXED_PARAMS}#{search_params}"
    results = @agent.get("#{BASE_URL}#{FIXED_PARAMS}#{search_params}")
    id_busqueda = results.form.field_with(:name => 'id_busqueda').value
    t_num_results = @agent.page.parser.css('div.paginar li')[0].text =~ /\s*de\s*(\d+)$/
    num_results = $1.to_i
    p num_results
    return id_busqueda, num_results
  end

  def get_search_results()
    id_busqueda, num_results = get_search_info()
    iterations = (num_results / MAX_PAGE_HITS)
    p iterations 
    for i in 0..iterations
      fetch_results(id_busqueda,i*1000)
    end    
  end
  
  def fetch_results(id,start)
    params = "&start=#{start}&id_busqueda=#{id}"
    @agent.get("#{BASE_URL}#{FIXED_SEARCH_PARAMS}#{params}")
    results = @agent.page.parser.css('div.listadoResult div.enlacesMas a').map { |link| link['href'] }.uniq
    results.each {|result|
      result.gsub!(/\.\.\//,"http://www.boe.es/")
      result =~ /id=(.*)$/
      p $1,result
      data = {
        boe: $1,
        link: result
      }
       ScraperWiki::save_sqlite(['boe'], data)
    }
  end
end

spider = BOESearchSpider.new(TEXT, TITLE, YEAR)
spider.get_search_results()