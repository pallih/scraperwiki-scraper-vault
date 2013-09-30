<?php

require 'scraperwiki/simple_html_dom.php';   

function getPageOfResults($url, $pagenum, $cat){
  $html = scraperWiki::scrape($url."?page=".$pagenum); 
  $dom = new simple_html_dom();
  $dom->load($html);
  $links = $dom->find("h2 a");
  $count = 0;
  foreach ($links as $link){
     echo $link->href."\n";
     // if (alreadyKnown($cat, $link->href)) return;
     $count = $count + 1;
     $record = array(
      'cat' => $cat, 
      'url' => $link->href
      );
      scraperwiki::save(array('cat', 'url'), $record);
  }
  echo "got ".$count." results\n";
  if ($count === 0) return;
  // getPageOfResults($url, $pagenum+1, $cat);
}

function alreadyKnown($cat, $url){
  $data = scraperwiki::sqliteexecute(           
      "select distinct id from swdata where cat='".$cat."' and url='".$url."'");
  if (count($data->data) === 0) return false;
  echo "already known : ".$url." in ".$cat."\n";
  return true;
}

getPageOfResults("http://www.open.edu/openlearn/subject/body-mind", 0, "Body and Mind"); // ~850
getPageOfResults("http://www.open.edu/openlearn/education", 0, "Education"); // ~140 
getPageOfResults("http://www.open.edu/openlearn/history-the-arts", 0, "History and the Arts"); // ~1300
getPageOfResults("http://www.open.edu/openlearn/languages", 0, "Language"); // 160
getPageOfResults("http://www.open.edu/openlearn/money-management", 0, "Money and Management"); // 634
getPageOfResults("http://www.open.edu/openlearn/nature-environment", 0, "Nature and Environment"); // 770
getPageOfResults("http://www.open.edu/openlearn/science-maths-technology", 0, "Science, Maths and Technology"); // 1480
getPageOfResults("http://www.open.edu/openlearn/society", 0, "Society"); // 742
getPageOfResults("http://www.open.edu/openlearn/whats-on", 0, "Whats on"); // 1275
getPageOfResults("http://www.open.edu/openlearn/about-openlearn", 0, "About OpenLearn"); // 16

?>
<?php

require 'scraperwiki/simple_html_dom.php';   

function getPageOfResults($url, $pagenum, $cat){
  $html = scraperWiki::scrape($url."?page=".$pagenum); 
  $dom = new simple_html_dom();
  $dom->load($html);
  $links = $dom->find("h2 a");
  $count = 0;
  foreach ($links as $link){
     echo $link->href."\n";
     // if (alreadyKnown($cat, $link->href)) return;
     $count = $count + 1;
     $record = array(
      'cat' => $cat, 
      'url' => $link->href
      );
      scraperwiki::save(array('cat', 'url'), $record);
  }
  echo "got ".$count." results\n";
  if ($count === 0) return;
  // getPageOfResults($url, $pagenum+1, $cat);
}

function alreadyKnown($cat, $url){
  $data = scraperwiki::sqliteexecute(           
      "select distinct id from swdata where cat='".$cat."' and url='".$url."'");
  if (count($data->data) === 0) return false;
  echo "already known : ".$url." in ".$cat."\n";
  return true;
}

getPageOfResults("http://www.open.edu/openlearn/subject/body-mind", 0, "Body and Mind"); // ~850
getPageOfResults("http://www.open.edu/openlearn/education", 0, "Education"); // ~140 
getPageOfResults("http://www.open.edu/openlearn/history-the-arts", 0, "History and the Arts"); // ~1300
getPageOfResults("http://www.open.edu/openlearn/languages", 0, "Language"); // 160
getPageOfResults("http://www.open.edu/openlearn/money-management", 0, "Money and Management"); // 634
getPageOfResults("http://www.open.edu/openlearn/nature-environment", 0, "Nature and Environment"); // 770
getPageOfResults("http://www.open.edu/openlearn/science-maths-technology", 0, "Science, Maths and Technology"); // 1480
getPageOfResults("http://www.open.edu/openlearn/society", 0, "Society"); // 742
getPageOfResults("http://www.open.edu/openlearn/whats-on", 0, "Whats on"); // 1275
getPageOfResults("http://www.open.edu/openlearn/about-openlearn", 0, "About OpenLearn"); // 16

?>
