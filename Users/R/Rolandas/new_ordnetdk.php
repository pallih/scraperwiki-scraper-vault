<?php

require 'scraperwiki/simple_html_dom.php';

echo "------------------------------start at ". date('H:i:s') ."------------------------------\n";
function get_page_query($dom)
{
# 2) get roll up div's anchor, parse href for query's first_id & last_id
#<div class="rulOp"> <a href="http://ordnet.dk/ddo/ordbog?browse=up&amp;last_id=59950&amp;first_id=59911&amp;query=ord&amp;aselect=opstyltet" title="rul op i listen">rul op</a>
  $rollUp = $dom->find("div.rulOp", 0);
  $rollUp_href = $rollUp->find("a", 0)->href;
  $url_parts = parse_url($rollUp_href);
  $query_parts = explode("&amp;", $url_parts["query"]);
  foreach ($query_parts as $v)
  {
    $query = explode("=",$v);
    if ($query[0] == "first_id") $first_id_str = $query[1];
    if ($query[0] == "last_id") $last_id_str = $query[1];
  }
  $first_id = intval($first_id_str);
  $last_id = intval($last_id_str);
  return array($first_id, $last_id);
}

function read_alphabetic_list($dom)
{
#  $first_id = $last_id = -1;
  list($first_id, $last_id) = get_page_query($dom);#  echo "\nfirst = $first_id_str; last = $last_id_str";


# 3) get search result div list
# <div class="searchResultBox"> <div>
#     <!-- <p>select_url: <span tal:content="python:request.get('page_settings').get('select_url')" /></p> -->
#     <a href="http://rdnet.dk/ddo/ordbog?aselect=opstoppertud&amp;query=ord&amp;first_id=59964&amp;last_id=60003">
#       opstoppertud
#     </a> sb. 
#   </div> </div>

  $searchResultBox = $dom->find("div.searchResultBox");
  if (count($searchResultBox) == 3)
  {
#  echo "\nsearchResultBox: " . $searchResultBox[0]->outertext; # testing
#  echo "\nsearchResultBox: " . $searchResultBox[1]->outertext; # testing

#  echo "\nsearchResultBox: " . $searchResultBox[2]->outertext; # testing
    $id = $first_id;
    foreach($searchResultBox[2]->find("div") as $data){
      $children = $data->children();
      $children[0]->outertext = "\n";
      $href = trim($children[1]->href);
      $word = trim($children[1]->innertext);
      $children[1]->outertext = "\n";
      $type = trim($data->innertext);

# 3b) save to db
      echo "\nid=$id\n";
      $data = array(
        "id" => $id++,
        "word" => $word,
        "type" => $type,
        "href" => $href
      );
      $table_name="word_list";
      $verbose=2;
      $message = scraperwiki::save_sqlite(array("id"), $data, $table_name, $verbose);
      print_r($message); #test
#      echo json_encode($data);
      if ($id == 3) break;
    }
  }
}
function read_pages()
{
# 1) get HTML string and make DOM
  $page_url = "http://ordnet.dk/ddo/ordbog?browse=up&last_id=80&first_id=41&query=ord&aselect=1%C2%BD";
  $dom = file_get_html($page_url);

  read_alphabetic_list($dom);

}

$read_pages = true;
$read_words = false;
if ($read_pages)
{
  read_pages();
}
if ($read_words)
{
  read_words();
}
function read_words()
{
}


echo "\n-------------------------------end at ". date('H:i:s') ."-------------------------------\n";
?>
