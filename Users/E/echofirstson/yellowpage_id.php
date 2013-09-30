<?php

require 'scraperwiki/simple_html_dom.php'; 

function scrap_yp($last_alphabet = '', $last_page = '')
{

$alphabet = range('a', 'z');

if(is_null($last_alphabet) || $last_alphabet == '')
{
    $temp_alphabet = scraperwiki::get_var('last_alphabet_loaded');

    if( !is_null($temp_alphabet))
    {
        
        $last_alphabet = $temp_alphabet;

    } else {
        $last_alphabet = 'a';
    }

}

if(is_null($last_page ) || $last_page == '')
{
    $temp_page = scraperwiki::get_var('last_page_loaded');

    if( !is_null($temp_page))
    {
        
        $last_page = $temp_page;

    } else {
        $last_page = 1;
    }

}


    $yp_base_url = 'http://www.yellowpages.co.id/browse/letter/'.$last_alphabet.'?page='.$last_page;

    $html = scraperWiki::scrape($yp_base_url);

    $dom = new simple_html_dom();

    $dom->load($html);

    foreach ($dom->find("ul.directory-list") as $data) {

echo $data;

    }


}

//scraperwiki::save_sqlite(array("yp"),array());

//scraperwiki::save_var('last_page', 27);           

scrap_yp();

?>
<?php

require 'scraperwiki/simple_html_dom.php'; 

function scrap_yp($last_alphabet = '', $last_page = '')
{

$alphabet = range('a', 'z');

if(is_null($last_alphabet) || $last_alphabet == '')
{
    $temp_alphabet = scraperwiki::get_var('last_alphabet_loaded');

    if( !is_null($temp_alphabet))
    {
        
        $last_alphabet = $temp_alphabet;

    } else {
        $last_alphabet = 'a';
    }

}

if(is_null($last_page ) || $last_page == '')
{
    $temp_page = scraperwiki::get_var('last_page_loaded');

    if( !is_null($temp_page))
    {
        
        $last_page = $temp_page;

    } else {
        $last_page = 1;
    }

}


    $yp_base_url = 'http://www.yellowpages.co.id/browse/letter/'.$last_alphabet.'?page='.$last_page;

    $html = scraperWiki::scrape($yp_base_url);

    $dom = new simple_html_dom();

    $dom->load($html);

    foreach ($dom->find("ul.directory-list") as $data) {

echo $data;

    }


}

//scraperwiki::save_sqlite(array("yp"),array());

//scraperwiki::save_var('last_page', 27);           

scrap_yp();

?>
