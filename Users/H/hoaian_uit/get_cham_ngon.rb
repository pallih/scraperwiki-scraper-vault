require 'rubygems'
require 'mechanize'

# global
@g_template = nil
@g_shop_id  = nil

##
#get_next_page
#Parameters::
# *(Page) *params*:page
#Return:: The next page to be scraped
#*Author*::
#----------------------------------------------------------------------------
def get_items_with_all_category page
  category_links = page.search('li a')
  category_links.each{|item|
    link = item[:href]
    text = item.text
    p text

    category_page = @agent.get(link)
    get_items_with_each_category(category_page, text)
  }
end

##
#get_next_page
#Parameters::
# *(Page) *params*:page
#Return:: The next page to be scraped
#*Author*::
#----------------------------------------------------------------------------
def get_items_with_each_category page, text
  get_items_in_page(page, text)
end

##
#get_next_page
#Parameters::
# *(Page) *params*:page
#Return:: The next page to be scraped
#*Author*::
#----------------------------------------------------------------------------
def get_items_in_page page, text
  while (is_available(page)) do
    begin
      get_all_infos(page, text)
    rescue
    end

    page = get_next_page(page)
  end
end

##
#get_next_page
#Parameters::
# *(Page) *params*:page
#Return:: The next page to be scraped
#*Author*::
#----------------------------------------------------------------------------
def get_all_infos page, category
  list_items = page.search('.post')

  link = page.uri.to_s
  list_items.each_with_index{|item,index|
     # get all items in page -------------------
     content = item.at('.entry-content a').text
     author  = item.at('.entry-author a').text
     record = {
        :category => category,
        :author   => author,
        :conent   => content
     }
     ScraperWiki.save_sqlite([], record)
  }
end

##
#get_next_page
#Parameters::
# *(Page) *params*:page
#Return:: The next page to be scraped
#*Author*::
#----------------------------------------------------------------------------
def get_next_page page
  link = page.search('.nextpostslink').first

  begin
    unless link[:href].nil? 
      return @agent.get(link[:href])
    end
  rescue
  end

  return nil
end

##
#get_next_page
#Parameters::
# *(Page) *params*:page
#Return:: The next page to be scraped
#*Author*::
#----------------------------------------------------------------------------
def is_available page
  return !page.nil? 
end

##
#get_next_page
#Parameters::
# *(Page) *params*:page
#Return:: The next page to be scraped
#*Author*::
#----------------------------------------------------------------------------
def scrap_all_pages
  Shop.find(:all).each {|item|
    @g_template = item.template
    @g_shopid = item.id

    scrap_data_from_page(item.home_page_link)
  }
end

##
#get_next_page
#Parameters::
# *(Page) *params*:page
#Return:: The next page to be scraped
#*Author*::
#----------------------------------------------------------------------------
def scrap_data_from_page link
  p link
  page = @agent.get(link)

  # get all categories
  get_items_with_all_category(page)
end


@agent = Mechanize.new{|a|
  a.ssl_version,
  a.verify_mode = 'SSLv3',
  OpenSSL::SSL::VERIFY_NONE,
  a.user_agent_alias = 'Linux Firefox'
}


scrap_data_from_page('http://khotangdanhngon.com/')