<?php

require 'scraperwiki/simple_html_dom.php';

$share1 = str_get_html(scraperwiki::scrape("http://www.digitallook.com/companyresearch/10151/"));

$cn = $share1->find("div#contentHeader h1",0); 
$sp = $share1->find("div#sharePrice span",2);

$record = array(
        'share' => $cn->innertext, 
        'price' => $sp->plaintext 
    );

    scraperwiki::save(array('share'), $record);

$share2 = str_get_html(scraperwiki::scrape("http://www.digitallook.com/companyresearch/10014/"));

$cn = $share2->find("div#contentHeader h1",0); 
$sp = $share2->find("div#sharePrice span",2);

$record = array(
        'share' => $cn->innertext, 
        'price' => $sp->plaintext 
    );

    scraperwiki::save(array('share'), $record);


$share3 = str_get_html(scraperwiki::scrape("http://www.digitallook.com/companyresearch/10017/"));

$cn = $share3->find("div#contentHeader h1",0); 
$sp = $share3->find("div#sharePrice span",2);

$record = array(
        'share' => $cn->innertext, 
        'price' => $sp->plaintext 
    );

    scraperwiki::save(array('share'), $record);

$share4 = str_get_html(scraperwiki::scrape("http://www.digitallook.com/companyresearch/10033/"));

$cn = $share4->find("div#contentHeader h1",0); 
$sp = $share4->find("div#sharePrice span",2);

$record = array(
        'share' => $cn->innertext, 
        'price' => $sp->plaintext 
    );

    scraperwiki::save(array('share'), $record);

$share5 = str_get_html(scraperwiki::scrape("http://www.digitallook.com/companyresearch/10048/"));

$cn = $share5->find("div#contentHeader h1",0); 
$sp = $share5->find("div#sharePrice span",2);

$record = array(
        'share' => $cn->innertext, 
        'price' => $sp->plaintext 
    );

    scraperwiki::save(array('share'), $record);



$share6 = str_get_html(scraperwiki::scrape("http://www.digitallook.com/companyresearch/11856/"));

$cn = $share6->find("div#contentHeader h1",0); 
$sp = $share6->find("div#sharePrice span",2);

$record = array(
        'share' => $cn->innertext, 
        'price' => $sp->plaintext 
    );

    scraperwiki::save(array('share'), $record);

$share7 = str_get_html(scraperwiki::scrape("http://www.digitallook.com/companyresearch/10182/"));

$cn = $share7->find("div#contentHeader h1",0); 
$sp = $share7->find("div#sharePrice span",2);

$record = array(
        'share' => $cn->innertext, 
        'price' => $sp->plaintext 
    );

    scraperwiki::save(array('share'), $record);


?>
<?php

require 'scraperwiki/simple_html_dom.php';

$share1 = str_get_html(scraperwiki::scrape("http://www.digitallook.com/companyresearch/10151/"));

$cn = $share1->find("div#contentHeader h1",0); 
$sp = $share1->find("div#sharePrice span",2);

$record = array(
        'share' => $cn->innertext, 
        'price' => $sp->plaintext 
    );

    scraperwiki::save(array('share'), $record);

$share2 = str_get_html(scraperwiki::scrape("http://www.digitallook.com/companyresearch/10014/"));

$cn = $share2->find("div#contentHeader h1",0); 
$sp = $share2->find("div#sharePrice span",2);

$record = array(
        'share' => $cn->innertext, 
        'price' => $sp->plaintext 
    );

    scraperwiki::save(array('share'), $record);


$share3 = str_get_html(scraperwiki::scrape("http://www.digitallook.com/companyresearch/10017/"));

$cn = $share3->find("div#contentHeader h1",0); 
$sp = $share3->find("div#sharePrice span",2);

$record = array(
        'share' => $cn->innertext, 
        'price' => $sp->plaintext 
    );

    scraperwiki::save(array('share'), $record);

$share4 = str_get_html(scraperwiki::scrape("http://www.digitallook.com/companyresearch/10033/"));

$cn = $share4->find("div#contentHeader h1",0); 
$sp = $share4->find("div#sharePrice span",2);

$record = array(
        'share' => $cn->innertext, 
        'price' => $sp->plaintext 
    );

    scraperwiki::save(array('share'), $record);

$share5 = str_get_html(scraperwiki::scrape("http://www.digitallook.com/companyresearch/10048/"));

$cn = $share5->find("div#contentHeader h1",0); 
$sp = $share5->find("div#sharePrice span",2);

$record = array(
        'share' => $cn->innertext, 
        'price' => $sp->plaintext 
    );

    scraperwiki::save(array('share'), $record);



$share6 = str_get_html(scraperwiki::scrape("http://www.digitallook.com/companyresearch/11856/"));

$cn = $share6->find("div#contentHeader h1",0); 
$sp = $share6->find("div#sharePrice span",2);

$record = array(
        'share' => $cn->innertext, 
        'price' => $sp->plaintext 
    );

    scraperwiki::save(array('share'), $record);

$share7 = str_get_html(scraperwiki::scrape("http://www.digitallook.com/companyresearch/10182/"));

$cn = $share7->find("div#contentHeader h1",0); 
$sp = $share7->find("div#sharePrice span",2);

$record = array(
        'share' => $cn->innertext, 
        'price' => $sp->plaintext 
    );

    scraperwiki::save(array('share'), $record);


?>
