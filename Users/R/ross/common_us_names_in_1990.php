<?php
# first time through, create tables and indices


$urls = array( 
  'boy_names'=>'http://www.census.gov/genealogy/names/dist.male.first',
  'girl_names'=>'http://www.census.gov/genealogy/names/dist.female.first',
  'last_names'=>'http://www.census.gov/genealogy/names/dist.all.last'
);

foreach ($urls as $table=>$url) {
  $data = scraperWiki::scrape($url);
  scraperwiki::sqliteexecute("drop table if exists $table");
  foreach (explode("\n", $data) as $s) {
     list($name, $freq, $total_freq, $rank) = explode(' ', preg_replace('{ +}', ' ', $s));
    scraperwiki::save_sqlite(array("rank"),array("name"=>$name, "rank"=> $rank, "frequency"=>$freq, "Cumulative" => $total_freq),$table_name=$table, $verbose=1);           
 }

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
  $data = scraperWiki::scrape($url);
  scraperwiki::sqliteexecute("drop table if exists $table");
  foreach (explode("\n", $data) as $s) {
     list($name, $freq, $total_freq, $rank) = explode(' ', preg_replace('{ +}', ' ', $s));
    scraperwiki::save_sqlite(array("rank"),array("name"=>$name, "rank"=> $rank, "frequency"=>$freq, "Cumulative" => $total_freq),$table_name=$table, $verbose=1);           
 }

}

?>
