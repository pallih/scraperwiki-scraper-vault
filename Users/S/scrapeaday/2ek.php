<?php

// Find documentation at http://simplehtmldom.sourceforge.net/manual.htm
require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://www.tweedekamer.nl/vergaderingen/commissievergaderingen/vandaag/details.jsp?parlisnummer=2012A04218&amp;dayofweek=Vrijdag&amp;his=0");
//print $html;
//print "\n\nEND OF HTML\n\n";

$dom = new simple_html_dom();
$dom->load($html);

$arr = array();
foreach ($dom->find('td,.iconopen, .left,.clear') as $td)
    array_push($arr, $td->plaintext);

//print_r($arr);

//$parts=parse_url("http://www.tweedekamer.nl/vergaderingen/commissievergaderingen/vandaag/details.jsp?parlisnummer=2012A04218&amp;dayofweek=Vrijdag&amp;his=0");
//$path_parts=explode('=', $parts['query']);
//$path_parts2=explode('&amp,', $parts['query']);
//$path_parts[count($path_parts)-4].
//$rest = var_export($path_parts2);
//$parlisnr = substr($rest, 10, -35);
//$output = array_slice($path_parts2, 1); 
 

//print_r($path_parts2);
//print_r($path_parts);

/*$url = "http://www.tweedekamer.nl/vergaderingen/commissievergaderingen/vandaag/details.jsp?parlisnummer=2012A04218&amp;dayofweek=Vrijdag&amp;his=0";

//print "original: $url \n";
$url = urldecode( $url );

//print "source: $url \n";
parse_str( $url, $params ); // Puts key/value-pairs in array    
print_r( $params );  
*/




$new = Array ();

for ($i = 0; $i < count($arr); $i+=15) {
    $new[] = Array(
        'Date' => $arr[$i+0],
        'Class' => $arr[$i+1],
        'Time' => $arr[$i+3],
        'Type' => $arr[$i+5],
        'Category' => $arr[$i+7],
        'Status' => $arr[$i+9],
        'Title' => $arr[$i+10],
        'Description' => $arr[$i+12]
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

?>


