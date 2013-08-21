<?php
require 'scraperwiki/simple_html_dom.php';

function get_dom($url)
{
  $html = scraperWiki::scrape($url);
  $dom = new simple_html_dom();
  $dom->load($html);
  return $dom;
}

function word_pron($dom)
{
  print gettype($dom) . " is dom\n\n";
 
  $word = $dom->find("div.definitionBoxTop>span.match", 0)->plaintext;
  print "word: /" . $word . "/";
  $udtDiv = $dom->find("div#id-udt", 0);
  if ($udtDiv == null)
  {
    print "udtDiv is null\n\n";
    return null;
  }
  else
  {
    $pron = $udtDiv->find("span.lydskrift text", 1)->innertext;
    print " [" . $pron . "]\n";
    $rec = array(
      'word' => $word, 
      'pronunciation' => $pron
    );
    return $rec;
  }
}

function read_page($url)
{
  $dom = get_dom($url);
  $record = word_pron($dom);
  if ($record != null)
  {
    scraperwiki::save_sqlite(array('word'), $record, "t_pron");
  }
}
 
function print_children($html)
{
  foreach ($html as $child1)
  {
    print "(tag)" . $child1->tag . "\n";
    print "(text)" . $child1->innertext . "\n";
  }
}


print "Starting...\n";
$first_url = "http://ordnet.dk/ddo/ordbog?aselect=ti&query=ti";

function make_site_list()
{
  $first_url = "http://ordnet.dk/ddo/ordbog?aselect=ti&query=ti";
  $dom = get_dom($first_url);
  $parent = $dom->find("div.rulOp", 0)->parent();
  $div_a_list = $parent->find("div.searchResultBox div a");
  $i = 0;
  foreach ($div_a_list as $child1)
  {
    $i++;
    if(isset($child1->href))
    {
      $hrefStr = str_replace("&amp;", "&", $child1->href);
      print "-------------($i) " . $child1->tag . ": " . $hrefStr . "\n";
      $pos = strpos($hrefStr, "aselect=");
      $substr = substr($hrefStr, $pos + 8);
      print "sub[" . $substr . "]\n";
    }
  }


//  $rec = array(
//    'word' => $word, 
//    'pronunciation' => $pron
//  );
//  return $rec;
}
//scraperwiki::save_var('last_page', 27);
make_site_list()
?>
