require 'csv'

txt = "bridge,designer,length
Brooklyn,J. A. Roebling,1595
Williamsburg,D. Duck,1600
Queensborough,Palmer & Hornbostel,1182
Triborough,O. H. Ammann,\"1380,383\"
Bronx Whitestone,O. H. Ammann,2300
Throgs Neck,O. H. Ammann,1800
George Washington,O. H. Ammann,3500
Spamspan,S. Spamington,10000
"

txt2 = "bridge,designer,length
Brooklyn,J. A. Roebling,1595
Manhattan,G. Lindenthal,1470
Williamsburg,L. L. Buck,1600
Queensborough,Palmer & Hornbostel,1182
Triborough,O. H. Ammann,\"1380,383\"
Bronx Whitestone,O. H. Ammann,2300
Throgs Neck,O. H. Ammann,1800
George Washington,O. H. Ammann,3500
"

txt3 = txt2

setup = false

if setup
  CSV.parse(txt, :headers => true).each do |row|
    puts "#{row.inspect}"
    ScraperWiki.save_sqlite(['bridge'],row.to_hash,"broken_bridge")
  end
  
  CSV.parse(txt2, :headers => true).each do |row|
    puts "#{row.inspect}"
    ScraperWiki.save_sqlite(['bridge'],row.to_hash,"bridge")
  end
  
  CSV.parse(txt3, :headers => true).each do |row|
    puts "#{row.inspect}"
    ScraperWiki.save_sqlite(['bridge'],row.to_hash,"bridge_evolve")
  end
else
  ct = ScraperWiki.get_var("mod_count") || 0
  ct = ct+1
  ScraperWiki.save_var("mod_count",ct)
  ScraperWiki.sqliteexecute("UPDATE bridge_evolve SET length = ? WHERE bridge = ?",[ct,"Throgs Neck"])
  ScraperWiki.commit()
end
require 'csv'

txt = "bridge,designer,length
Brooklyn,J. A. Roebling,1595
Williamsburg,D. Duck,1600
Queensborough,Palmer & Hornbostel,1182
Triborough,O. H. Ammann,\"1380,383\"
Bronx Whitestone,O. H. Ammann,2300
Throgs Neck,O. H. Ammann,1800
George Washington,O. H. Ammann,3500
Spamspan,S. Spamington,10000
"

txt2 = "bridge,designer,length
Brooklyn,J. A. Roebling,1595
Manhattan,G. Lindenthal,1470
Williamsburg,L. L. Buck,1600
Queensborough,Palmer & Hornbostel,1182
Triborough,O. H. Ammann,\"1380,383\"
Bronx Whitestone,O. H. Ammann,2300
Throgs Neck,O. H. Ammann,1800
George Washington,O. H. Ammann,3500
"

txt3 = txt2

setup = false

if setup
  CSV.parse(txt, :headers => true).each do |row|
    puts "#{row.inspect}"
    ScraperWiki.save_sqlite(['bridge'],row.to_hash,"broken_bridge")
  end
  
  CSV.parse(txt2, :headers => true).each do |row|
    puts "#{row.inspect}"
    ScraperWiki.save_sqlite(['bridge'],row.to_hash,"bridge")
  end
  
  CSV.parse(txt3, :headers => true).each do |row|
    puts "#{row.inspect}"
    ScraperWiki.save_sqlite(['bridge'],row.to_hash,"bridge_evolve")
  end
else
  ct = ScraperWiki.get_var("mod_count") || 0
  ct = ct+1
  ScraperWiki.save_var("mod_count",ct)
  ScraperWiki.sqliteexecute("UPDATE bridge_evolve SET length = ? WHERE bridge = ?",[ct,"Throgs Neck"])
  ScraperWiki.commit()
end
