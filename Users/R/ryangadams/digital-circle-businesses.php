<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';
$base_url = "http://digitalcircle.org";
$index_page = "http://digitalcircle.org/businesses/";

parseIndexPage($index_page);

function parseIndexPage($url)
{
global $base_url;

    $html = scraperwiki::scrape($url);
    
    # Use the PHP Simple HTML DOM Parser to extract <td> tags
    $dom = new simple_html_dom();
    $dom->load($html);
    
    foreach($dom->find('article.business') as $business)
    {
        $link = $business->children(1)->first_child()->first_child();
        $business_link = $link->href;
        $business_id = substr($business_link, strrpos($business_link, "/")+1);
        parseBusinessPage($business_id);
    }
    $next = $dom->find("div.pagination a.next_page",0)->href;
    print $next;
    if($next)
    {
        $urlToParse = $base_url . $next;
        print $urlToParse;
        parseIndexPage($urlToParse);
    }


}

function parseBusinessPage($business_id)
{
    $business_link = "http://digitalcircle.org/businesses/" . $business_id;
    $page = scraperwiki::scrape($business_link);
    $business = new simple_html_dom();
    $business->load($page);

    $business_array = array();
    $business_array['business_id'] = $business_id;
    $business_array['name'] = $business->find("article.business header h1.org",0)->plaintext;
    $business_array['desc'] = $business->find("article.business section.description",0)->plaintext;
    $business_array['skills'] = "";
    foreach($business->find("#skills ul li a") as $skill)
    {
        $business_array['skills'] = $business_array['skills'] . $skill->plaintext . ":/:";
    }
    $sector_url = $business->find("dd a[href*=sector]",0)->href;
    if($sector_url != "")
    {    
        $sector = explode("sector=",$sector_url);
        $business_array['sector'] = array_pop($sector);
    }
    $business_array['url'] = $business->find("ul#contact a.url",0)->href;
    $business_array['location'] = $business->find("aside.sidebar span.locality",0)->plaintext;


    

    scraperwiki::save_sqlite(array('business_id'), $business_array);
}
?>