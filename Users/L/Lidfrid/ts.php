<?php

    $url ="http://search.twitter.com/search.json?q=repidee13";

    $ch = curl_init($url);
            curl_setopt($ch,CURLOPT_USERAGENT,"Mozilla/5.0 (Windows; U; Windows NT 5.1; pl; rv:1.9) Gecko/2008052906 Firefox/3.0"); // mask as firefox 3
            curl_setopt($ch,CURLOPT_SSL_VERIFYPEER,false);  //disable ssl certificate validation
            curl_setopt($ch,CURLOPT_SSL_VERIFYHOST,false);
            curl_setopt($ch,CURLOPT_FAILONERROR,1);
            curl_setopt($ch,CURLOPT_FOLLOWLOCATION,1);    // allow redirects
            curl_setopt($ch,CURLOPT_RETURNTRANSFER,1);    // return into a variable
    $page = curl_exec($ch);

    $dom = new DOMDocument;
    @$dom->loadHTML($page);
    $xpath = new DOMXPath($dom);
    $lis = $xpath->query("//entry");
    echo $page;
?>