<?php
set_time_limit(0);
require 'scraperwiki/simple_html_dom.php';
// require 'simple_html_dom.php';
function getdata($url){
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    //curl_setopt($ch, CURLOPT_PROXY, "200.211.199.219:80");
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    $sitedata = curl_exec ($ch);
    curl_close ($ch);
    return $sitedata;
}

/** 
 * Returns the url query as associative array 
 * 
 * @param    string    query 
 * @return    array    params 
*/ 


function convertUrlQuery($query) { 
    $queryParts = explode('&', $query); 
    
    $params = array(); 
    foreach ($queryParts as $param) { 
        $item = explode('=', $param); 
        $params[$item[0]] = $item[1]; 
    } 
    
    return $params; 
} 


for ($i=957; $i < 1541 ; ) {
    $data = getdata("http://www.flipkart.com/home-kitchen/pr?p%5B%5D=sort%3Dprice_desc&sid=j9e&layout=grid&start=".$i."&ajax=true");
    $data = str_replace("<textarea id='ajax'>", "", $data);
    $data = str_replace("</textarea>", "", $data);
    $data = html_entity_decode($data);

    $html = str_get_html($data);

    foreach($html->find('.fk-anchor-link') as $element) {
        $link = 'http://www.flipkart.com'.$element->href;
        if ($url = parse_url($link)) {
            $urlquery = convertUrlQuery($url['query']);
            $url = $url['scheme'].'://'.$url['host'].$url['path'].'?pid='.$urlquery['pid'];

            // put all your logic here 
            $itemdata = getdata($url);        
            $product_url = (string)$url;

            //sqlite save command
scraperwiki::sqliteexecute("insert into flipkart_home_and_kitchen_dump values (?,?)", array($product_url,$itemdata));

            //sqlite save command
            scraperwiki::sqlitecommit();

        }        
    }
    // ending for loop 
    if($i>20){
        $i=$i+20;
    }else{
        $i=$i+21;
    }
}

?>