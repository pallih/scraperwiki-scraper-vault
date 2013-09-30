<?php

require 'scraperwiki/simple_html_dom.php';

$clans = array();

//Clan scrape src
$html = scraperWiki::scrape("http://en.wikipedia.org/wiki/List_of_Scottish_clans"); 

//Load src
$dom = new simple_html_dom();
$dom->load($html);

//Load table as object
$table = $dom->find("table.wikitable");
$data = new simple_html_dom();
$data->load($table[0]);

//Load $rows as array
$rows = $dom->find('table.wikitable tr');
array_shift($rows);

//Scrape clan info
foreach($rows as $row) {

    $clan = array();

    //Verify there are 5 columns (redundancy, redundancy, redundancy)
    $tds = $row->find('td');
    if(count($tds) == 5) {

        $clan['name'] = $tds[0]->plaintext;
        
        //Get Wikipedia URL if it exists
        if($tds[0]->find('a' , 0))
            $clan['url'] = 'http://en.wikipedia.org' . $tds[0]->find('a' , 0)->href;
        else
            $clan['url'] = '';

        //Get crest image url
        if($tds[1]->find('a' , 0))
            $clan['crest']['img'] = 'http://en.wikipedia.org' . $tds[1]->find('a' , 0)->href;
        else
            $clan['crest']['img'] = '';

        //Get motto origin
        if($tds[2]->find('small' , 0))
            $clan['motto']['origin'] = $tds[2]->find('small' , 0)->plaintext;
        else
            $clan['motto']['origin'] = '';

        //Get crest description
        if($tds[2]->find('b' , 0) && $tds[2]->find('b' , 0)->plaintext == 'Crest:') {
            $clan['crest']['description'] = $tds[2]->find('b' , 0)->nextSibling()->plaintext;
        }
        else
            $clan['crest']['description'] = '';

        //Get motto
        if($tds[2]->find('b' , 1) && $tds[2]->find('b' , 1)->plaintext == 'Motto:')
            $clan['motto']['motto'] = $tds[2]->find('b' , 1)->nextSibling()->plaintext;
        else
            $clan['motto']['motto'] = '';

        //Get chief
        if($tds[3]->find('b' , 0) && $tds[3]->find('b' , 0)->plaintext == 'Chief:') {
            $clan['chief'] = $tds[3]->find('b' , 0)->plaintext;
        }
        else
            $clan['chief'] = '';
        
        //Get seat
        if($tds[3]->find('b' , 1) && $tds[3]->find('b' , 1)->plaintext == 'Seat:') {
            $clan['seat'] = $tds[3]->find('b' , 1)->plaintext;
        }
        else
            $clan['seat'] = '';

        //Get notes
        if($tds[4]->find('small')) {
            $facts = array();
            foreach($tds[4]->find('small') as $fact) array_push($facts , $fact);
            $clan['facts'] = $facts;
        }
        else $clan['facts'] = '';

        print 'name: ' . $clan['name'] . "\n";
        print 'url: ' . $clan['url'] . "\n";
        print 'crest image: ' . $clan['crest']['img'] . "\n";
        print 'crest description: ' . $clan['crest']['description'] . "\n";
        print 'motto: ' . $clan['motto']['motto'] . "\n";
        print 'motto origin: ' . $clan['motto']['origin'] . "\n";
        print 'chief: ' . $clan['chief'] . "\n";
        print 'seat: ' . $clan['seat'] . "\n";
        print 'facts: ' . $clan['facts'] . "\n";
    }

    //Get clan region
    if($row->style) {
        if($row->style == 'background:#faecc8;') $clan['region'] = 'Lowland/Border';
        elseif($row->style == 'background:#d0e5f5;') $clan['region'] = 'Highland/Island';
        else{$clan['region'] = '';}
    }
    else{$clan['region'] = '';}
}

?>
<?php

require 'scraperwiki/simple_html_dom.php';

$clans = array();

//Clan scrape src
$html = scraperWiki::scrape("http://en.wikipedia.org/wiki/List_of_Scottish_clans"); 

//Load src
$dom = new simple_html_dom();
$dom->load($html);

//Load table as object
$table = $dom->find("table.wikitable");
$data = new simple_html_dom();
$data->load($table[0]);

//Load $rows as array
$rows = $dom->find('table.wikitable tr');
array_shift($rows);

//Scrape clan info
foreach($rows as $row) {

    $clan = array();

    //Verify there are 5 columns (redundancy, redundancy, redundancy)
    $tds = $row->find('td');
    if(count($tds) == 5) {

        $clan['name'] = $tds[0]->plaintext;
        
        //Get Wikipedia URL if it exists
        if($tds[0]->find('a' , 0))
            $clan['url'] = 'http://en.wikipedia.org' . $tds[0]->find('a' , 0)->href;
        else
            $clan['url'] = '';

        //Get crest image url
        if($tds[1]->find('a' , 0))
            $clan['crest']['img'] = 'http://en.wikipedia.org' . $tds[1]->find('a' , 0)->href;
        else
            $clan['crest']['img'] = '';

        //Get motto origin
        if($tds[2]->find('small' , 0))
            $clan['motto']['origin'] = $tds[2]->find('small' , 0)->plaintext;
        else
            $clan['motto']['origin'] = '';

        //Get crest description
        if($tds[2]->find('b' , 0) && $tds[2]->find('b' , 0)->plaintext == 'Crest:') {
            $clan['crest']['description'] = $tds[2]->find('b' , 0)->nextSibling()->plaintext;
        }
        else
            $clan['crest']['description'] = '';

        //Get motto
        if($tds[2]->find('b' , 1) && $tds[2]->find('b' , 1)->plaintext == 'Motto:')
            $clan['motto']['motto'] = $tds[2]->find('b' , 1)->nextSibling()->plaintext;
        else
            $clan['motto']['motto'] = '';

        //Get chief
        if($tds[3]->find('b' , 0) && $tds[3]->find('b' , 0)->plaintext == 'Chief:') {
            $clan['chief'] = $tds[3]->find('b' , 0)->plaintext;
        }
        else
            $clan['chief'] = '';
        
        //Get seat
        if($tds[3]->find('b' , 1) && $tds[3]->find('b' , 1)->plaintext == 'Seat:') {
            $clan['seat'] = $tds[3]->find('b' , 1)->plaintext;
        }
        else
            $clan['seat'] = '';

        //Get notes
        if($tds[4]->find('small')) {
            $facts = array();
            foreach($tds[4]->find('small') as $fact) array_push($facts , $fact);
            $clan['facts'] = $facts;
        }
        else $clan['facts'] = '';

        print 'name: ' . $clan['name'] . "\n";
        print 'url: ' . $clan['url'] . "\n";
        print 'crest image: ' . $clan['crest']['img'] . "\n";
        print 'crest description: ' . $clan['crest']['description'] . "\n";
        print 'motto: ' . $clan['motto']['motto'] . "\n";
        print 'motto origin: ' . $clan['motto']['origin'] . "\n";
        print 'chief: ' . $clan['chief'] . "\n";
        print 'seat: ' . $clan['seat'] . "\n";
        print 'facts: ' . $clan['facts'] . "\n";
    }

    //Get clan region
    if($row->style) {
        if($row->style == 'background:#faecc8;') $clan['region'] = 'Lowland/Border';
        elseif($row->style == 'background:#d0e5f5;') $clan['region'] = 'Highland/Island';
        else{$clan['region'] = '';}
    }
    else{$clan['region'] = '';}
}

?>
<?php

require 'scraperwiki/simple_html_dom.php';

$clans = array();

//Clan scrape src
$html = scraperWiki::scrape("http://en.wikipedia.org/wiki/List_of_Scottish_clans"); 

//Load src
$dom = new simple_html_dom();
$dom->load($html);

//Load table as object
$table = $dom->find("table.wikitable");
$data = new simple_html_dom();
$data->load($table[0]);

//Load $rows as array
$rows = $dom->find('table.wikitable tr');
array_shift($rows);

//Scrape clan info
foreach($rows as $row) {

    $clan = array();

    //Verify there are 5 columns (redundancy, redundancy, redundancy)
    $tds = $row->find('td');
    if(count($tds) == 5) {

        $clan['name'] = $tds[0]->plaintext;
        
        //Get Wikipedia URL if it exists
        if($tds[0]->find('a' , 0))
            $clan['url'] = 'http://en.wikipedia.org' . $tds[0]->find('a' , 0)->href;
        else
            $clan['url'] = '';

        //Get crest image url
        if($tds[1]->find('a' , 0))
            $clan['crest']['img'] = 'http://en.wikipedia.org' . $tds[1]->find('a' , 0)->href;
        else
            $clan['crest']['img'] = '';

        //Get motto origin
        if($tds[2]->find('small' , 0))
            $clan['motto']['origin'] = $tds[2]->find('small' , 0)->plaintext;
        else
            $clan['motto']['origin'] = '';

        //Get crest description
        if($tds[2]->find('b' , 0) && $tds[2]->find('b' , 0)->plaintext == 'Crest:') {
            $clan['crest']['description'] = $tds[2]->find('b' , 0)->nextSibling()->plaintext;
        }
        else
            $clan['crest']['description'] = '';

        //Get motto
        if($tds[2]->find('b' , 1) && $tds[2]->find('b' , 1)->plaintext == 'Motto:')
            $clan['motto']['motto'] = $tds[2]->find('b' , 1)->nextSibling()->plaintext;
        else
            $clan['motto']['motto'] = '';

        //Get chief
        if($tds[3]->find('b' , 0) && $tds[3]->find('b' , 0)->plaintext == 'Chief:') {
            $clan['chief'] = $tds[3]->find('b' , 0)->plaintext;
        }
        else
            $clan['chief'] = '';
        
        //Get seat
        if($tds[3]->find('b' , 1) && $tds[3]->find('b' , 1)->plaintext == 'Seat:') {
            $clan['seat'] = $tds[3]->find('b' , 1)->plaintext;
        }
        else
            $clan['seat'] = '';

        //Get notes
        if($tds[4]->find('small')) {
            $facts = array();
            foreach($tds[4]->find('small') as $fact) array_push($facts , $fact);
            $clan['facts'] = $facts;
        }
        else $clan['facts'] = '';

        print 'name: ' . $clan['name'] . "\n";
        print 'url: ' . $clan['url'] . "\n";
        print 'crest image: ' . $clan['crest']['img'] . "\n";
        print 'crest description: ' . $clan['crest']['description'] . "\n";
        print 'motto: ' . $clan['motto']['motto'] . "\n";
        print 'motto origin: ' . $clan['motto']['origin'] . "\n";
        print 'chief: ' . $clan['chief'] . "\n";
        print 'seat: ' . $clan['seat'] . "\n";
        print 'facts: ' . $clan['facts'] . "\n";
    }

    //Get clan region
    if($row->style) {
        if($row->style == 'background:#faecc8;') $clan['region'] = 'Lowland/Border';
        elseif($row->style == 'background:#d0e5f5;') $clan['region'] = 'Highland/Island';
        else{$clan['region'] = '';}
    }
    else{$clan['region'] = '';}
}

?>
<?php

require 'scraperwiki/simple_html_dom.php';

$clans = array();

//Clan scrape src
$html = scraperWiki::scrape("http://en.wikipedia.org/wiki/List_of_Scottish_clans"); 

//Load src
$dom = new simple_html_dom();
$dom->load($html);

//Load table as object
$table = $dom->find("table.wikitable");
$data = new simple_html_dom();
$data->load($table[0]);

//Load $rows as array
$rows = $dom->find('table.wikitable tr');
array_shift($rows);

//Scrape clan info
foreach($rows as $row) {

    $clan = array();

    //Verify there are 5 columns (redundancy, redundancy, redundancy)
    $tds = $row->find('td');
    if(count($tds) == 5) {

        $clan['name'] = $tds[0]->plaintext;
        
        //Get Wikipedia URL if it exists
        if($tds[0]->find('a' , 0))
            $clan['url'] = 'http://en.wikipedia.org' . $tds[0]->find('a' , 0)->href;
        else
            $clan['url'] = '';

        //Get crest image url
        if($tds[1]->find('a' , 0))
            $clan['crest']['img'] = 'http://en.wikipedia.org' . $tds[1]->find('a' , 0)->href;
        else
            $clan['crest']['img'] = '';

        //Get motto origin
        if($tds[2]->find('small' , 0))
            $clan['motto']['origin'] = $tds[2]->find('small' , 0)->plaintext;
        else
            $clan['motto']['origin'] = '';

        //Get crest description
        if($tds[2]->find('b' , 0) && $tds[2]->find('b' , 0)->plaintext == 'Crest:') {
            $clan['crest']['description'] = $tds[2]->find('b' , 0)->nextSibling()->plaintext;
        }
        else
            $clan['crest']['description'] = '';

        //Get motto
        if($tds[2]->find('b' , 1) && $tds[2]->find('b' , 1)->plaintext == 'Motto:')
            $clan['motto']['motto'] = $tds[2]->find('b' , 1)->nextSibling()->plaintext;
        else
            $clan['motto']['motto'] = '';

        //Get chief
        if($tds[3]->find('b' , 0) && $tds[3]->find('b' , 0)->plaintext == 'Chief:') {
            $clan['chief'] = $tds[3]->find('b' , 0)->plaintext;
        }
        else
            $clan['chief'] = '';
        
        //Get seat
        if($tds[3]->find('b' , 1) && $tds[3]->find('b' , 1)->plaintext == 'Seat:') {
            $clan['seat'] = $tds[3]->find('b' , 1)->plaintext;
        }
        else
            $clan['seat'] = '';

        //Get notes
        if($tds[4]->find('small')) {
            $facts = array();
            foreach($tds[4]->find('small') as $fact) array_push($facts , $fact);
            $clan['facts'] = $facts;
        }
        else $clan['facts'] = '';

        print 'name: ' . $clan['name'] . "\n";
        print 'url: ' . $clan['url'] . "\n";
        print 'crest image: ' . $clan['crest']['img'] . "\n";
        print 'crest description: ' . $clan['crest']['description'] . "\n";
        print 'motto: ' . $clan['motto']['motto'] . "\n";
        print 'motto origin: ' . $clan['motto']['origin'] . "\n";
        print 'chief: ' . $clan['chief'] . "\n";
        print 'seat: ' . $clan['seat'] . "\n";
        print 'facts: ' . $clan['facts'] . "\n";
    }

    //Get clan region
    if($row->style) {
        if($row->style == 'background:#faecc8;') $clan['region'] = 'Lowland/Border';
        elseif($row->style == 'background:#d0e5f5;') $clan['region'] = 'Highland/Island';
        else{$clan['region'] = '';}
    }
    else{$clan['region'] = '';}
}

?>
