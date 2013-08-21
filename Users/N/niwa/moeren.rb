# Blank Ruby
require 'nokogiri'
require 'mechanize'
require 'kconv'

agent = Mechanize.new
#agent.user_agent_alias = ''
agent.get("http://www.nijibox3.com/moeren/uploader/all.html?view=list&order=0")
doc = Nokogiri::HTML(agent.page.body)

doc.root.search('table/tr').map{|e|
  cells = e.search('td')
  
  if(cells.length > 4)
    url = ""
    file_name = ""

    cells[1].search('a').map{|link|
      file_path = link[:href].to_s
      #remove garbage of file_path ( ./src/filename.png.html : "." and ".html")
      file_path = file_path.slice(1,file_path.length-6)
      file_name = file_path.slice(5,11)
      url = "http://www.nijibox3.com/moeren/uploader" + file_path
    }
    
    data = {
      'file_name' => file_name,
      'url' => url,
      'comment' => cells[2].inner_html.toutf8,
      'size' => cells[3].inner_html,
      'date' => cells[4].inner_html
    } 
  end

  ScraperWiki.save_sqlite(unique_keys=['file_name'], data=data)
}
