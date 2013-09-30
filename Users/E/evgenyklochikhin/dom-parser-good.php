<?php

// Find documentation at http://simplehtmldom.sourceforge.net/manual.htm
require  'scraperwiki/simple_html_dom.php';

$url = "http://ruseffect.com";

$html = scraperwiki::scrape($url);
//print $html;
//print "\n\nEND OF HTML\n\n"; 

$dom = new simple_html_dom();
$dom->load($html);

// First iteration of link search on homepage
$links = array(); 
foreach ($dom->find('/howdy/') as $a)
        array_push($links, $a->plaintext);

$links = array_unique($links);
print_r($links);
die;


foreach ($links as $l)
        if (preg_match("/.*.ruseffect.com/", $l)) {
            if (preg_match("/.*#/", $l)) {
} else {
        $hello = scraperwiki::scrape($l);
        $dom2 = new simple_html_dom();
        $dom2->load($l);
}
}


// Second iteration of link search on first-level pages
$links2 = array(); 
foreach ($dom2->find('a') as $a2)
            array_push($links2, $a2->href);

$links2 = array_unique($links2);
print_r($links2);

die;

foreach ($links2 as $l2)
        if (preg_match("/.*.ruseffect.com/", $l2) || preg_match("/$.*/", $l2)) {
            if (($l2 == $l) && (preg_match("/.*#/", $l))) {
                echo "Bad match";
} else {
        print_r($url . $l2);
        scraperwiki::scrape($url . $l2);
}
}

//print_r($links2);

die;


?>
<?php

// Find documentation at http://simplehtmldom.sourceforge.net/manual.htm
require  'scraperwiki/simple_html_dom.php';

$url = "http://ruseffect.com";

$html = scraperwiki::scrape($url);
//print $html;
//print "\n\nEND OF HTML\n\n"; 

$dom = new simple_html_dom();
$dom->load($html);

// First iteration of link search on homepage
$links = array(); 
foreach ($dom->find('/howdy/') as $a)
        array_push($links, $a->plaintext);

$links = array_unique($links);
print_r($links);
die;


foreach ($links as $l)
        if (preg_match("/.*.ruseffect.com/", $l)) {
            if (preg_match("/.*#/", $l)) {
} else {
        $hello = scraperwiki::scrape($l);
        $dom2 = new simple_html_dom();
        $dom2->load($l);
}
}


// Second iteration of link search on first-level pages
$links2 = array(); 
foreach ($dom2->find('a') as $a2)
            array_push($links2, $a2->href);

$links2 = array_unique($links2);
print_r($links2);

die;

foreach ($links2 as $l2)
        if (preg_match("/.*.ruseffect.com/", $l2) || preg_match("/$.*/", $l2)) {
            if (($l2 == $l) && (preg_match("/.*#/", $l))) {
                echo "Bad match";
} else {
        print_r($url . $l2);
        scraperwiki::scrape($url . $l2);
}
}

//print_r($links2);

die;


?>
