<?php
error_reporting(E_ERROR);
require 'scraperwiki/simple_html_dom.php';

/* globals */
$db_index = array('cite');
$base_url = 'http://www.qp.alberta.ca';
$index_url = $base_url . '/570.cfm?search_by=alpha&letter=%s&txSubLoc=%s'; // %s = index (A-Z), then regulations or acts
$start_index = 'A';

/* execution */

// for acts and regulations
foreach(array('acts','regulations') as $type){
  // for each index from A-Z (plus 1 & 2)
  foreach(array_merge(range($start_index,'Z'), range('1','2')) as $a){
    // load the list of legislation
    $html_content = scraperwiki::scrape(sprintf($index_url, $a, $type));
    if(empty($html_content))
      continue;
    $dom = str_get_html($html_content);
    if(!$dom)
       continue;
   
    // for each statute or reg.
    foreach($dom->find("#content table ul li a") as $row){
      $r = array('jurisdiction' => 'alberta');
      $r['type'] = ($type == 'acts') ? 'statute' : 'regulation';
      $r['title'] = $row->plaintext;
 
       // cite, url_html, year
      
      // drill into inner page for the statute
      $link = $base_url . '/' . $row->href;
      $inner_html_content = scraperwiki::scrape($link);
      if(empty($inner_html_content)){
        // cannot save without at least a cite from the inner page
        continue;
      }

      // pull out just the main column (to try to avoid zend_nm_heap errors)
      //$found = preg_match('/\<div id\=\"contentColumn\"\>(.*?)\<\!\-\- close content column \-\-\>/', $inner_html_content, $match);
      $found = preg_match('/\<div id\=\"contentColumn\"\>(.*?)<\!\-\- close content/s', $inner_html_content, $match);
      $inner_html_content = $match[1];

      // get the dom
      $inner_dom = str_get_html($inner_html_content);
      if(!$inner_dom){
        // cannot save without at least a cite from the inner page
        continue;
      }

      // get the main table
      $tbl = $inner_dom->find('.columnLeftFull .tbl', 0);
      if(!$tbl)
        continue;

      // find the relevant inner page info
      foreach($tbl->find('td') as $item){
         if(preg_match('/\s*Chapter\/Regulation\:\s*(.*)/', $item->plaintext, $match)){
           $r['cite'] = $match[1];

           // try to reformat the cite into proper notation (eg. "A-43 RSA 2000" -> RSA 2000, c A-43)
           if(preg_match('/([A-Z]\-[\d\.]+)\s+([A-Z]+)\s+(\d{4})/', $r['cite'], $match)){
             $r['cite'] = $match[2] . ' ' . $match[3] . ', c ' . $match[1];
             $r['year'] = $match[3];
           }
           else if(preg_match('/(\d+\/)(\d{4})\s*\Z/', $cite['cite'], $match)){
             $r['cite'] = 'Alta Reg ' . $match[1] . $match[2];
             $r['year'] = $match[2];
           }
         }
         else{
           // check for links to documents
           $doclink = $item->find('a',0);
           if($doclink && preg_match('/PDF/', $doclink->plaintext))
             $r['url_pdf'] = $base_url . '/' . $doclink->href;
           else if($doclink && preg_match('/HTML/', $doclink->plaintext))
             $r['url_html'] = $base_url . '/' . $doclink->href;
         }
      }// for each inner page info item
      
      scraperwiki::save($db_index, $r);
    }// end for each statute/reg
  }// end for each A-Z index
}//end for statute vs. reg.
?>




<?php
error_reporting(E_ERROR);
require 'scraperwiki/simple_html_dom.php';

/* globals */
$db_index = array('cite');
$base_url = 'http://www.qp.alberta.ca';
$index_url = $base_url . '/570.cfm?search_by=alpha&letter=%s&txSubLoc=%s'; // %s = index (A-Z), then regulations or acts
$start_index = 'A';

/* execution */

// for acts and regulations
foreach(array('acts','regulations') as $type){
  // for each index from A-Z (plus 1 & 2)
  foreach(array_merge(range($start_index,'Z'), range('1','2')) as $a){
    // load the list of legislation
    $html_content = scraperwiki::scrape(sprintf($index_url, $a, $type));
    if(empty($html_content))
      continue;
    $dom = str_get_html($html_content);
    if(!$dom)
       continue;
   
    // for each statute or reg.
    foreach($dom->find("#content table ul li a") as $row){
      $r = array('jurisdiction' => 'alberta');
      $r['type'] = ($type == 'acts') ? 'statute' : 'regulation';
      $r['title'] = $row->plaintext;
 
       // cite, url_html, year
      
      // drill into inner page for the statute
      $link = $base_url . '/' . $row->href;
      $inner_html_content = scraperwiki::scrape($link);
      if(empty($inner_html_content)){
        // cannot save without at least a cite from the inner page
        continue;
      }

      // pull out just the main column (to try to avoid zend_nm_heap errors)
      //$found = preg_match('/\<div id\=\"contentColumn\"\>(.*?)\<\!\-\- close content column \-\-\>/', $inner_html_content, $match);
      $found = preg_match('/\<div id\=\"contentColumn\"\>(.*?)<\!\-\- close content/s', $inner_html_content, $match);
      $inner_html_content = $match[1];

      // get the dom
      $inner_dom = str_get_html($inner_html_content);
      if(!$inner_dom){
        // cannot save without at least a cite from the inner page
        continue;
      }

      // get the main table
      $tbl = $inner_dom->find('.columnLeftFull .tbl', 0);
      if(!$tbl)
        continue;

      // find the relevant inner page info
      foreach($tbl->find('td') as $item){
         if(preg_match('/\s*Chapter\/Regulation\:\s*(.*)/', $item->plaintext, $match)){
           $r['cite'] = $match[1];

           // try to reformat the cite into proper notation (eg. "A-43 RSA 2000" -> RSA 2000, c A-43)
           if(preg_match('/([A-Z]\-[\d\.]+)\s+([A-Z]+)\s+(\d{4})/', $r['cite'], $match)){
             $r['cite'] = $match[2] . ' ' . $match[3] . ', c ' . $match[1];
             $r['year'] = $match[3];
           }
           else if(preg_match('/(\d+\/)(\d{4})\s*\Z/', $cite['cite'], $match)){
             $r['cite'] = 'Alta Reg ' . $match[1] . $match[2];
             $r['year'] = $match[2];
           }
         }
         else{
           // check for links to documents
           $doclink = $item->find('a',0);
           if($doclink && preg_match('/PDF/', $doclink->plaintext))
             $r['url_pdf'] = $base_url . '/' . $doclink->href;
           else if($doclink && preg_match('/HTML/', $doclink->plaintext))
             $r['url_html'] = $base_url . '/' . $doclink->href;
         }
      }// for each inner page info item
      
      scraperwiki::save($db_index, $r);
    }// end for each statute/reg
  }// end for each A-Z index
}//end for statute vs. reg.
?>




