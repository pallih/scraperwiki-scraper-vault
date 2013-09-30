# Blank Ruby

#!/usr/bin/ruby

require 'nokogiri'
require 'open-uri'
require 'json'

body = open('http://www.himasali.com/lounaslista/').read;
html = Nokogiri::parse(body);

html.search("//div[@id='content']/p").each{|node|
        text = node.text
        text.gsub!(/\n\n/, "\n");
        if(text =~ /^(\d+)\.(\d+)\.\n(.*)/m)
                date = sprintf("#{Time.now.year}-%02d-%02d", $2, $1);
                menutext = $3;
                menutext.gsub!(/([^\d])\n(.*\d+,\d\d)/) {"#{$1} #{$2}"}; 
                menulines = menutext.split(/\n/);
                menulines.each{|line|
                        if(line =~ /^(.*)\s*(\d+),(\d+)$/) then
                                doc_item = {
                                        "title" => $1 ,
                                        "price" => "#{$2}.#{$3}",
                                        "date" => date,
                                }
                                ScraperWiki::save_sqlite(['date', 'title'], doc_item)
                        end
                }
        end
}

# Blank Ruby

#!/usr/bin/ruby

require 'nokogiri'
require 'open-uri'
require 'json'

body = open('http://www.himasali.com/lounaslista/').read;
html = Nokogiri::parse(body);

html.search("//div[@id='content']/p").each{|node|
        text = node.text
        text.gsub!(/\n\n/, "\n");
        if(text =~ /^(\d+)\.(\d+)\.\n(.*)/m)
                date = sprintf("#{Time.now.year}-%02d-%02d", $2, $1);
                menutext = $3;
                menutext.gsub!(/([^\d])\n(.*\d+,\d\d)/) {"#{$1} #{$2}"}; 
                menulines = menutext.split(/\n/);
                menulines.each{|line|
                        if(line =~ /^(.*)\s*(\d+),(\d+)$/) then
                                doc_item = {
                                        "title" => $1 ,
                                        "price" => "#{$2}.#{$3}",
                                        "date" => date,
                                }
                                ScraperWiki::save_sqlite(['date', 'title'], doc_item)
                        end
                }
        end
}

# Blank Ruby

#!/usr/bin/ruby

require 'nokogiri'
require 'open-uri'
require 'json'

body = open('http://www.himasali.com/lounaslista/').read;
html = Nokogiri::parse(body);

html.search("//div[@id='content']/p").each{|node|
        text = node.text
        text.gsub!(/\n\n/, "\n");
        if(text =~ /^(\d+)\.(\d+)\.\n(.*)/m)
                date = sprintf("#{Time.now.year}-%02d-%02d", $2, $1);
                menutext = $3;
                menutext.gsub!(/([^\d])\n(.*\d+,\d\d)/) {"#{$1} #{$2}"}; 
                menulines = menutext.split(/\n/);
                menulines.each{|line|
                        if(line =~ /^(.*)\s*(\d+),(\d+)$/) then
                                doc_item = {
                                        "title" => $1 ,
                                        "price" => "#{$2}.#{$3}",
                                        "date" => date,
                                }
                                ScraperWiki::save_sqlite(['date', 'title'], doc_item)
                        end
                }
        end
}

# Blank Ruby

#!/usr/bin/ruby

require 'nokogiri'
require 'open-uri'
require 'json'

body = open('http://www.himasali.com/lounaslista/').read;
html = Nokogiri::parse(body);

html.search("//div[@id='content']/p").each{|node|
        text = node.text
        text.gsub!(/\n\n/, "\n");
        if(text =~ /^(\d+)\.(\d+)\.\n(.*)/m)
                date = sprintf("#{Time.now.year}-%02d-%02d", $2, $1);
                menutext = $3;
                menutext.gsub!(/([^\d])\n(.*\d+,\d\d)/) {"#{$1} #{$2}"}; 
                menulines = menutext.split(/\n/);
                menulines.each{|line|
                        if(line =~ /^(.*)\s*(\d+),(\d+)$/) then
                                doc_item = {
                                        "title" => $1 ,
                                        "price" => "#{$2}.#{$3}",
                                        "date" => date,
                                }
                                ScraperWiki::save_sqlite(['date', 'title'], doc_item)
                        end
                }
        end
}

