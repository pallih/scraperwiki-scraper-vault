<?php

function save_page($url,$table_name="pages"){
  $text = scraperwiki::scrape($url);
  $d=array( 
    "url" => $url,
    "text" => $text
  );
  ScraperWiki::save_sqlite(array('url'),$d,$table_name);
}

function get_page($url,$table_name="pages"){
  $rows=ScraperWiki::select("`text` from " . $table_name . " where url=?;",array($url));
  #Check length, then
  return $rows[0]['text'];
}



function test() {
  save_page('http://scraperwiki.com');
  echo get_page('http://scraperwiki.com');
}

test();

?>
<?php

function save_page($url,$table_name="pages"){
  $text = scraperwiki::scrape($url);
  $d=array( 
    "url" => $url,
    "text" => $text
  );
  ScraperWiki::save_sqlite(array('url'),$d,$table_name);
}

function get_page($url,$table_name="pages"){
  $rows=ScraperWiki::select("`text` from " . $table_name . " where url=?;",array($url));
  #Check length, then
  return $rows[0]['text'];
}



function test() {
  save_page('http://scraperwiki.com');
  echo get_page('http://scraperwiki.com');
}

test();

?>
