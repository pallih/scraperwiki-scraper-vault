# Blank Ruby

require 'open-uri'
require 'nokogiri'
require 'pp'

body = open('http://www.ravintolafaro.fi/lounaslista.html').read;
html = Nokogiri.parse(body);

@title1=""
@title2=""
@alltext = "";
html.search("//div[@class='cushycms']/div/strong").each{|node2|
        #   rint "name=", node.name, "text1=", node, "\n"
        # if(node.name == "strong")then
               print "text=", node2.text, "\n"
               @alltext = @alltext + " " + node2.text ;
        if(false) then
        #        node.children.each{|node2|
                        text = node2.text
                        text.gsub!(/^\s*(.*)\s*$/){$1}
                        if(text =~ /lounas (\d+)\.(\d+)\.(\d+)/)then
                                @date = "%04d-%02d-%02d" % [$3, $2, $1]
                        elsif(text =~ /^(Keitto|Liha|Kala|Kasvis)([^\w]|$)/)then
                                @title1 = $1
                                @title2 = ""
                        elsif(text =~ /^Pieni\s*(\d+),(\d\d)\s*\/\s*Iso\s*(\d+),(\d\d)$/)then
                                price1 = "#{$1}.#{$2}"
                                price2 = "#{$3}.#{$4}"
                                data = {date: @date, title: "#{@title1}: #{@title2} Pieni", price: price1}
                                ScraperWiki::save_sqlite(['date','title'], data)
                                data = {date: @date, title: "#{@title1}: #{@title2} Iso", price: price2}
                                ScraperWiki::save_sqlite(['date','title'], data)
                        elsif(text =~ /^(\d+),(\d\d)$/)then
                                price = "#{$1}.#{$2}"
                                data = {date: @date, title: "#{@title1}: #{@title2}", price: price}
                                ScraperWiki::save_sqlite(['date','title'], data)
                        else
                                @title2 += text
                        end
        end
        #       }
        # else
        #        if(node.class == Nokogiri::XML::Text)then
        #                @title2 += node.text
        #                @title2.gsub!(/^\s*(.*)\s*$/){$1}
        #        end
        # end
}
print "alltext: #{@alltext}\n"


@alltext.match(/lounas (\d+)\.(\d+)\.(\d+)/i){
  @date = "%04d-%02d-%02d" % [$3, $2, $1];
}

@alltext.scan(/(Keitto) *([^\d]+) *Pieni\s*(\d+),(\d\d)\s*\/\s*Iso\s*(\d+),(\d\d)/){
  @title1 = $1
  @title2 = $2
  price = "#{$3},#{$4}";
  data = {date: @date, title: "#{@title1}: #{@title2} Pieni", price: price}
  ScraperWiki::save_sqlite(['date', 'title'], data);
  price = "#{$5},#{$6}";
  data = {date: @date, title: "#{@title1}: #{@title2} Iso", price: price}
  ScraperWiki::save_sqlite(['date', 'title'], data);
}

#@alltext.scan(/(Liha|Kala|Kasvis) *([^\d]+) *(\d+),(\d+)/){
#  @title1 = $1
#  @title2 = $2
#  price = "#{$3},#{$4}";
#  data = {date: @date, title: "#{@title1}: #{@title2}", price: price}
#  ScraperWiki::save_sqlite(['date', 'title'], data);
#}

@alltext.scan(/\s*([^\d]*)\s+([^\d]+) *(\d+),(\d+)/){
  @title1 = $1
  @title2 = $2
  price = "#{$3},#{$4}";
  data = {date: @date, title: "#{@title1}: #{@title2}", price: price}
  ScraperWiki::save_sqlite(['date', 'title'], data);
}
