<?php

    //get all players link
    $playersList = array();
    $linksList = array();
    
    for( $i='a';;$i++){
        if ($i == 'x') continue;
        $givenLink = "http://www.baseball-reference.com/players/". $i . "/";
        array_push($linksList,$givenLink);   
        if($i=='z') break;       
                
    }
    
    foreach($linksList as $link){
        $html = file_get_contents($link);
        $dom = new DomDocument();
        @$dom->loadHTML($html);
        $xpath = new DOMXPath($dom);
        $mainNode= $xpath->query("//pre/a/@href");
       
        foreach($mainNode as $eachNode){
            
            $myLink = "http://www.baseball-reference.com". $eachNode->nodeValue;
            array_push($playersList, $myLink);  
           
       }

    }


$i=0;
   foreach($playersList as $link){
    if($i<=14905)
    {$i++ ;
    continue;
    }

        //$link ="http://www.baseball-reference.com/players/a/abadijo01.shtml";
        $givenLink =$link;
        $html = file_get_contents($link);
        $dom = new DomDocument();
        @$dom->loadHTML($html);
        $xpath = new DOMXPath($dom);
    
        $mainNode= $xpath->query("//div[@id='info_box']//h1/text()");   
        list($fName,$lName) = explode(' ',$mainNode->item(0)->nodeValue);
        
   
        $position = $xpath->query("//strong[starts-with(.,'Position')]/following::text()")->item(0)->nodeValue;
        $position = str_replace(": ","",$position);
        $birthDate = $xpath->query("//span[@id='necro-birth']/@data-birth")->item(0)->nodeValue;
        $death = $xpath->query("//span[@id='necro-death']/@data-death")->item(0)->nodeValue;
    
        //$schools= $xpath->query("//p/strong[.='College:']/following-sibling::a[starts-with(@href,'/colleges/')]/text()");
        
        $schools= $xpath->query(".//a[.='Schools']/following::span[@class='small_text']")->item(0)->nodeValue;
        if(!$schools){
            $schools= $xpath->query(".//a[.='School']/following::a")->item(0)->nodeValue;   
             //$schools="sudip";
         }      
        
        
        $teams = $xpath->query(".//strong[.='Teams']/following::text()")->item(0)->nodeValue;
        
        if(!$teams)    
            $teams = $xpath->query(".//strong[.='Team']/following::text()")->item(0)->nodeValue;
        
        $teams = str_replace("(by GP):","",$teams);
    
        $debut =$xpath->query(".//a[.='Debut']/following::a")->item(0)->nodeValue;
        if($debut=="Final Game")
            $debut =$xpath->query(".//a[.='Debut']/parent::*/following::text()")->item(0)->nodeValue;
    
    
        
        scraperwiki::save_sqlite(array("index"),array("index"=>$i, "First name"=>$fName, "Last Name"=>$lName, "Position"=>$position,"Birth Date"=>$birthDate,"School"=>$schools,"Teams"=>$teams,"Debut"=>$debut,"Death"=>$death, "Link"=>$givenLink));
    $i++;   
 }


?>

<?php

    //get all players link
    $playersList = array();
    $linksList = array();
    
    for( $i='a';;$i++){
        if ($i == 'x') continue;
        $givenLink = "http://www.baseball-reference.com/players/". $i . "/";
        array_push($linksList,$givenLink);   
        if($i=='z') break;       
                
    }
    
    foreach($linksList as $link){
        $html = file_get_contents($link);
        $dom = new DomDocument();
        @$dom->loadHTML($html);
        $xpath = new DOMXPath($dom);
        $mainNode= $xpath->query("//pre/a/@href");
       
        foreach($mainNode as $eachNode){
            
            $myLink = "http://www.baseball-reference.com". $eachNode->nodeValue;
            array_push($playersList, $myLink);  
           
       }

    }


$i=0;
   foreach($playersList as $link){
    if($i<=14905)
    {$i++ ;
    continue;
    }

        //$link ="http://www.baseball-reference.com/players/a/abadijo01.shtml";
        $givenLink =$link;
        $html = file_get_contents($link);
        $dom = new DomDocument();
        @$dom->loadHTML($html);
        $xpath = new DOMXPath($dom);
    
        $mainNode= $xpath->query("//div[@id='info_box']//h1/text()");   
        list($fName,$lName) = explode(' ',$mainNode->item(0)->nodeValue);
        
   
        $position = $xpath->query("//strong[starts-with(.,'Position')]/following::text()")->item(0)->nodeValue;
        $position = str_replace(": ","",$position);
        $birthDate = $xpath->query("//span[@id='necro-birth']/@data-birth")->item(0)->nodeValue;
        $death = $xpath->query("//span[@id='necro-death']/@data-death")->item(0)->nodeValue;
    
        //$schools= $xpath->query("//p/strong[.='College:']/following-sibling::a[starts-with(@href,'/colleges/')]/text()");
        
        $schools= $xpath->query(".//a[.='Schools']/following::span[@class='small_text']")->item(0)->nodeValue;
        if(!$schools){
            $schools= $xpath->query(".//a[.='School']/following::a")->item(0)->nodeValue;   
             //$schools="sudip";
         }      
        
        
        $teams = $xpath->query(".//strong[.='Teams']/following::text()")->item(0)->nodeValue;
        
        if(!$teams)    
            $teams = $xpath->query(".//strong[.='Team']/following::text()")->item(0)->nodeValue;
        
        $teams = str_replace("(by GP):","",$teams);
    
        $debut =$xpath->query(".//a[.='Debut']/following::a")->item(0)->nodeValue;
        if($debut=="Final Game")
            $debut =$xpath->query(".//a[.='Debut']/parent::*/following::text()")->item(0)->nodeValue;
    
    
        
        scraperwiki::save_sqlite(array("index"),array("index"=>$i, "First name"=>$fName, "Last Name"=>$lName, "Position"=>$position,"Birth Date"=>$birthDate,"School"=>$schools,"Teams"=>$teams,"Debut"=>$debut,"Death"=>$death, "Link"=>$givenLink));
    $i++;   
 }


?>

