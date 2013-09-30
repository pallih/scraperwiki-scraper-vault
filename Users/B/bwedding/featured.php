<?php

// Only change the city

    $html = file_get_contents("http://www.logstylemantels.com/Mtlinvent_results.cfm");
    $dom = new DOMDocument();
    @$dom->loadHTML($html);
    $x = new DOMXPath($dom);
    $i = 0;
    $data = array();
    foreach($x->query("//div[@id='ires']//h3//a") as $node)
    {
        
        $url = $node->getAttribute("href")."\n";
        $url = stristr($url , "http");
        $url = parse_url($url, PHP_URL_HOST) . "\n";
        echo $url;
        scraperwiki::save_sqlite($data, array("index"=>$i++, "url"=>$url));    
    }  
    
       
?>
<?php

// Only change the city

    $html = file_get_contents("http://www.logstylemantels.com/Mtlinvent_results.cfm");
    $dom = new DOMDocument();
    @$dom->loadHTML($html);
    $x = new DOMXPath($dom);
    $i = 0;
    $data = array();
    foreach($x->query("//div[@id='ires']//h3//a") as $node)
    {
        
        $url = $node->getAttribute("href")."\n";
        $url = stristr($url , "http");
        $url = parse_url($url, PHP_URL_HOST) . "\n";
        echo $url;
        scraperwiki::save_sqlite($data, array("index"=>$i++, "url"=>$url));    
    }  
    
       
?>
