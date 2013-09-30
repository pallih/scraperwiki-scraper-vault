<?php
# first time through, create tables and indices


$urls = array(
  'boy_names'=>'http://www.census.gov/genealogy/names/dist.male.first',
  'girl_names'=>'http://www.census.gov/genealogy/names/dist.female.first',
  'last_names'=>'http://www.census.gov/genealogy/names/dist.all.last'
);

foreach ($urls as $table=>$url) {
  # first time through, create tables and indices
  scraperwiki::sqliteexecute("drop table if exists $table");
 
  scraperwiki::sqliteexecute("create table $table (rank INTEGER PRIMARY KEY, `name` string, freq INTEGER, cumulative_freq INTEGER)");
  // scraperwiki::sqliteexecute("create unique index ${table}rank on $table (rank)");
  scraperwiki::sqliteexecute("create unique index `{$table}name` on $table (name)");
  scraperwiki::sqliteexecute("create index {$table}cumulative_freq on $table (cumulative_freq)");

  $data = scraperWiki::scrape($url);
  foreach (explode("\n", $data) as $s) {
     // hack, should really use readf or scanf something like that
     list($name, $freq, $total_freq, $rank) = explode(' ', preg_replace('{ +}', ' ', $s));
     if (!empty($name))
         scraperwiki::sqliteexecute("insert into $table values (?,?,?,?)", array($rank, ucfirst(strtolower($name)), $freq*1000, $total_freq*1000));
 }
  scraperwiki::sqlitecommit();
}

?>
<?php
# first time through, create tables and indices


$urls = array(
  'boy_names'=>'http://www.census.gov/genealogy/names/dist.male.first',
  'girl_names'=>'http://www.census.gov/genealogy/names/dist.female.first',
  'last_names'=>'http://www.census.gov/genealogy/names/dist.all.last'
);

foreach ($urls as $table=>$url) {
  # first time through, create tables and indices
  scraperwiki::sqliteexecute("drop table if exists $table");
 
  scraperwiki::sqliteexecute("create table $table (rank INTEGER PRIMARY KEY, `name` string, freq INTEGER, cumulative_freq INTEGER)");
  // scraperwiki::sqliteexecute("create unique index ${table}rank on $table (rank)");
  scraperwiki::sqliteexecute("create unique index `{$table}name` on $table (name)");
  scraperwiki::sqliteexecute("create index {$table}cumulative_freq on $table (cumulative_freq)");

  $data = scraperWiki::scrape($url);
  foreach (explode("\n", $data) as $s) {
     // hack, should really use readf or scanf something like that
     list($name, $freq, $total_freq, $rank) = explode(' ', preg_replace('{ +}', ' ', $s));
     if (!empty($name))
         scraperwiki::sqliteexecute("insert into $table values (?,?,?,?)", array($rank, ucfirst(strtolower($name)), $freq*1000, $total_freq*1000));
 }
  scraperwiki::sqlitecommit();
}

?>
