<?php

# Blank PHP
require 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("http://www.truckstopsf.com");
$html = str_get_html($html_content);

foreach ($html->find("section") as $content) {           
  
    $thisweek = $content->children(1)->children(0)->innertext;
    $urlnext = $content->children(1)->children(2);
    
    $weekday = array('Mon ', 'Tue ', 'Wed ', 'Thu ', 'Fri ');
  

/*
    $data[0] = array(
            "day" => "",
            "date" =>"",
            "trucks" => array(
                    "tname"=> "name of the truck",
                    "url"  => "url",
                    "blurb" => "empty"
            )
 
     );
*/

   
    foreach($content->find("div") as $p){
            

            if(   $p-> tag == "div"){
                
                            print $p;
           
                 
                foreach($p->children() as $node){
                 
                

                   
                    $line =  substr($node->innertext, 0, 4);
                    $key = substr($line,0,3);  
                    
                    
                    
                    if(in_array($line,$weekday)) {
                                          
                        $data[$key]= array(
                                "day" => $key,
                                "date" => $node->innertext
                        );                   
                        
                        $day = $key;    
                    }elseif ($node->tag != "h3"){
                
                        
                        $truckName = $node->first_child()->innertext;
                        $blurb = $node->find("strong", 0)->innertext = "";
                        $blurb = $node->plaintext;
                        
                        $truck = array("tname"=> $truckName,
                                       "url"  => "http://",
                                        "blurb" => $blurb
                        );                   
                        $data[$day]['trucks'][] = $truck;
                        

                       
                       // print $truckName. " ".$blurb . "\n";
                                            
                    }// end of else if
                    
                  

                    // getting within that day

                    

                } //end of foreach #node                    

            }    //end of foreach $p


         }  //end of if div

}  //end foreach content   


/*


foreach ($data as $i => $d){
    print $d["day"]."\n";
    foreach ($d["trucks"] as  $a => $t){
        print $t['tname'] ."\n";
        print $t['blurb'] ."\n";
    }  
}


<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Twitter Bootstrap</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">
 </head>

  <body data-spy="scroll" data-target=".subnav" data-offset="50">
    
  </body>
</html>


*/
//print_r($data);




//http://oreilly.com/catalog/progphp/chapter/ch05.html

?>
<?php

# Blank PHP
require 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("http://www.truckstopsf.com");
$html = str_get_html($html_content);

foreach ($html->find("section") as $content) {           
  
    $thisweek = $content->children(1)->children(0)->innertext;
    $urlnext = $content->children(1)->children(2);
    
    $weekday = array('Mon ', 'Tue ', 'Wed ', 'Thu ', 'Fri ');
  

/*
    $data[0] = array(
            "day" => "",
            "date" =>"",
            "trucks" => array(
                    "tname"=> "name of the truck",
                    "url"  => "url",
                    "blurb" => "empty"
            )
 
     );
*/

   
    foreach($content->find("div") as $p){
            

            if(   $p-> tag == "div"){
                
                            print $p;
           
                 
                foreach($p->children() as $node){
                 
                

                   
                    $line =  substr($node->innertext, 0, 4);
                    $key = substr($line,0,3);  
                    
                    
                    
                    if(in_array($line,$weekday)) {
                                          
                        $data[$key]= array(
                                "day" => $key,
                                "date" => $node->innertext
                        );                   
                        
                        $day = $key;    
                    }elseif ($node->tag != "h3"){
                
                        
                        $truckName = $node->first_child()->innertext;
                        $blurb = $node->find("strong", 0)->innertext = "";
                        $blurb = $node->plaintext;
                        
                        $truck = array("tname"=> $truckName,
                                       "url"  => "http://",
                                        "blurb" => $blurb
                        );                   
                        $data[$day]['trucks'][] = $truck;
                        

                       
                       // print $truckName. " ".$blurb . "\n";
                                            
                    }// end of else if
                    
                  

                    // getting within that day

                    

                } //end of foreach #node                    

            }    //end of foreach $p


         }  //end of if div

}  //end foreach content   


/*


foreach ($data as $i => $d){
    print $d["day"]."\n";
    foreach ($d["trucks"] as  $a => $t){
        print $t['tname'] ."\n";
        print $t['blurb'] ."\n";
    }  
}


<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Twitter Bootstrap</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">
 </head>

  <body data-spy="scroll" data-target=".subnav" data-offset="50">
    
  </body>
</html>


*/
//print_r($data);




//http://oreilly.com/catalog/progphp/chapter/ch05.html

?>
