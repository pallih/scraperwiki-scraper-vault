# This scraper is to scrape the summary of all Development Applications for a Sample Council

# The summary of a Development Application includes:



# 1. council_reference: The unique identification assigned for a Development Application by the authority



#    Example: 'TA/00323/2012'



# 2. address: The physical address that the Development Application relates to. This will be geocoded so doesn't need to be a specific format

#    but obviously the more explicit it is the more likely it will be successfully geo-coded.

#    If the original address did not include the state (e.g. "QLD") at the end, then add it.



#    Example: '1 Sowerby St, Goulburn, NSW'



# 3. description: A text description of what the Development Application seeks to carry out.



#    Example: 'Ground floor alterations to rear and first floor addition'



# 4. info_url:  A URL that provides more information about the Development Application.

#    This should be a persistent URL that preferably is specific to this particular Development Application.

#    In many cases councils force users to click through a license to access Development Application.

#    In this case be careful about what URL you provide. Test clicking the link in a browser that hasn't established a session

#    with the council's site to ensure you will be able to click the link and not be presented with an error.



#    Example: 'http://foo.gov.au/app?key=527230'



# 5. comment_url:  A URL where users can provide a response to council about this particular Development Application.

#    As in info_url this needs to be a persistent URL and should be specific to this particular Development Application if possible.

#    Email mailto links are also valid in this field.



#    Example: 'http://foo.gov.au/comment?key=527230'



# 6. date_scraped:  The date that the scraper collects this data (i.e. now). Should be in ISO 8601 format.

#    Use the following Ruby code: Date.today.to_s



#    Example: '2012-08-01'



# History: December 27, 2012

# By nhuanvn



# Required libraries



require 'rubygems'

require 'mechanize'

require 'active_support'





# The starting URL to get Development Applications from



# Todo: Change the STARTING_URL to reflect your work

STARTING_URL = 'https://eservices.cairns.qld.gov.au/eservice/daEnquiryInit.do?nodeNum=227'

SEARCH_URL = 'https://eservices.cairns.qld.gov.au/eservice/daEnquiry.do?number='

CHILD_URL = 'https://eservices.cairns.qld.gov.au'

# COMMENT_URL_PREFIX: The prefix of the URL where users can provide a response to the council about a particular Development Application.

# That URL needs to be a persistent URL and should be specific to a particular Development Application if possible.

# Email mailto links are also valid in this field.



# Todo: Change the COMMENT_URL_PREFIX to reflect your work

COMMENT_URL_PREFIX = 'http://www.cairns.qld.gov.au/home/contact-us-online'





##

#get_all_das

#Parameters::

# *(Page) *params*:page

#Return:: All Development Applications from this council

#*Author*::

#----------------------------------------------------------------------------

def get_all_das(page_links)

  (@index..@max_index).each do |i|

   a = CHILD_URL + page_links[i].at('a')[:href]

   child_page = @agent.get(a)

   get_all_das_in_page(child_page)

  end

end





##

#is_available

#Parameters::

# *(Page) *params*:page

#Return:: Return true if the page is available for scraping Development Applications. Return false otherwise

#*Author*::

#----------------------------------------------------------------------------

def is_available(page)

  # Todo: Return true if the page is available for scraping Development Applications. Return false otherwise

  return !page.nil? 

end



##

#get_all_das_in_page



#Parameters::

# *(Page) *params*:page

#Return:: list of da in page

#*Author*::

#----------------------------------------------------------------------------

def get_all_das_in_page(child_page)

  # Todo: For each element of the page that contains the Development Application, get Development Application Summary.

  # For example:

  

  da_container = child_page.search("div#fullcontent p[class$=rowDataOnly]")

  get_da_summary(child_page, da_container)

end



##

#get_next_page

#Parameters::

# *(Page) *params*:page

#Return:: The next page to be scraped

#*Author*::

#----------------------------------------------------------------------------

def get_next_page(page)

  # Todo: Put your code here to get the next page to be scraped

  

end



##

#get_da_summary



#Parameters::

# *(tag) *params*:da_container tag

#Return:: The Development Application Summary which contains the list of fields as described on the top of this source file

#*Author*::

#----------------------------------------------------------------------------

def get_da_summary(page, da_container)

  # Todo: Put your code to process the da_container to get the Development Application Summary here

  

  result = {}

  da_container.each do |p_item|

    if p_item.at('span[class$=key]') != nil

      result[p_item.at('span[class$=key]').text] = p_item.at('span[class$=inputField]').text

    end

  end

  record = {

   'council_reference' => clean_whitespace(result["Application No."].to_s),

   'address' => clean_whitespace(result["Applicant Address"].to_s),

   'description' => CGI::unescapeHTML(clean_whitespace(result["Description of Work"].to_s)),

   'info_url' => SEARCH_URL + clean_whitespace(result["Application No."].to_s),

   'comment_url' => COMMENT_URL_PREFIX,

   'date_scraped' => Date.today.to_s,

   'page_content' => page.body.to_s.force_encoding('utf-8')

  }

  if ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? 

    ScraperWiki.save_sqlite(['council_reference'], record)

  else

    puts "Skipping already saved record " + record['council_reference']

  end

end



###############################################################################################

# Start of helper functions section

###############################################################################################



##

#clean whitespace

#Parameters::

# *(tag) *params*: a tag

#Return::a tag

#*Author*::

#----------------------------------------------------------------------------

def clean_whitespace(a)

  a.gsub("\r", ' ').gsub("\n", ' ').squeeze(" ").strip

end









###############################################################################################

# End of helper functions section

###############################################################################################





###############################################################################################

# The code to scrape will start running here

###############################################################################################

@agent = Mechanize.new{|a|

  a.ssl_version,

  a.verify_mode = 'SSLv3',

  OpenSSL::SSL::VERIFY_NONE,

  a.idle_timeout = 10000000,

  a.open_timeout = 10000000,

  a.read_timeout = 10000000,

  a.user_agent_alias = 'Linux Firefox'

}

p "KKKKKKKKKKKKK"
@agent.get('http://example.com/foo.torrent').save_as '/home/scriptrunner/xxx.html'
