require 'nokogiri'

Nokogiri::HTML(ScraperWiki::scrape("https://dev.twitter.com/docs/api/1.1")).search(".views-field-title a").each_with_index do |a, index|
  url = "https://dev.twitter.com" + a.attributes["href"].value
  page = ScraperWiki::scrape(url)
  doc = Nokogiri::HTML(page)
  title = doc.css('h1#title').text
  description = doc.css('#content-main > div > p').map(&:text)
  params = doc.css('.parameter').map{|param| [param.css('.param')[0].text.split, param.search('p')[0].text].flatten}
  rate_limited, per_user, per_app, authentication, family, object = Array.new(6)

  doc.css('.api-doc-block tr').each do |row|
    case row.children[0].text
    when "Rate Limited?"
      rate_limited = row.children[1].text
    when "Requests per rate limit window"
      per_user, per_app = row.children[1].text.split(/\/user|\/app/)
    when "Authentication"
      authentication = row.children[1].text
    when "Resource family"
      family = row.children[1].text
    when "Response Object"
      object = row.children[1].text
    end
  end

  data = {
    id: index + 1,
    url: url,
    resource: title,
    description: description,
    params: params,
    rate_limited: rate_limited,
    per_user: per_user,
    per_app: per_app,
    authentication: authentication,
    family: family,
    object: object,
  }
  ScraperWiki::save_sqlite(['resource'], data)      
end