require 'hpricot'

rossiSite = "http://www.rossiboots.com.au/catalogue/catalogue_browse.asp?"
cataloguePages = ["deptID=3&subDeptID=4", "deptID=3&subDeptID=5", "deptID=3&subDeptID=6", "deptID=3&subDeptID=7",
                  "deptID=7&Page=1", "deptID=7&Page=2",
                  "deptID=11",
                  "deptID=15",
                  "deptID=8",
                  "deptID=9",
                  "deptID=6",
                  "deptID=14",
                  "deptID=17"
]

cataloguePages.each do |pageUri|
  doc = Hpricot(ScraperWiki::scrape(rossiSite + pageUri))

  doc.search("//td[@class='catProdNameSmall']/../../../table").each do |v|
    puts v.search("tr/td/div/a").first['href']
    data = {
      name: v.search("td[@class='catProdNameSmall']").text,
      #url: v.search("td[@class='catMoreDetailSmall']/a/@href"),
      url: v.search("tr/td/div/a").first['href'],
      category: pageUri
    }
    puts data.to_json
    # primary key should be 'url'. products with duplicate names may exist
    ScraperWiki::save_sqlite(['name'], data)
  end
end

  

require 'hpricot'

rossiSite = "http://www.rossiboots.com.au/catalogue/catalogue_browse.asp?"
cataloguePages = ["deptID=3&subDeptID=4", "deptID=3&subDeptID=5", "deptID=3&subDeptID=6", "deptID=3&subDeptID=7",
                  "deptID=7&Page=1", "deptID=7&Page=2",
                  "deptID=11",
                  "deptID=15",
                  "deptID=8",
                  "deptID=9",
                  "deptID=6",
                  "deptID=14",
                  "deptID=17"
]

cataloguePages.each do |pageUri|
  doc = Hpricot(ScraperWiki::scrape(rossiSite + pageUri))

  doc.search("//td[@class='catProdNameSmall']/../../../table").each do |v|
    puts v.search("tr/td/div/a").first['href']
    data = {
      name: v.search("td[@class='catProdNameSmall']").text,
      #url: v.search("td[@class='catMoreDetailSmall']/a/@href"),
      url: v.search("tr/td/div/a").first['href'],
      category: pageUri
    }
    puts data.to_json
    # primary key should be 'url'. products with duplicate names may exist
    ScraperWiki::save_sqlite(['name'], data)
  end
end

  

