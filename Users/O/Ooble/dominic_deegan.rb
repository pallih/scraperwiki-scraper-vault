require 'nokogiri'

def comics
  html = ScraperWiki::scrape('http://dominic-deegan.com/')
  document = Nokogiri::HTML html
  comics = document.css '.comic'
  comics.zip(1..comics.length).map { |comic, position|
    {
      position: position,
      image: comic.css('img').first.attribute('src').content,
      date: Date.strptime(comic.css('.date').first.content, '%A, %B %e, %Y')
    }
  }
end

def news
  html = ScraperWiki::scrape('http://dominic-deegan.com/news.php')
  document = Nokogiri::HTML html
  posts = document.css '#blogs .blog'
  posts.map { |post|
    {
      title: post.css('.title').first.content,
      date: Date.strptime(post.css('.time').first.content, '%B %e, %Y'),
      author: post.css('.author').first.content.sub(/^Posted by /, ''),
      content: post.css('.content').first.inner_html
    }
  }
end

ScraperWiki::save_sqlite [:image, :date], comics, 'comics'
ScraperWiki::save_sqlite [:title, :date], news, 'news'
require 'nokogiri'

def comics
  html = ScraperWiki::scrape('http://dominic-deegan.com/')
  document = Nokogiri::HTML html
  comics = document.css '.comic'
  comics.zip(1..comics.length).map { |comic, position|
    {
      position: position,
      image: comic.css('img').first.attribute('src').content,
      date: Date.strptime(comic.css('.date').first.content, '%A, %B %e, %Y')
    }
  }
end

def news
  html = ScraperWiki::scrape('http://dominic-deegan.com/news.php')
  document = Nokogiri::HTML html
  posts = document.css '#blogs .blog'
  posts.map { |post|
    {
      title: post.css('.title').first.content,
      date: Date.strptime(post.css('.time').first.content, '%B %e, %Y'),
      author: post.css('.author').first.content.sub(/^Posted by /, ''),
      content: post.css('.content').first.inner_html
    }
  }
end

ScraperWiki::save_sqlite [:image, :date], comics, 'comics'
ScraperWiki::save_sqlite [:title, :date], news, 'news'
