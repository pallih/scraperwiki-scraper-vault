<?php

// Only change the city

        #$html = file_get_contents("https://www.google.com/search?num=100&start=1&q=katy+%22Featured+on+YP.COM%22&oq=katy+%22Featured+on+YP.COM%");
 $html = file_get_contents(https://www.google.it/webhp?sourceid=chrome-instant&ie=UTF-8&ion=1#hl=it&gs_nf=1&cp=24&gs_id=j&xhr=t&q=laquila99+%22Ezio+Bianchi%22&pf=p&sclient=psy-ab&oq=laquila99+%22Ezio+Bianchi%22&aq=f&aqi=&aql=&gs_l=&pbx=1&bav=on.2,or.r_gc.r_pw.r_cp.r_qf.,cf.osb&fp=cd35444d88909c23&ion=1&biw=1864&bih=981);
    @$dom->loadHTML($html);
    $x = new DOMXPath($dom);
    $i = 0;
    foreach($x->query("//div[@id='ires']//h3//a") as $node)
    {
        $url = $node->getAttribute("href")."\n";
        $url = stristr($url , "http");
        $url = parse_url($url, PHP_URL_HOST) . "\n";
        echo $url;
        scraperwiki::save_sqlite(array("fd"), array("fd"=>$url));
        $i++;
    }  
        
?>
