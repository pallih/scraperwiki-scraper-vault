require 'nokogiri'

xml = ScraperWiki::scrape("http://data.parliament.uk/briefingpapers/PublisherService.svc/briefingpapers")
       # why only twenty results?
@doc = Nokogiri::XML(xml)

@doc.xpath("//Document").each do |document|
  
  data = {
      authors: ['DummyAuthor1', 'DummyAuthor2'],
      document_type: document.xpath('DocumentType').text,
      last_published_date: document.xpath('LastPublishedDate').text,
      last_updated_date: document.xpath('LastUpdatedDate').text,
      link: document.xpath('Link').text,
      publisher_id: document.xpath('Publisher/Id').text,
      publisher_value: document.xpath('Publisher/Value').text,

      sections: ['DummySection1', 'DummySection2'],

      reference: document.xpath('Reference').text,
      status: document.xpath('Status').text,
      teaser_text: document.xpath('TeaserText').text,
      subjects: ['DummySubject1', 'DummySubject2'],
      summary: document.xpath('Summary').text,

      title: document.xpath('Title').text,
      version: document.xpath('Version').text,

    }
    #document.xpath('Authors/Author').each do |author|
    #  data['email'] = author.xpath('Email').text
    #end
    ScraperWiki::save_sqlite(['reference'], data)
end
require 'nokogiri'

xml = ScraperWiki::scrape("http://data.parliament.uk/briefingpapers/PublisherService.svc/briefingpapers")
       # why only twenty results?
@doc = Nokogiri::XML(xml)

@doc.xpath("//Document").each do |document|
  
  data = {
      authors: ['DummyAuthor1', 'DummyAuthor2'],
      document_type: document.xpath('DocumentType').text,
      last_published_date: document.xpath('LastPublishedDate').text,
      last_updated_date: document.xpath('LastUpdatedDate').text,
      link: document.xpath('Link').text,
      publisher_id: document.xpath('Publisher/Id').text,
      publisher_value: document.xpath('Publisher/Value').text,

      sections: ['DummySection1', 'DummySection2'],

      reference: document.xpath('Reference').text,
      status: document.xpath('Status').text,
      teaser_text: document.xpath('TeaserText').text,
      subjects: ['DummySubject1', 'DummySubject2'],
      summary: document.xpath('Summary').text,

      title: document.xpath('Title').text,
      version: document.xpath('Version').text,

    }
    #document.xpath('Authors/Author').each do |author|
    #  data['email'] = author.xpath('Email').text
    #end
    ScraperWiki::save_sqlite(['reference'], data)
end
