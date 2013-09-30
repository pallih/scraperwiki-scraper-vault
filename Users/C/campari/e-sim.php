<?php

//$id=array();
$max=254602;
$index=1;
$countname ="Hungary";


for ($i=107483; $i<=$max; $i++)
  {
    $jsonurl = "http://primera.e-sim.org/apiCitizenById.html?id=" . $i  ;   
    $json = file_get_contents($jsonurl,0,null,null);
    $json_output = json_decode($json);
    $country = $json_output->citizenship;
   

      if ($country==$countname)
         {
            $id=$json_output->id ;
            scraperwiki::save_sqlite(array("Index"),array("Index"=>$index, "ID"=>$id));
            $index++;
         }
         
      $mar = $i % 6 ;   
         
      if ($mar == 0 )
      {
        sleep(5);
      }
         
  }    



/*foreach ($id as $value)
    {
        //echo $value ;
        echo "\"";
        echo $value ;
        echo "\",";
    }   */
  
?>

<?php

//$id=array();
$max=254602;
$index=1;
$countname ="Hungary";


for ($i=107483; $i<=$max; $i++)
  {
    $jsonurl = "http://primera.e-sim.org/apiCitizenById.html?id=" . $i  ;   
    $json = file_get_contents($jsonurl,0,null,null);
    $json_output = json_decode($json);
    $country = $json_output->citizenship;
   

      if ($country==$countname)
         {
            $id=$json_output->id ;
            scraperwiki::save_sqlite(array("Index"),array("Index"=>$index, "ID"=>$id));
            $index++;
         }
         
      $mar = $i % 6 ;   
         
      if ($mar == 0 )
      {
        sleep(5);
      }
         
  }    



/*foreach ($id as $value)
    {
        //echo $value ;
        echo "\"";
        echo $value ;
        echo "\",";
    }   */
  
?>

