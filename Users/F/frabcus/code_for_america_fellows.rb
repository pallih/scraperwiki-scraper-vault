require 'nokogiri'


def get_year(year)
  html = ScraperWiki.scrape("http://codeforamerica.org/" + year.to_s + "-fellows/")
  
  doc = Nokogiri::HTML(html)
  doc.search('#fellowcarousel li').each do |f|
    data = {}
  
    # get basic data
    data['year'] = year
    data['name'] = f.search('strong')[0].inner_html
    data['photo'] = f.search('img')[0].attr('src')
    data['url'] = "http://codeforamerica.org" + f.search('a')[0].attr('href')

    # get details
    details_html = ScraperWiki.scrape(data['url'])
    details_doc = Nokogiri::HTML(details_html)
    posts = details_doc.search('.post')
    data["number_of_posts"] = posts.size

    # count comments on posts
    #comments_count = 0;
    #for post in posts
    #  comments_count = comments_count + post.search('#comments')[0].inner_html.to_i
    #end
    #data['total_comments'] = comments_count

    ScraperWiki.save(unique_keys=['year','name'], data)
  end
end

get_year(2011)
#get_year(2012)


require 'nokogiri'


def get_year(year)
  html = ScraperWiki.scrape("http://codeforamerica.org/" + year.to_s + "-fellows/")
  
  doc = Nokogiri::HTML(html)
  doc.search('#fellowcarousel li').each do |f|
    data = {}
  
    # get basic data
    data['year'] = year
    data['name'] = f.search('strong')[0].inner_html
    data['photo'] = f.search('img')[0].attr('src')
    data['url'] = "http://codeforamerica.org" + f.search('a')[0].attr('href')

    # get details
    details_html = ScraperWiki.scrape(data['url'])
    details_doc = Nokogiri::HTML(details_html)
    posts = details_doc.search('.post')
    data["number_of_posts"] = posts.size

    # count comments on posts
    #comments_count = 0;
    #for post in posts
    #  comments_count = comments_count + post.search('#comments')[0].inner_html.to_i
    #end
    #data['total_comments'] = comments_count

    ScraperWiki.save(unique_keys=['year','name'], data)
  end
end

get_year(2011)
#get_year(2012)


