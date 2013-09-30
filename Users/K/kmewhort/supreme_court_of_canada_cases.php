<?php
/* Usage notes:
     Change the $minYear back as far as 1876 to get data from previous years.
*/
error_reporting(E_ERROR);
require 'scraperwiki/simple_html_dom.php';

/* globals */
$db_index = array('court','year','cite');
$minYear = 2012;
$base_url = 'http://scc.lexum.org';
$index_url = $base_url . '/en/dn/%d/01.html'; // %d = year

/* execution */

// for each year
for($y = $minYear; $y <= date('Y'); $y++){
  // load the page listing the cases for the year
  $html_content = scraperwiki::scrape(sprintf($index_url, $y));
  if(empty($html_content))
    continue;
  $dom = str_get_html($html_content);
  if(!$dom)
     continue;
   
  // for each case
  foreach($dom->find(".results li") as $row){
    $r = array('year' => $y, 'court' => 'SCC');
    $r['title'] = $row->find(".title a",0)->innertext;

    $cite_txt = trim($row->find(".item span", 2)->plaintext);
    if(empty($cite_txt)) // sometimes it's in the 3rd span
      $cite_txt = trim($row->find(".item span", 3)->plaintext);
    $r['cite'] = html_entity_decode($cite_txt, ENT_COMPAT, 'UTF-8');
    
    $r['date'] = html_entity_decode($row->find(".selected",0)->innertext, ENT_COMPAT, 'UTF-8');

    // load the inner case page to get the direct file links
    $link = $base_url . $row->find(".title a",0)->href;
    $case_html_content = scraperwiki::scrape($link);
    if(empty($case_html_content)){
       scraperwiki::save($db_index, $r);
       continue;
    }

    // pull out only the first table containing the file links (loading the whole page can result in running out of heapspace with a zend_nm_heap error)
    $regx_result = preg_match('/\<table\>(.*?)\<\/table\>/is', $case_html_content, $match);

    // get the dom
    $case_dom = str_get_html($match[1]);
    if(!$case_dom){
       scraperwiki::save($db_index, $r);
       continue;
    }

    foreach($case_dom->find(".item") as $item){
       $file_link = $item->find('a',0)->href;

       if($item->plaintext == 'PDF')
         $r['url_pdf'] = $base_url . $file_link;
       else if($item->plaintext == 'WPD')
         $r['url_wpd'] = $base_url . $file_link;
       else if($item->plaintext == 'DOCX')
         $r['url_doc'] = $base_url . $file_link;
       else if($item->plaintext == 'Printer Friendly')
         $r['url_html'] = $file_link;
    }
    scraperwiki::save($db_index, $r);
  }
} 
?>
<?php
/* Usage notes:
     Change the $minYear back as far as 1876 to get data from previous years.
*/
error_reporting(E_ERROR);
require 'scraperwiki/simple_html_dom.php';

/* globals */
$db_index = array('court','year','cite');
$minYear = 2012;
$base_url = 'http://scc.lexum.org';
$index_url = $base_url . '/en/dn/%d/01.html'; // %d = year

/* execution */

// for each year
for($y = $minYear; $y <= date('Y'); $y++){
  // load the page listing the cases for the year
  $html_content = scraperwiki::scrape(sprintf($index_url, $y));
  if(empty($html_content))
    continue;
  $dom = str_get_html($html_content);
  if(!$dom)
     continue;
   
  // for each case
  foreach($dom->find(".results li") as $row){
    $r = array('year' => $y, 'court' => 'SCC');
    $r['title'] = $row->find(".title a",0)->innertext;

    $cite_txt = trim($row->find(".item span", 2)->plaintext);
    if(empty($cite_txt)) // sometimes it's in the 3rd span
      $cite_txt = trim($row->find(".item span", 3)->plaintext);
    $r['cite'] = html_entity_decode($cite_txt, ENT_COMPAT, 'UTF-8');
    
    $r['date'] = html_entity_decode($row->find(".selected",0)->innertext, ENT_COMPAT, 'UTF-8');

    // load the inner case page to get the direct file links
    $link = $base_url . $row->find(".title a",0)->href;
    $case_html_content = scraperwiki::scrape($link);
    if(empty($case_html_content)){
       scraperwiki::save($db_index, $r);
       continue;
    }

    // pull out only the first table containing the file links (loading the whole page can result in running out of heapspace with a zend_nm_heap error)
    $regx_result = preg_match('/\<table\>(.*?)\<\/table\>/is', $case_html_content, $match);

    // get the dom
    $case_dom = str_get_html($match[1]);
    if(!$case_dom){
       scraperwiki::save($db_index, $r);
       continue;
    }

    foreach($case_dom->find(".item") as $item){
       $file_link = $item->find('a',0)->href;

       if($item->plaintext == 'PDF')
         $r['url_pdf'] = $base_url . $file_link;
       else if($item->plaintext == 'WPD')
         $r['url_wpd'] = $base_url . $file_link;
       else if($item->plaintext == 'DOCX')
         $r['url_doc'] = $base_url . $file_link;
       else if($item->plaintext == 'Printer Friendly')
         $r['url_html'] = $file_link;
    }
    scraperwiki::save($db_index, $r);
  }
} 
?>
