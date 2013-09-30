require 'nokogiri' 

def genUrl(okres,obec,cobec,ulice,cisPop,psc)
   return "http://psc.ceskaposta.cz/eep_psc/GetSearch.action" +
    "?volani=href" + 
    "&formOkres="  + CGI::escape( okres.to_s()) + 
    "&formObec="   + CGI::escape(  obec.to_s()) + 
    "&formCobec="  + CGI::escape( cobec.to_s()) + 
    "&formUlice="  + CGI::escape( ulice.to_s()) + 
    "&formCisPop=" + CGI::escape(cisPop.to_s()) + 
    "&formPsc="    + CGI::escape(   psc.to_s())
end

def editUrl(url)
  return url.sub(/;jsessionid=[0-9a-f]*/,"")
            .sub(/\/\?/,"GetSearch.action?action:GetSearch=Vyhledat&")
end

# Returns all pages reachable via 'Page 2' etc.
def pages(url)
  urls = Array.new
  data = Array.new 
  data << Nokogiri::HTML(ScraperWiki.scrape(url))
  data[0].css('p.pages a').each do |link|
    urls << editUrl(link.attribute("href").to_s())
  end

  urls.uniq.each do |link|
    data << Nokogiri::HTML(ScraperWiki.scrape(link))
  end

  return data
end


#ScraperWiki.sqliteexecute("DROP TABLE IF EXISTS okres")
#ScraperWiki.sqliteexecute("DROP TABLE IF EXISTS mesto")
#ScraperWiki.sqliteexecute("DROP TABLE IF EXISTS ulice")
#ScraperWiki.sqliteexecute("DROP TABLE IF EXISTS cobec")


mid = 0
uid = 0
cid = 0

def saveOkres(okres) {
  ScraperWiki::save_sqlite(
    unique_keys=['oid'],
    data=okres,
    table_name="okres"
  )
}

def saveMesto(mesto) {
  ScraperWiki::save_sqlite(
    unique_keys=['oid','mid'],
    data=mesto,
    table_name="mesto"
  )
}

Nokogiri::HTML(ScraperWiki.scrape("http://psc.ceskaposta.cz/CleanForm.action"))
  .css('select#okres option').each do |okresNode|

  saveOkres({
    'oid'  => Integer(okresNode['value']),
    'name' => okresNode.inner_html,
    'done' => false
  })
end

ScraperWiki.select("* FROM okres WHERE done=false").each do |okres|
  puts("okres#" + okres['oid'].to_s() + " = " + okres['name'])

  mesta = Array.new
  pages(genUrl(okres['oid'],"","","","","")).each do |page|
    page.css("table#row td:nth-child(2) a:nth-child(1)").each do |row|
      mesta << row.inner_html
    end
  end
  
  mid = 0
  mesta.uniq.each do |mestoName|
    saveMesto({
      'oid' => okres['oid'],
      'mid' => (mid = mid + 1),
      'name' => mestoName,
    })
  end

  okres['done'] = true;
  saveOkres(okres);
end


ScraperWiki.select("* from mesto").each do |mesto|
  puts("mesto#" + mesto['mid'].to_s() + " = " + mesto['name'])

  casti = Array.new
  url = genUrl(mesto['oid'],mesto['name'],"","","","")
  pages(url).each do |page|
    page.css("table#row td:nth-child(3) a:nth-child(1)").each do |row|
      casti << row.inner_html
    end
  end

  casti = casti.uniq
  casti.each do |castName|
    cobec = {
      'cid'  => (cid = cid + 1),
      'name' => castName,
      'mid'  => mesto['mid'],
    }
    ScraperWiki.save_sqlite(
      unique_keys=['cid'],
      data=cobec,
      table_name="cobec"
    )

    ulice = Array.new
    pages(genUrl(mesto['oid'],mesto['name'],cobec['name'],"","","")).each do |page|
      page.css("table#row td:nth-child(4) a:nth-child(1)").each do |row|
        ulice << row.inner_html
      end
    end

    ulice = ulice.uniq
    ulice.each do |ulicName|
      ulic = {
        'uid'  => (uid = uid + 1),
        'name' => ulicName,
        'cid'  => cobec['cid'],
      }
      ScraperWiki.save_sqlite(
        unique_keys=['uid'],
        data=ulic,
        table_name="ulice"
      )
    end
  end
end

require 'nokogiri' 

def genUrl(okres,obec,cobec,ulice,cisPop,psc)
   return "http://psc.ceskaposta.cz/eep_psc/GetSearch.action" +
    "?volani=href" + 
    "&formOkres="  + CGI::escape( okres.to_s()) + 
    "&formObec="   + CGI::escape(  obec.to_s()) + 
    "&formCobec="  + CGI::escape( cobec.to_s()) + 
    "&formUlice="  + CGI::escape( ulice.to_s()) + 
    "&formCisPop=" + CGI::escape(cisPop.to_s()) + 
    "&formPsc="    + CGI::escape(   psc.to_s())
end

def editUrl(url)
  return url.sub(/;jsessionid=[0-9a-f]*/,"")
            .sub(/\/\?/,"GetSearch.action?action:GetSearch=Vyhledat&")
end

# Returns all pages reachable via 'Page 2' etc.
def pages(url)
  urls = Array.new
  data = Array.new 
  data << Nokogiri::HTML(ScraperWiki.scrape(url))
  data[0].css('p.pages a').each do |link|
    urls << editUrl(link.attribute("href").to_s())
  end

  urls.uniq.each do |link|
    data << Nokogiri::HTML(ScraperWiki.scrape(link))
  end

  return data
end


#ScraperWiki.sqliteexecute("DROP TABLE IF EXISTS okres")
#ScraperWiki.sqliteexecute("DROP TABLE IF EXISTS mesto")
#ScraperWiki.sqliteexecute("DROP TABLE IF EXISTS ulice")
#ScraperWiki.sqliteexecute("DROP TABLE IF EXISTS cobec")


mid = 0
uid = 0
cid = 0

def saveOkres(okres) {
  ScraperWiki::save_sqlite(
    unique_keys=['oid'],
    data=okres,
    table_name="okres"
  )
}

def saveMesto(mesto) {
  ScraperWiki::save_sqlite(
    unique_keys=['oid','mid'],
    data=mesto,
    table_name="mesto"
  )
}

Nokogiri::HTML(ScraperWiki.scrape("http://psc.ceskaposta.cz/CleanForm.action"))
  .css('select#okres option').each do |okresNode|

  saveOkres({
    'oid'  => Integer(okresNode['value']),
    'name' => okresNode.inner_html,
    'done' => false
  })
end

ScraperWiki.select("* FROM okres WHERE done=false").each do |okres|
  puts("okres#" + okres['oid'].to_s() + " = " + okres['name'])

  mesta = Array.new
  pages(genUrl(okres['oid'],"","","","","")).each do |page|
    page.css("table#row td:nth-child(2) a:nth-child(1)").each do |row|
      mesta << row.inner_html
    end
  end
  
  mid = 0
  mesta.uniq.each do |mestoName|
    saveMesto({
      'oid' => okres['oid'],
      'mid' => (mid = mid + 1),
      'name' => mestoName,
    })
  end

  okres['done'] = true;
  saveOkres(okres);
end


ScraperWiki.select("* from mesto").each do |mesto|
  puts("mesto#" + mesto['mid'].to_s() + " = " + mesto['name'])

  casti = Array.new
  url = genUrl(mesto['oid'],mesto['name'],"","","","")
  pages(url).each do |page|
    page.css("table#row td:nth-child(3) a:nth-child(1)").each do |row|
      casti << row.inner_html
    end
  end

  casti = casti.uniq
  casti.each do |castName|
    cobec = {
      'cid'  => (cid = cid + 1),
      'name' => castName,
      'mid'  => mesto['mid'],
    }
    ScraperWiki.save_sqlite(
      unique_keys=['cid'],
      data=cobec,
      table_name="cobec"
    )

    ulice = Array.new
    pages(genUrl(mesto['oid'],mesto['name'],cobec['name'],"","","")).each do |page|
      page.css("table#row td:nth-child(4) a:nth-child(1)").each do |row|
        ulice << row.inner_html
      end
    end

    ulice = ulice.uniq
    ulice.each do |ulicName|
      ulic = {
        'uid'  => (uid = uid + 1),
        'name' => ulicName,
        'cid'  => cobec['cid'],
      }
      ScraperWiki.save_sqlite(
        unique_keys=['uid'],
        data=ulic,
        table_name="ulice"
      )
    end
  end
end

