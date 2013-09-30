<?php
require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();

$html = scraperWiki::scrape("http://api.sr.se/api/v2/programs/index?channelid=164&pagination=false");

$dom->load($html);
foreach($dom->find("program") as $program){
    $pod = $program->find("haspod");
    
    //Stupid if-statement because of string
    //The program has pods
    if($pod[0]->innertext == "true"){

        $castSite = scraperWiki::scrape("http://api.sr.se/api/v2/podfiles?programid=" . $program->id . "&size=30");
        $podDom = new simple_html_dom();
        $podDom->load($castSite);
        
        //Loop through all of the pod programs
        foreach($podDom->find("podfile") as $pod){
            $url = $pod->find("url");
            $tempDesc = $pod->find("description");
            $description = utf8_encode(mb_substr($tempDesc[0]->innertext, 0, 50) . "...");
            unset($tempDesc);
            
            $record = array( 'podId' => $pod->id, 'progId' => $program->id, 'progName' => $program->name, 'url' => $url[0]->innertext, 'description' => $description);
            scraperwiki::save(array('podId'), $record);
        }
    }
}
?><?php
require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();

$html = scraperWiki::scrape("http://api.sr.se/api/v2/programs/index?channelid=164&pagination=false");

$dom->load($html);
foreach($dom->find("program") as $program){
    $pod = $program->find("haspod");
    
    //Stupid if-statement because of string
    //The program has pods
    if($pod[0]->innertext == "true"){

        $castSite = scraperWiki::scrape("http://api.sr.se/api/v2/podfiles?programid=" . $program->id . "&size=30");
        $podDom = new simple_html_dom();
        $podDom->load($castSite);
        
        //Loop through all of the pod programs
        foreach($podDom->find("podfile") as $pod){
            $url = $pod->find("url");
            $tempDesc = $pod->find("description");
            $description = utf8_encode(mb_substr($tempDesc[0]->innertext, 0, 50) . "...");
            unset($tempDesc);
            
            $record = array( 'podId' => $pod->id, 'progId' => $program->id, 'progName' => $program->name, 'url' => $url[0]->innertext, 'description' => $description);
            scraperwiki::save(array('podId'), $record);
        }
    }
}
?>