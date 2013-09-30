require 'typhoeus'
require 'nokogiri'

module Page
  include Typhoeus
  include Nokogiri  

  HYDRA = Hydra.new

  def self.request(uri, opts = {})
    request = Request.new(uri, opts)
    
    request.on_complete do |response|
      if response.success? 
        parse(response.body)
      else
        raise RequestFailure, "requested uri:#{response.request.url} status:#{response.code}"
      end
    end

    queue request
  end

  def self.parse(html)
    HTML.parse(html).xpath("//text()").each { |t| puts t.text }
  end

  def self.queue(request)
    HYDRA.queue request
  end

  def self.run!
    HYDRA.run 
  end

  class RequestFailure < StandardError; end
end

include Page

["http://www.google.com", "http://www.yahoo.com/"].each do |uri|
  Page.request(uri, :follow_location => true)
end

Page.run!require 'typhoeus'
require 'nokogiri'

module Page
  include Typhoeus
  include Nokogiri  

  HYDRA = Hydra.new

  def self.request(uri, opts = {})
    request = Request.new(uri, opts)
    
    request.on_complete do |response|
      if response.success? 
        parse(response.body)
      else
        raise RequestFailure, "requested uri:#{response.request.url} status:#{response.code}"
      end
    end

    queue request
  end

  def self.parse(html)
    HTML.parse(html).xpath("//text()").each { |t| puts t.text }
  end

  def self.queue(request)
    HYDRA.queue request
  end

  def self.run!
    HYDRA.run 
  end

  class RequestFailure < StandardError; end
end

include Page

["http://www.google.com", "http://www.yahoo.com/"].each do |uri|
  Page.request(uri, :follow_location => true)
end

Page.run!