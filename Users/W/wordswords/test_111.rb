require 'open-uri'
require 'nokogiri'
queries=['ruby']
locations=['manchester']

for query in queries
  for location in locations
    print "Now finding jobs on indeed.co.uk for #{query} in #{location} \n"
    start=0
    catch (:done) do
      loop do
        queryurl="http://www.indeed.co.uk/jobs?q="+query+"&l="+location+"&start="+start.to_s+"&filter=0"
        sleep 1.5
        doc = Nokogiri::HTML(open(queryurl))

        doc.search("div[@class = 'row ']").each do |row|

          jobtitle = ''
          href = ''
          summary = ''
          date = ''
          address = ''
  
          row.search("h2[@class = 'jobtitle']").each do |node|
           jobtitle = node.inner_text
           
           node.search("a").each do |link|
             href = "http://www.indeed.co.uk" + link['href']
           end
          end
  
          row.search("span[@class = 'summary']").each do |node|
            summary = node.inner_text
          end

          row.search("span[@class = 'date']").each do |node|
            date = node.inner_text
          end
  
          row.search("span[@itemprop = 'addressLocality']").each do |node|
            address = node.inner_text
          end

          data={
              title: jobtitle,
              link: href,
              date: date,
              address: address,
              summary: summary
          }
  
          ScraperWiki::save_sqlite(['link'], data)

        end
            
        doc.search("//div[@id = 'searchCount']").each do |node|
          print node.inner_text + "\n"
          total_count = node.inner_text.split[-1].to_i
          print "Total Count = " + total_count.to_s + "\n"
          
            if start.to_i > total_count
              print "We're done. reached #{total_count}\n"
              throw :done
            end
        end
    
        start=start+10
      end
    end
  end
end

