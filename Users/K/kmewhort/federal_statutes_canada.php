<?php
error_reporting(E_ERROR);
require 'scraperwiki/simple_html_dom.php';

/* globals */
$db_index = array('cite');
$base_url = 'http://laws-lois.justice.gc.ca';
$index_url = $base_url . '/eng/acts/%s.html'; // %s = index (A-Z);


/* execution */

// for each index from A-Z
foreach(range('A','Z') as $a){
    // load the list of legislation
    $html_content = scraperwiki::scrape(sprintf($index_url, $a));
    if(empty($html_content))
      continue;
    $dom = str_get_html($html_content);
    if(!$dom)
       continue;
   
    // for each act
    foreach($dom->find(".titlesList li") as $row){
      $r = array('jurisdiction' => 'federal', 'type' => 'statute');
      $r['title'] = $row->find(".TocTitle",0)->plaintext;
      $r['cite'] = $row->find(".htmlLink",0)->plaintext;

      // extract year from the citation
      if(preg_match('/(\d{4})\,/', $r['cite'], $match))
        $r['year'] = $match[1];

      // check if marked as repealed
      $r['repealed'] = false;
      if($row->find(".TocTitle .Repealed",0))
        $r['repealed'] = true;
    
      // load the inner page to get the direct file links
      $link = $base_url . '/eng/acts/' . $row->find(".TocTitle",0)->href;
      $inner_html_content = scraperwiki::scrape($link);
      if(empty($inner_html_content)){
        scraperwiki::save($db_index, $r);
        continue;
      }

      // get the dom
      $inner_dom = str_get_html($inner_html_content);
      if(!$inner_dom){
        scraperwiki::save($db_index, $r);
        continue;
      }

      // html, xml & pdf
      $link_base = substr($link, 0, strrpos($link, '/')+1);
      foreach($inner_dom->find("#printAll li a") as $item){
        if(preg_match('/HTML/', $item->plaintext)){
          $r['url_html'] = $link_base . $item->href;
          print $r['url_html']  . "\n";
        }
        else if(preg_match('/XML/', $item->plaintext)){
          $r['url_xml'] = $link_base . $item->href;
          break;
        }
        else if(preg_match('/PDF/', $item->plaintext)){
          $r['url_pdf'] = $link_base . $item->href;
          break;
        }

      }
      scraperwiki::save($db_index, $r);
    }// end for each act
}// end for each A-Z index
?>

<?php
error_reporting(E_ERROR);
require 'scraperwiki/simple_html_dom.php';

/* globals */
$db_index = array('cite');
$base_url = 'http://laws-lois.justice.gc.ca';
$index_url = $base_url . '/eng/acts/%s.html'; // %s = index (A-Z);


/* execution */

// for each index from A-Z
foreach(range('A','Z') as $a){
    // load the list of legislation
    $html_content = scraperwiki::scrape(sprintf($index_url, $a));
    if(empty($html_content))
      continue;
    $dom = str_get_html($html_content);
    if(!$dom)
       continue;
   
    // for each act
    foreach($dom->find(".titlesList li") as $row){
      $r = array('jurisdiction' => 'federal', 'type' => 'statute');
      $r['title'] = $row->find(".TocTitle",0)->plaintext;
      $r['cite'] = $row->find(".htmlLink",0)->plaintext;

      // extract year from the citation
      if(preg_match('/(\d{4})\,/', $r['cite'], $match))
        $r['year'] = $match[1];

      // check if marked as repealed
      $r['repealed'] = false;
      if($row->find(".TocTitle .Repealed",0))
        $r['repealed'] = true;
    
      // load the inner page to get the direct file links
      $link = $base_url . '/eng/acts/' . $row->find(".TocTitle",0)->href;
      $inner_html_content = scraperwiki::scrape($link);
      if(empty($inner_html_content)){
        scraperwiki::save($db_index, $r);
        continue;
      }

      // get the dom
      $inner_dom = str_get_html($inner_html_content);
      if(!$inner_dom){
        scraperwiki::save($db_index, $r);
        continue;
      }

      // html, xml & pdf
      $link_base = substr($link, 0, strrpos($link, '/')+1);
      foreach($inner_dom->find("#printAll li a") as $item){
        if(preg_match('/HTML/', $item->plaintext)){
          $r['url_html'] = $link_base . $item->href;
          print $r['url_html']  . "\n";
        }
        else if(preg_match('/XML/', $item->plaintext)){
          $r['url_xml'] = $link_base . $item->href;
          break;
        }
        else if(preg_match('/PDF/', $item->plaintext)){
          $r['url_pdf'] = $link_base . $item->href;
          break;
        }

      }
      scraperwiki::save($db_index, $r);
    }// end for each act
}// end for each A-Z index
?>

