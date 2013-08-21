<?php
 ######################################
 # Basic PHP scraper
 ######################################
 
 require  'scraperwiki/simple_html_dom.php';
 
 $html = scraperwiki::scrape("http://td2660.dk/index.php?option=com_content&task=category&sectionid=7&id=18&Itemid=99999999&Itemid=51");
 print $html;
 
 # Use the PHP Simple HTML DOM Parser to extract <td> tags
 $dom = new simple_html_dom();
 $dom->load($html);
 
 foreach($dom->find('<form name="adminForm"') as $data)
 {
     # Store data in the datastore
     print $data->plaintext . "\n";
     scraperwiki::save(array('data'), array('data' => $data->plaintext));
 }
 
 ?>