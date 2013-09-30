<?php
######################################
# City of Boston Press Release Scraper
# by JerseyCoder 
######################################

require  'scraperwiki/simple_html_dom.php';
$html = scraperwiki::scrape("http://www.cityofboston.gov/news/press_search.aspx");
$dom = new simple_html_dom();
$flag = false;
$numofpages = 0;
$i = 2;
# get the number of pages
$dom->load($html);
$pagelabelarr = $dom->find('span.pagelabel');
$lastelement  = $pagelabelarr[count($pagelabelarr)-2];
$numofpages = $lastelement->plaintext;

#scrape the first page
foreach($dom->find('span.news_title') as $data)
    {
        # Store data in the datastore
        print $data->plaintext . "\n";
        scraperwiki::save(array('data'), array('data' => $data->plaintext));
    }

# now do other pages
    while($i <= $numofpages) {
    $urlnu = "http://www.cityofboston.gov/news/press_search.aspx?search=1&sel_month=&sel_year=&page=" . $i;
    $html = scraperwiki::scrape($urlnu);
    # print $html;

    # Use the PHP Simple HTML DOM Parser to extract tags
    $dom = new simple_html_dom();
    $dom->load($html);

    foreach($dom->find('span.news_title') as $data)
    {
        # Store data in the datastore
        print $data->plaintext . "\n";
        $textdataesc = html_entity_decode($data->plaintext);
        $textdataesc = htmlspecialchars_decode($textdataesc, ENT_QUOTES);
        scraperwiki::save(array('data'), array('data' => $textdataesc));
    }
    $i = $i + 1;
}
?><?php
######################################
# City of Boston Press Release Scraper
# by JerseyCoder 
######################################

require  'scraperwiki/simple_html_dom.php';
$html = scraperwiki::scrape("http://www.cityofboston.gov/news/press_search.aspx");
$dom = new simple_html_dom();
$flag = false;
$numofpages = 0;
$i = 2;
# get the number of pages
$dom->load($html);
$pagelabelarr = $dom->find('span.pagelabel');
$lastelement  = $pagelabelarr[count($pagelabelarr)-2];
$numofpages = $lastelement->plaintext;

#scrape the first page
foreach($dom->find('span.news_title') as $data)
    {
        # Store data in the datastore
        print $data->plaintext . "\n";
        scraperwiki::save(array('data'), array('data' => $data->plaintext));
    }

# now do other pages
    while($i <= $numofpages) {
    $urlnu = "http://www.cityofboston.gov/news/press_search.aspx?search=1&sel_month=&sel_year=&page=" . $i;
    $html = scraperwiki::scrape($urlnu);
    # print $html;

    # Use the PHP Simple HTML DOM Parser to extract tags
    $dom = new simple_html_dom();
    $dom->load($html);

    foreach($dom->find('span.news_title') as $data)
    {
        # Store data in the datastore
        print $data->plaintext . "\n";
        $textdataesc = html_entity_decode($data->plaintext);
        $textdataesc = htmlspecialchars_decode($textdataesc, ENT_QUOTES);
        scraperwiki::save(array('data'), array('data' => $textdataesc));
    }
    $i = $i + 1;
}
?>