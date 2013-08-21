<?php /* FWIW: ScraperWiki is running PHP v5.3.5 */
define('DEBUG', false);

if (DEBUG) require_once 'scraperwiki.php';

require_once 'scraperwiki/simple_html_dom.php';

if (DEBUG) { require_once 'gasp_helper_php.php'; } else { require('https://scraperwiki.com/editor/raw/gasp_helper_php'); }


define('URL_BASE', "http://price.house.gov/");

$gasp = new GaspHelper("aacf0db461fe47179a15f3c5422100dc", "P000523", "rep_david_price_scraper");


function get_full_url($path)
{
    return URL_BASE . htmlspecialchars_decode($path);
}

/**
 * Retrieve the dom for a page/path on the site
 *
 * @param string $path (the path portion of the url)
 * @return void
 * @author Daniel Cloud
 */
function get_page_dom($path)
{
    $url = get_full_url($path);
    print "Retrieving '" . $url . "'\n";
    $html = null;
    $html = scraperWiki::scrape($url);
    $dom = null;
    $dom = new simple_html_dom();
    $dom->load($html);
    return $dom;
}


/**
 * scrape_bio 
 *  Scrape and store the bio using GaspHelper.
 *
 * @return void
 * @author Daniel Cloud
 */
function scrape_bio()
{
    global $gasp;
    $bio_path = 'index.php?option=com_content&view=article&id=2444&Itemid=100225';
    $bio_elem_id = 'mainContent';
    
    $dom = get_page_dom($bio_path);
    $search = 'div[id='. $bio_elem_id .'] p';
    print "Looking for '$search'\n";
    $bio_elems = $dom->find($search);
    print "Found bio div\n";
    $bio_txt = "";
    for ($i=0; $i < count($bio_elems); $i++) { $bio_txt .= $bio_elems[$i]->outertext; }
    print $bio_txt;
    if (!DEBUG) $gasp->add_biography($bio_txt);
}


/**
 * Scrape press releases from the press release front page.
 * TODO: Handle present/past releases. We don't need to retrieve all of them every time.
 * 
 * @return void
 * @author Daniel Cloud
 */
function scrape_press_releases()
{
    global $gasp;
    $press_releases_path = 'index.php?option=com_content&view=article&id=2536&Itemid=100260';
    $press_release_link_search = 'div[id=mainContent] li a';

    $dom = get_page_dom($press_releases_path);
    $pr_anchors = $dom->find($press_release_link_search);
    $len=count($pr_anchors);
    print "found \$press_rel_links: $len\n\n";
    for ($i=0; $i < $len; $i++) { 
        $pr_dom = get_page_dom($pr_anchors[$i]->href);
        $content_el = "div[id=mainContent]";
        $find_title = $content_el . " td[class=contentheading]";
        $title = trim($pr_dom->find($find_title, 0)->plaintext);
        $date_el = $content_el . " td[class=createdate]";
        $date_str = trim($pr_dom->find($date_el, 0)->plaintext);
        $graphs = $pr_dom->find($content_el . " p");
        $text = "";
        for ($n=0; $n < count($graphs); $n++) { 
            $text .= $graphs[$n]->outertext;
        }
        print $date_str . "\n" . $title . "\n" . $text . "\n\n";
        if (!DEBUG) $gasp->add_press_release($title, $date_str, $text);
    }
}

/**
 * Scrape addresses from the office locations page
 *
 * @return void
 * @author Daniel Cloud
 **/
function scrape_addresses()
{
    global $gasp;
    $office_locations_path = '';
    $office_loc_search = "div[id=footer] p";
    $phone_regex = '/\d{3}\.\d{3}\.\d{4}/';
    
    $dom = get_page_dom($office_locations_path);
    $office_els = $dom->find($office_loc_search);
    
    $num_els = count($office_els);
    for ($o=0; $o < $num_els; $o++) { 
        print $office_els[$o]->outertext . "\n";
        // Getting phone out would require a regex
        
        $matches = array();
        preg_match($phone_regex, $office_els[$o]->outertext, $matches);
        
        print "Phone number is " . $matches[0] . "\n\n";

        if (!DEBUG) $gasp->add_office($office_els[$o]->outertext, $matches[0]);
    }
}

/**
 * Scrape issues from the issues pages.
 *
 * @return void
 * @author Daniel Cloud
 **/
function scrape_issues()
{
    global $gasp;
    $issues_list_path = 'index.php?option=com_content&view=article&id=2478&Itemid=100240';
    $contentarea_el = 'div[id=mainContent]';
    $issues_list_search = $contentarea_el . ' li a';
    
    $dom = get_page_dom($issues_list_path);
    $issues_links_els = $dom->find($issues_list_search);
    
    $num_links = count($issues_links_els);
    for ($g=0; $g < $num_links; $g++) { 
        $issue_dom = get_page_dom($issues_links_els[$g]->href);
        $title = trim($issue_dom->find("td[class=contentheading]", 0)->plaintext);
        print $title . "\n";
        $content = "";
        $issue_graphs = $issue_dom->find($contentarea_el . " p");
        $num_graphs = count($issue_graphs);
        for ($p=0; $p < $num_graphs; $p++) { 
            $content .=  $issue_graphs[$p]->outertext;
        }
        print $content . "\n";
        if (!DEBUG) $gasp->add_issue($title, $content, array("url"=> get_full_url($issues_links_els[$g]->href)));
    }
}

/**
 * Scrape events
 * @return void
 * @author Daniel Cloud
 **/
function scrape_events()
{
    global $gasp;
    $events_path = 'index.cfm?FuseAction=Events.Home';
    $events_page_copy = 'div[id=copyWrapper]';
    $events_dom = get_page_dom($events_path);
    $content = $events_dom->find($events_page_copy, 0)->innertext;
    print $content;
    // if (!DEBUG) $gasp->add_event($title, $date, $location, array("url"=> get_full_url($issues_links_els[$g]->href)));
}

/**
 * Scrape social media accounts (twitter, youtube, facebook, etc.)
 *
 * @return void
 * @author Daniel Cloud
 **/
function scrape_social_media()
{
    global $gasp;
    print "Youtube is http://www.youtube.com/user/RepDavidPrice\n";
    if (!DEBUG) $gasp->add_youtube('http://www.youtube.com/user/RepDavidPrice');
    print "Flickr http://www.flickr.com/photos/repdavidprice/\n";
    if (!DEBUG) $gasp->add_flickr('http://www.flickr.com/photos/repdavidprice/');
    print "Twitter http://twitter.com/#!/RepDavidEPrice\n";
    if (!DEBUG) $gasp->add_twitter('http://twitter.com/#!/RepDavidEPrice');
    // David Price's Facebook page isn't listed (prominently) on his website.
    print "Facebook https://www.facebook.com/pages/David-Price/8338225975\n";
    if (!DEBUG) $gasp->add_facebook('https://www.facebook.com/pages/David-Price/8338225975');
}

/**
 * Run whichever scraper functions you need to
 */
scrape_bio();
scrape_press_releases();
scrape_addresses();
scrape_issues();
scrape_events();
scrape_social_media();
if (!DEBUG) $gasp->finish();
?>