<?php
/*
    //class to hold players details
    class player{
        var $fName;
        var $lName;
        var $twitterId;
        var $position;
        var $birthDate;
        var $college;
        var $team;
        var $debut;
        var $death;
        var $link;
    }
*/
?>

<?php
    //get all players link
    $playersList = array();
    $linksList = array();
    array_push($linksList,"http://www.pro-football-reference.com/players/dbindex.htm");
    array_push($linksList,"http://www.pro-football-reference.com/players/teindex.htm");
    array_push($linksList,"http://www.pro-football-reference.com/players/rbindex.htm");
    array_push($linksList,"http://www.pro-football-reference.com/players/pindex.htm");
    array_push($linksList,"http://www.pro-football-reference.com/players/olindex.htm");
    array_push($linksList,"http://www.pro-football-reference.com/players/kindex.htm");
    array_push($linksList,"http://www.pro-football-reference.com/players/wrindex.htm");
    array_push($linksList,"http://www.pro-football-reference.com/players/lbindex.htm");
    array_push($linksList,"http://www.pro-football-reference.com/players/qbindex.htm");
    array_push($linksList,"http://www.pro-football-reference.com/players/dlindex.htm");

    for( $i='a';;$i++){
        if ($i == 'x') continue;
        $givenLink = "http://www.pro-football-reference.com/players/". $i . "/";
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
            
            $myLink = "http://www.pro-football-reference.com". $eachNode->nodeValue;
            array_push($playersList, $myLink);  
           
       }

    }

?>

<?php
$i=0;
    foreach($playersList as $link){

        //$link ="http://www.pro-football-reference.com/players/B/BaneHe20.htm";
        $givenLink =$link;
        $html = file_get_contents($link);
        $dom = new DomDocument();
        @$dom->loadHTML($html);
        $xpath = new DOMXPath($dom);
    
        $mainNode= $xpath->query("//div[@id='info_box']/h1/text()");   
        list($fName,$lName) = explode(' ',$mainNode->item(0)->nodeValue);
        
        $twitterQuery =$xpath->query("//div[@class='social_media']/following::p/a/text()[starts-with(.,'@')]");
        $twitterId =$twitterQuery->item(0)->nodeValue;
        
    
        $position = $xpath->query("//strong[[starts-with(.,'Position')]]/following::text()")->item(0)->nodeValue;
        
        $birthDate = $xpath->query("//span[@id='necro-birth']/@data-birth")->item(0)->nodeValue;
        $death = $xpath->query("//span[@id='necro-death']/@data-death")->item(0)->nodeValue;
    
        //$schools= $xpath->query("//p/strong[.='College:']/following-sibling::a[starts-with(@href,'/colleges/')]/text()");
        $schools= $xpath->query(".//a[starts-with(.,'School')]/following::a/text()");
        
        $teams = $xpath->query("//table[@id='defense']/tbody/tr/td[3]");
        $team =$teams->item(0)->nodeValue;
        foreach($teams as $givenTeam){
            $team.=", ".$givenTeam->nodeValue;
        }
    
        $debut =$xpath->query("//table[@id='defense']/tbody/tr/td[1]")->item(0)->nodeValue;
    
    
        
        scraperwiki::save_sqlite(array("index"),array("index"=>$i, "First name"=>$fName, "Last Name"=>$lName, "TwitterId"=>$twitterId,"Position"=>$position,"Birth Date"=>$birthDate,"School"=>$school,"Team"=>$team,"Debut"=>$debut,"Death"=>$death, "Link"=>$givenLink));
    $i++;   
 }
?>

<?php
/*
    //class to hold players details
    class player{
        var $fName;
        var $lName;
        var $twitterId;
        var $position;
        var $birthDate;
        var $college;
        var $team;
        var $debut;
        var $death;
        var $link;
    }
*/
?>

<?php
    //get all players link
    $playersList = array();
    $linksList = array();
    array_push($linksList,"http://www.pro-football-reference.com/players/dbindex.htm");
    array_push($linksList,"http://www.pro-football-reference.com/players/teindex.htm");
    array_push($linksList,"http://www.pro-football-reference.com/players/rbindex.htm");
    array_push($linksList,"http://www.pro-football-reference.com/players/pindex.htm");
    array_push($linksList,"http://www.pro-football-reference.com/players/olindex.htm");
    array_push($linksList,"http://www.pro-football-reference.com/players/kindex.htm");
    array_push($linksList,"http://www.pro-football-reference.com/players/wrindex.htm");
    array_push($linksList,"http://www.pro-football-reference.com/players/lbindex.htm");
    array_push($linksList,"http://www.pro-football-reference.com/players/qbindex.htm");
    array_push($linksList,"http://www.pro-football-reference.com/players/dlindex.htm");

    for( $i='a';;$i++){
        if ($i == 'x') continue;
        $givenLink = "http://www.pro-football-reference.com/players/". $i . "/";
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
            
            $myLink = "http://www.pro-football-reference.com". $eachNode->nodeValue;
            array_push($playersList, $myLink);  
           
       }

    }

?>

<?php
$i=0;
    foreach($playersList as $link){

        //$link ="http://www.pro-football-reference.com/players/B/BaneHe20.htm";
        $givenLink =$link;
        $html = file_get_contents($link);
        $dom = new DomDocument();
        @$dom->loadHTML($html);
        $xpath = new DOMXPath($dom);
    
        $mainNode= $xpath->query("//div[@id='info_box']/h1/text()");   
        list($fName,$lName) = explode(' ',$mainNode->item(0)->nodeValue);
        
        $twitterQuery =$xpath->query("//div[@class='social_media']/following::p/a/text()[starts-with(.,'@')]");
        $twitterId =$twitterQuery->item(0)->nodeValue;
        
    
        $position = $xpath->query("//strong[[starts-with(.,'Position')]]/following::text()")->item(0)->nodeValue;
        
        $birthDate = $xpath->query("//span[@id='necro-birth']/@data-birth")->item(0)->nodeValue;
        $death = $xpath->query("//span[@id='necro-death']/@data-death")->item(0)->nodeValue;
    
        //$schools= $xpath->query("//p/strong[.='College:']/following-sibling::a[starts-with(@href,'/colleges/')]/text()");
        $schools= $xpath->query(".//a[starts-with(.,'School')]/following::a/text()");
        
        $teams = $xpath->query("//table[@id='defense']/tbody/tr/td[3]");
        $team =$teams->item(0)->nodeValue;
        foreach($teams as $givenTeam){
            $team.=", ".$givenTeam->nodeValue;
        }
    
        $debut =$xpath->query("//table[@id='defense']/tbody/tr/td[1]")->item(0)->nodeValue;
    
    
        
        scraperwiki::save_sqlite(array("index"),array("index"=>$i, "First name"=>$fName, "Last Name"=>$lName, "TwitterId"=>$twitterId,"Position"=>$position,"Birth Date"=>$birthDate,"School"=>$school,"Team"=>$team,"Debut"=>$debut,"Death"=>$death, "Link"=>$givenLink));
    $i++;   
 }
?>

