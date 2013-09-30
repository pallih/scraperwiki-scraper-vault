require 'scraperwiki'

ScraperWiki::sqliteexecute 'create table if not exists [Pack my box with five dozen liquor jugs.] (hand gloves)'
ScraperWiki::sqliteexecute 'create table if not exists [Packmyboxwithfivedozenliquorjugs.] (hand gloves)'
ScraperWiki::sqliteexecute 'create table if not exists [The xylophone orchestra vowed to imbibe jugs of kumquat fizz.] (xylophone orchestra)'

ScraperWiki::sqliteexecute 'insert into [Pack my box with five dozen liquor jugs.] VALUES (1)'
ScraperWiki::sqliteexecute 'insert into [Pack my box with five dozen liquor jugs.] VALUES (2)'
ScraperWiki::sqliteexecute 'insert into [Pack my box with five dozen liquor jugs.] VALUES (3)'

ScraperWiki::sqliteexecute 'insert into [The xylophone orchestra vowed to imbibe jugs of kumquat fizz.] VALUES (4)'
ScraperWiki::sqliteexecute 'insert into [The xylophone orchestra vowed to imbibe jugs of kumquat fizz.] VALUES (5)'
ScraperWiki::sqliteexecute 'insert into [The xylophone orchestra vowed to imbibe jugs of kumquat fizz.] VALUES (6)'

ScraperWiki::commit

puts ScraperWiki::select('* from sqlite_master')
puts ScraperWiki::select('* from [Pack my box with five dozen liquor jugs.]')require 'scraperwiki'

ScraperWiki::sqliteexecute 'create table if not exists [Pack my box with five dozen liquor jugs.] (hand gloves)'
ScraperWiki::sqliteexecute 'create table if not exists [Packmyboxwithfivedozenliquorjugs.] (hand gloves)'
ScraperWiki::sqliteexecute 'create table if not exists [The xylophone orchestra vowed to imbibe jugs of kumquat fizz.] (xylophone orchestra)'

ScraperWiki::sqliteexecute 'insert into [Pack my box with five dozen liquor jugs.] VALUES (1)'
ScraperWiki::sqliteexecute 'insert into [Pack my box with five dozen liquor jugs.] VALUES (2)'
ScraperWiki::sqliteexecute 'insert into [Pack my box with five dozen liquor jugs.] VALUES (3)'

ScraperWiki::sqliteexecute 'insert into [The xylophone orchestra vowed to imbibe jugs of kumquat fizz.] VALUES (4)'
ScraperWiki::sqliteexecute 'insert into [The xylophone orchestra vowed to imbibe jugs of kumquat fizz.] VALUES (5)'
ScraperWiki::sqliteexecute 'insert into [The xylophone orchestra vowed to imbibe jugs of kumquat fizz.] VALUES (6)'

ScraperWiki::commit

puts ScraperWiki::select('* from sqlite_master')
puts ScraperWiki::select('* from [Pack my box with five dozen liquor jugs.]')