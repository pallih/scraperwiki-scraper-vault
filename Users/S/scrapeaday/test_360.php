<?php

// Find documentation at http://simplehtmldom.sourceforge.net/manual.htm
require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://www.shell.nl/home/content/nld/aboutshell/careers_tpkg/students_and_graduates/is_shell_right_for_me/events/");
//print $html;
//print "\n\nEND OF HTML\n\n"; 

$dom = new simple_html_dom();
$dom->load($html);

$arr = array(); 
foreach ($dom->find('td') as $td)
    array_push($arr, $td->plaintext);

$new = Array();

for ($i = 0; $i < count($arr); $i+=4) {
    $new[] = Array(
        'ID' => count ($new),
        'Date' => $arr[$i+0],
        'Title' => $arr[$i+1],
        'Location' => $arr[$i+2],
        'Link' => $arr[$i+3]
    );    
}

print_r($new);

scraperwiki::save(array('ID'), $new);
scraperwiki::save(array('Date'), $new);
scraperwiki::save(array('Title'), $new);
scraperwiki::save(array('Location'), $new);
scraperwiki::save(array('Link'), $new); 

?>