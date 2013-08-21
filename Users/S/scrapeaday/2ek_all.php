<?php

/*$mainurl = 'http://www.tweedekamer.nl/vergaderingen/commissievergaderingen/volgende_weken/dagoverzicht.jsp?JAAR=2012&MAAND=12&DAG=03&DOW=2';

$replace = 'JAAR=2012';

$url = str_replace('?JAAR=2012&', '?' . $replace . '&', $mainurl);

print_r($url);*/

$baseurl ='http://www.tweedekamer.nl/vergaderingen/commissievergaderingen/volgende_weken/';
$request_url ='http://www.tweedekamer.nl/vergaderingen/commissievergaderingen/volgende_weken/index.jsp';
 
$baseurl ='http://www.tweedekamer.nl/vergaderingen/commissievergaderingen/volgende_weken/';
$request_url ='http://www.tweedekamer.nl/vergaderingen/commissievergaderingen/volgende_weken/index.jsp';
 
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $request_url);   
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);  
    $result = curl_exec($ch);
    curl_close($ch);
    //$regex='|<a.*?href="(.*?)"|';
    preg_match_all('|<a.*?href="(.*?)"|',$result,$parts);
    $links=$parts[1];
    foreach($links as $link){
        echo $link."\r\n";
//print_r($link);
        if(!strstr( $link, 'dagoverzicht.jsp')) {
         continue;
        }

    $ch2 = curl_init();
        $timeout = 5;
        curl_setopt($ch2,CURLOPT_URL,$baseurl .$link);
        curl_setopt($ch2,CURLOPT_RETURNTRANSFER,1);
        curl_setopt($ch2,CURLOPT_CONNECTTIMEOUT,$timeout);
        $data = curl_exec($ch2);
        curl_close($ch2);
 //       return $data;
        print 'inspected '.$link.' done';
       // print_r($data);

   





// Find documentation at http://simplehtmldom.sourceforge.net/manual.htm
require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape($baseurl.$link);
//print $html;
//print "\n\nEND OF HTML\n\n";

$dom = new simple_html_dom();
$dom->load($data);

$arr = array();
foreach ($dom->find('td,.iconopen, .left,.clear') as $td)
    array_push($arr, $td->plaintext);

print_r($arr);




/*$url = "http://www.tweedekamer.nl/vergaderingen/commissievergaderingen/vandaag/details.jsp?parlisnummer=2012A04218&amp;dayofweek=Vrijdag&amp;his=0";

//print "original: $url \n";
$url = urldecode( $url );

//print "source: $url \n";
parse_str( $url, $params ); // Puts key/value-pairs in array    
print_r( $params ); 
*/

/*$data = array ();
$pattern = "/s/";

$matches = array_filter($data, function($a) use($pattern)  {
    return preg_grep($pattern, $a);
});


/*
$new = Array ();

for ($i = 0; $i < count($arr); $i+=4) {
    $new[] = Array(
        'Date' => $arr[$i+0],
        'Class' => $arr[$i+8],
        'Time' => $arr[$i+2],
        'Type' => $arr[$i+4],
        'Category' => $arr[$i+16],
        'Status' => $arr[$i+9],
        'Title' => $arr[$i+7],
        //'Description' => $arr[$i+12]
    );    
}

print_r($new);

scraperwiki::save(array('Class'), $new);
scraperwiki::save(array('Date'), $new);
scraperwiki::save(array('Time'), $new);
scraperwiki::save(array('Type'), $new);
scraperwiki::save(array('Category'), $new);
scraperwiki::save(array('Status'), $new);
scraperwiki::save(array('Description'), $new);
scraperwiki::save(array('Title'), $new);
*/
?>



