# Test of monkeypatching require

# TODO: I can't find where include is yet, so probably just don't support that for now

require 'uri'
require 'net/http'
require 'tempfile'

module Kernel
  alias_method :sw_old_require, :require
 
  def require(f)
    begin
       return sw_old_require(f)
    rescue LoadError
       puts "this is using ScraperWiki's magic require!"

       # don't include same thing twice - we can't rely on the underlying
       # require for this as we have a random tmp filename.
       @sw_require_already_done = {} if @sw_require_already_done.nil? 
       if @sw_require_already_done[f]
         return
       end
       
       # get the included library from its codewiki
       uri  = URI.parse("http://scraperwiki.com/editor/raw/" + f)
       content = Net::HTTP.get(uri)

       # save it to a temporary file
       tmp = Tempfile.new(['sw_ruby_require', '.rb'])
       newf = tmp.path
       tmp << content
       tmp.close
       # puts newf

       # include it
       sw_old_require(newf)
       @sw_require_already_done[f] = true
    end
  end
end

require "nokogiri"
require "ruby_library"

hello_library()

# require again to make sure it doesn't import again (no second print)
require "ruby_library"

