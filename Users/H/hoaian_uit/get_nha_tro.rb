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
  category_links = page.search('.bgw a')
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
  #while (is_available(page)) do
  #  begin
      get_all_infos(page, text)
  #  rescue
  #  end

  #  page = get_next_page(page)
  #end
end

##
#get_next_page
#Parameters::
# *(Page) *params*:page
#Return:: The next page to be scraped
#*Author*::
#----------------------------------------------------------------------------
def get_all_infos page, category
  p "get all..."

  link = page.uri.to_s
  index = 1
  
  begin
  p page.uri.to_s
  p page.search('#dtlP a')

  list_items = page.search('#dtlP a')
  list_items.each_with_index{|item,index|
     p item

     href = item[:href]
     page = @agent.get(href)
     desc= page.search('.chitiet').first.text
     img = page.search('.ptdl img').first[:src]
     date = page.search('.ptd1').first.text

     # get all items in page -------------------
     info = page.search('.bd i')
     id = info[0].text
     count  = info[1].text
     price  = info[2].text
     area   = info[3].text

     info = page.search('.bd b')
     yc   = info[0].text
     record = {
        :id => id,
        :count   => count,
        :price   => price,
        :area    => area,
        :yc      => yc,
        :desc    => desc,
        :img     => img,
        :date    => date
     }

     begin
       ScraperWiki.save_sqlite([], record)
     rescue
     end
  }
  index += 1
      page = @agent.get(link.gsub(".html","") + "/page-#{index}.html")
  end while list_items.count > 0
end

##
#get_next_page
#Parameters::
# *(Page) *params*:page
#Return:: The next page to be scraped
#*Author*::
#----------------------------------------------------------------------------
def get_next_page page

  return false
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


scrap_data_from_page('http://thuephongtro.com/phong-tro/1c/quan-1.html')require 'rubygems'
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
  category_links = page.search('.bgw a')
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
  #while (is_available(page)) do
  #  begin
      get_all_infos(page, text)
  #  rescue
  #  end

  #  page = get_next_page(page)
  #end
end

##
#get_next_page
#Parameters::
# *(Page) *params*:page
#Return:: The next page to be scraped
#*Author*::
#----------------------------------------------------------------------------
def get_all_infos page, category
  p "get all..."

  link = page.uri.to_s
  index = 1
  
  begin
  p page.uri.to_s
  p page.search('#dtlP a')

  list_items = page.search('#dtlP a')
  list_items.each_with_index{|item,index|
     p item

     href = item[:href]
     page = @agent.get(href)
     desc= page.search('.chitiet').first.text
     img = page.search('.ptdl img').first[:src]
     date = page.search('.ptd1').first.text

     # get all items in page -------------------
     info = page.search('.bd i')
     id = info[0].text
     count  = info[1].text
     price  = info[2].text
     area   = info[3].text

     info = page.search('.bd b')
     yc   = info[0].text
     record = {
        :id => id,
        :count   => count,
        :price   => price,
        :area    => area,
        :yc      => yc,
        :desc    => desc,
        :img     => img,
        :date    => date
     }

     begin
       ScraperWiki.save_sqlite([], record)
     rescue
     end
  }
  index += 1
      page = @agent.get(link.gsub(".html","") + "/page-#{index}.html")
  end while list_items.count > 0
end

##
#get_next_page
#Parameters::
# *(Page) *params*:page
#Return:: The next page to be scraped
#*Author*::
#----------------------------------------------------------------------------
def get_next_page page

  return false
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


scrap_data_from_page('http://thuephongtro.com/phong-tro/1c/quan-1.html')