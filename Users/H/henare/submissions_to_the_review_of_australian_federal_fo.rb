require 'mechanize'

agent = Mechanize.new
base_url = 'http://www.ag.gov.au'

page = agent.get "#{base_url}/Consultationsreformsandreviews/Pages/ReviewofFOIlaws.aspx"

submissions = page.at('#ctl00_PlaceHolderMain_ctl01_ctl02__ControlWrapper_RichHtmlField').search(:ul)[1].search(:li)

submissions.each do |submission|
  link = base_url + submission.at(:a).attr(:href)

  record = {
    title: submission.inner_text,
    link: link,
    date: Date.today,
    description: "FOI submission by #{submission.inner_text}: #{link}"
  }

  if (ScraperWiki.select("* from swdata where `link`='#{record[:link]}'").empty? rescue true)
    ScraperWiki.save_sqlite([:link], record)
  else
    puts "Skipping already saved record with link " + record[:link]
  end
end
require 'mechanize'

agent = Mechanize.new
base_url = 'http://www.ag.gov.au'

page = agent.get "#{base_url}/Consultationsreformsandreviews/Pages/ReviewofFOIlaws.aspx"

submissions = page.at('#ctl00_PlaceHolderMain_ctl01_ctl02__ControlWrapper_RichHtmlField').search(:ul)[1].search(:li)

submissions.each do |submission|
  link = base_url + submission.at(:a).attr(:href)

  record = {
    title: submission.inner_text,
    link: link,
    date: Date.today,
    description: "FOI submission by #{submission.inner_text}: #{link}"
  }

  if (ScraperWiki.select("* from swdata where `link`='#{record[:link]}'").empty? rescue true)
    ScraperWiki.save_sqlite([:link], record)
  else
    puts "Skipping already saved record with link " + record[:link]
  end
end
require 'mechanize'

agent = Mechanize.new
base_url = 'http://www.ag.gov.au'

page = agent.get "#{base_url}/Consultationsreformsandreviews/Pages/ReviewofFOIlaws.aspx"

submissions = page.at('#ctl00_PlaceHolderMain_ctl01_ctl02__ControlWrapper_RichHtmlField').search(:ul)[1].search(:li)

submissions.each do |submission|
  link = base_url + submission.at(:a).attr(:href)

  record = {
    title: submission.inner_text,
    link: link,
    date: Date.today,
    description: "FOI submission by #{submission.inner_text}: #{link}"
  }

  if (ScraperWiki.select("* from swdata where `link`='#{record[:link]}'").empty? rescue true)
    ScraperWiki.save_sqlite([:link], record)
  else
    puts "Skipping already saved record with link " + record[:link]
  end
end
