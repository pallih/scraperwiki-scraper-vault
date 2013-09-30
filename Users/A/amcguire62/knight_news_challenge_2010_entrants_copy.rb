require 'nokogiri'
require 'uri'

def scrape_page(page)
  url = "http://generalprop.newschallenge.org/SNC/GroupSearch.aspx?itemGUID=099e3da3-b2fc-494a-b391-f3e7e71cee40&pguid=900d111c-1475-4d78-8fab-789663818724&ItemListPage=" + page.to_s
  html = ScraperWiki.scrape(url)
  doc = Nokogiri::HTML(html)
  count = 0
  doc.search('.ItemContentContainer').each do |c|
    count = count + 1

    puts c.inner_html
    data = {}
    data['title'] = c.search('a')[0].inner_html
    data['details_url'] = URI.join(url, c.search('a')[0]['href'])
    data['user'] = c.search('a')[1].inner_html
    data['user_url'] = URI.join(url, c.search('a')[1]['href'])
    full_stars = c.css("img[src='App_Themes/Knight2010Proposals/images/star_sm_full.gif']").size
    half_stars = c.css("img[src='App_Themes/Knight2010Proposals/images/star_sm_half.gif']").size
    data['stars'] = full_stars.to_f + 0.5 * half_stars.to_f
    data['creation_date'] = Date.parse(c.search('.itemcreationdate')[0].inner_html)
    data['views'] = c.search('.viewcounter')[0].inner_html

    puts data.to_json
    ScraperWiki.save(unique_keys=['details_url',], data=data)
  end

  return count > 0
end

page = 0
while scrape_page(page):
  page = page + 1
  scrape_page(page)
end



require 'nokogiri'
require 'uri'

def scrape_page(page)
  url = "http://generalprop.newschallenge.org/SNC/GroupSearch.aspx?itemGUID=099e3da3-b2fc-494a-b391-f3e7e71cee40&pguid=900d111c-1475-4d78-8fab-789663818724&ItemListPage=" + page.to_s
  html = ScraperWiki.scrape(url)
  doc = Nokogiri::HTML(html)
  count = 0
  doc.search('.ItemContentContainer').each do |c|
    count = count + 1

    puts c.inner_html
    data = {}
    data['title'] = c.search('a')[0].inner_html
    data['details_url'] = URI.join(url, c.search('a')[0]['href'])
    data['user'] = c.search('a')[1].inner_html
    data['user_url'] = URI.join(url, c.search('a')[1]['href'])
    full_stars = c.css("img[src='App_Themes/Knight2010Proposals/images/star_sm_full.gif']").size
    half_stars = c.css("img[src='App_Themes/Knight2010Proposals/images/star_sm_half.gif']").size
    data['stars'] = full_stars.to_f + 0.5 * half_stars.to_f
    data['creation_date'] = Date.parse(c.search('.itemcreationdate')[0].inner_html)
    data['views'] = c.search('.viewcounter')[0].inner_html

    puts data.to_json
    ScraperWiki.save(unique_keys=['details_url',], data=data)
  end

  return count > 0
end

page = 0
while scrape_page(page):
  page = page + 1
  scrape_page(page)
end



require 'nokogiri'
require 'uri'

def scrape_page(page)
  url = "http://generalprop.newschallenge.org/SNC/GroupSearch.aspx?itemGUID=099e3da3-b2fc-494a-b391-f3e7e71cee40&pguid=900d111c-1475-4d78-8fab-789663818724&ItemListPage=" + page.to_s
  html = ScraperWiki.scrape(url)
  doc = Nokogiri::HTML(html)
  count = 0
  doc.search('.ItemContentContainer').each do |c|
    count = count + 1

    puts c.inner_html
    data = {}
    data['title'] = c.search('a')[0].inner_html
    data['details_url'] = URI.join(url, c.search('a')[0]['href'])
    data['user'] = c.search('a')[1].inner_html
    data['user_url'] = URI.join(url, c.search('a')[1]['href'])
    full_stars = c.css("img[src='App_Themes/Knight2010Proposals/images/star_sm_full.gif']").size
    half_stars = c.css("img[src='App_Themes/Knight2010Proposals/images/star_sm_half.gif']").size
    data['stars'] = full_stars.to_f + 0.5 * half_stars.to_f
    data['creation_date'] = Date.parse(c.search('.itemcreationdate')[0].inner_html)
    data['views'] = c.search('.viewcounter')[0].inner_html

    puts data.to_json
    ScraperWiki.save(unique_keys=['details_url',], data=data)
  end

  return count > 0
end

page = 0
while scrape_page(page):
  page = page + 1
  scrape_page(page)
end



