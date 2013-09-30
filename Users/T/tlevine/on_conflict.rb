# Demonstration of http://sqlite.org/lang_conflict.html
require 'scraperwiki'

for on_conflict in ['scraperwiki_default', 'ROLLBACK', 'ABORT', 'FAIL', 'IGNORE', 'REPLACE']
  ScraperWiki::sqliteexecute("DROP TABLE IF EXISTS #{on_conflict};")
  if on_conflict == 'scraperwiki_default'
    ScraperWiki::sqliteexecute("CREATE TABLE #{on_conflict} (bar TEXT, insertion_number BLOB, UNIQUE(bar));")
  else
    ScraperWiki::sqliteexecute("CREATE TABLE #{on_conflict} (bar TEXT, insertion_number BLOB, UNIQUE(bar) ON CONFLICT #{on_conflict});")
  end
  ScraperWiki::sqliteexecute("INSERT INTO #{on_conflict} VALUES ('chainsaw', 1);")
  ScraperWiki::commit()

  # Begin a transaction. (This might not work because of ScraperWiki weirdness.)
  ScraperWiki::sqliteexecute("INSERT INTO #{on_conflict} VALUES ('articulating dump truck', 0);")
  ScraperWiki::sqliteexecute("INSERT INTO #{on_conflict} VALUES ('vibratory soil compactor', 0);")
  ScraperWiki::sqliteexecute("INSERT INTO #{on_conflict} VALUES ('motor grader', 0);")

  # Insert a conflicting row
  begin
    ScraperWiki::sqliteexecute("INSERT INTO #{on_conflict} VALUES ('chainsaw', 2);")
  rescue SqliteException => msg
    ScraperWiki::sqliteexecute("INSERT INTO #{on_conflict} VALUES ('error', '#{msg}')")
    puts "Error with #{on_conflict} conflict-handling: #{msg}"
  else
    ScraperWiki::sqliteexecute("INSERT INTO #{on_conflict} VALUES ('no error', '')")
  end
  ScraperWiki::commit()
end# Demonstration of http://sqlite.org/lang_conflict.html
require 'scraperwiki'

for on_conflict in ['scraperwiki_default', 'ROLLBACK', 'ABORT', 'FAIL', 'IGNORE', 'REPLACE']
  ScraperWiki::sqliteexecute("DROP TABLE IF EXISTS #{on_conflict};")
  if on_conflict == 'scraperwiki_default'
    ScraperWiki::sqliteexecute("CREATE TABLE #{on_conflict} (bar TEXT, insertion_number BLOB, UNIQUE(bar));")
  else
    ScraperWiki::sqliteexecute("CREATE TABLE #{on_conflict} (bar TEXT, insertion_number BLOB, UNIQUE(bar) ON CONFLICT #{on_conflict});")
  end
  ScraperWiki::sqliteexecute("INSERT INTO #{on_conflict} VALUES ('chainsaw', 1);")
  ScraperWiki::commit()

  # Begin a transaction. (This might not work because of ScraperWiki weirdness.)
  ScraperWiki::sqliteexecute("INSERT INTO #{on_conflict} VALUES ('articulating dump truck', 0);")
  ScraperWiki::sqliteexecute("INSERT INTO #{on_conflict} VALUES ('vibratory soil compactor', 0);")
  ScraperWiki::sqliteexecute("INSERT INTO #{on_conflict} VALUES ('motor grader', 0);")

  # Insert a conflicting row
  begin
    ScraperWiki::sqliteexecute("INSERT INTO #{on_conflict} VALUES ('chainsaw', 2);")
  rescue SqliteException => msg
    ScraperWiki::sqliteexecute("INSERT INTO #{on_conflict} VALUES ('error', '#{msg}')")
    puts "Error with #{on_conflict} conflict-handling: #{msg}"
  else
    ScraperWiki::sqliteexecute("INSERT INTO #{on_conflict} VALUES ('no error', '')")
  end
  ScraperWiki::commit()
end