<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

//sdfsdfsdfsdf

$page_counter= 0 ;
$content=TRUE ;

while ($content==TRUE ){
 $html = scraperwiki::scrape("http://www.centralscotlandfire.gov.uk/incident_page.php?page=".$page_counter);

$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find('div[id=incident_line]') as $data_line){
    $id='';

     foreach($data_line->find('div[id=incident_station]') as $data){
         foreach($dom->find('a') as $data){
           $station=  $data->plaintext ;             
         }
      }

      foreach($data_line->find('div[id=incident_status]') as $data){
      $split = preg_split('@:@' , $data->plaintext );
      $id=substr($split[1], 0 ,-4);
      $hour=$split[2];

      $date_split = preg_split('@ @' , $split[3]); 
      //print_r($date_split); 
      $min=substr($date_split[0], 0 ,-2);
      $ampm=substr($date_split[0], -2);
      $day=$date_split[1];
      $date=$date_split[2];
      $month=$date_split[3];
     }
      foreach($data_line->find('div[id=incident_description]') as $data){
         $split = preg_split('@:@' , $data->plaintext );
         $desc=  $split[1];
     }
      foreach($data_line->find('div[id=incident_units]') as $data){
         $split = preg_split('@:@' , $data->plaintext );
         $units=  $split[1];
     } 
      foreach($data_line->find('div[id=incident_location]') as $data){
         $split = preg_split('@:@' , $data->plaintext );
         $location=  $split[1];
     }
      foreach($data_line->find('div[id=incident_summary]') as $data){
         $split = preg_split('@:@' , $data->plaintext );
         $summary=  $split[1];
     } 
     if ( $id!='' ) {
      # Store data in the datastore
      scraperwiki::save_sqlite(array('id'), array( 'id' =>$id ,
                                                    'station' =>$station ,
                                                    'date' =>$date ,
                                                    'hour' =>$hour ,
                                                    'day' =>$day ,
                                                    'ampm' =>$ampm ,
                                                    'month' =>$month ,
                                                    'minute' =>$min ,
                                                    'description' =>$desc ,  
                                                    'units' =>$units , 
                                                    'location' =>$location , 
                                                    'summary' =>$summary )      );


     } else {
      // id is empty set content to false
      $content=FALSE;
     }
  }
  $page_counter++;
}
?>