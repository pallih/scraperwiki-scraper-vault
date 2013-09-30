<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';


$id= 1 ;
$content=TRUE ;

while ($content==TRUE ){
 $html = scraperwiki::scrape("http://www.myfdb.com/people/".$id);

$dom = new simple_html_dom();
$dom->load($html);

      foreach($dom->find('div[id=breadcrumb]') as $data){
         foreach($dom->find('a') as $data){
           $name=  $data->plaintext ;             
         }
      }             

     if ( $id!='' ) {
      # Store data in the datastore
      scraperwiki::save_sqlite(array('id'), array( 'id' =>$id, 
                                                   'name' => $name));
     } else {
      // id is empty set content to false
      $content=FALSE;
     }

  $id++;
} 
?><?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';


$id= 1 ;
$content=TRUE ;

while ($content==TRUE ){
 $html = scraperwiki::scrape("http://www.myfdb.com/people/".$id);

$dom = new simple_html_dom();
$dom->load($html);

      foreach($dom->find('div[id=breadcrumb]') as $data){
         foreach($dom->find('a') as $data){
           $name=  $data->plaintext ;             
         }
      }             

     if ( $id!='' ) {
      # Store data in the datastore
      scraperwiki::save_sqlite(array('id'), array( 'id' =>$id, 
                                                   'name' => $name));
     } else {
      // id is empty set content to false
      $content=FALSE;
     }

  $id++;
} 
?>