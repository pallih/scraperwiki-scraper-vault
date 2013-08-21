<?php /* FWIW: ScraperWiki is running PHP v5.3.5 */
define('DEBUG', false);

if (DEBUG) require_once 'scraperwiki.php';

require_once 'scraperwiki/simple_html_dom.php';


if (DEBUG) {
    require_once 'gasp_helper_php.php';
}
else
{
    require('https://scraperwiki.com/editor/raw/gasp_helper_php');    
}


define('URL_BASE', "http://burr.senate.gov/public/");

$gasp = new GaspHelper("YOUR_SUNLIGHT_KEY", "L000550");
// $URL_BASE = "http://burr.senate.gov/public/";


function get_full_url($path)
{
    return URL_BASE . htmlspecialchars_decode($path);
}

/**
 * Retrieve the dom for a page/path on the site
 *
 * @param string $path 
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
    $bio_path = 'index.cfm?FuseAction=AboutSenatorBurr.Biography';
    $bio_elem_id = 'copyMargins';
    $bio_sub_element = 'font';
    
    $dom = get_page_dom($bio_path);
    $search = 'div[id='. $bio_elem_id .'] ' . $bio_sub_element;
    print "Looking for '$search'\n";
    $bio_elem = $dom->find($search);
    print "Found bio div\n";
    $bio_txt = $bio_elem[0]->plaintext;
    print $bio_txt;
    if (!DEBUG) $gasp->add_biography($bio_txt);
}


/**
 * Scrape press releases from the press release front page.
 * TODO: scrape from RSS feed, since that should be less breakable/smarter
 * TODO: Handle present/past releases, not just the ones on the front page
 * 
 * @return void
 * @author Daniel Cloud
 */
function scrape_press_releases()
{
    global $gasp;
    $press_releases_path = 'index.cfm?FuseAction=PressOffice.PressReleases';
    $press_releases_list_class = 'pressrelease';
    $press_release_link_search = 'td[class=recordsTableItemLabel] a';

    $dom = get_page_dom($press_releases_path);
    $pr_anchors = $dom->find($press_release_link_search);
    $len=count($pr_anchors);
    print "found \$press_rel_links: $len\n\n";
    for ($i=0; $i < $len; $i++) { 
        $pr_dom = get_page_dom($pr_anchors[$i]->href);
        $content_el = "div[id=copyWrapper]";
        $find_title = $content_el . " h1[class=ContentView]";
        $title = $pr_dom->find($find_title, 0)->plaintext;
        $date_el = $content_el . " h4[class=ContentView]";
        $date_str = $pr_dom->find($date_el, 0)->plaintext;
        $graphs = $pr_dom->find($content_el . " p");
        $text = "";
        for ($n=0; $n < count($graphs); $n++) { 
            $text .= $graphs[$n]->outertext . "\n";
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
    $office_locations_path = 'index.cfm?FuseAction=Contact.OfficeLocations';
    $office_loc_search = "div[id=copyMargins] td td";
    
    $dom = get_page_dom($office_locations_path);
    $office_els = $dom->find($office_loc_search);
    
    $num_els = count($office_els);
    for ($o=0; $o < $num_els; $o++) { 
        print $office_els[$o]->plaintext . "\n\n";
        if (!DEBUG) $gasp->add_office($office_els[$o]->plaintext);
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
    $issues_list_path = 'index.cfm?FuseAction=IssueStatements.Home';
    $issues_list_search = 'ul[class=LinksList] li a';
    
    $dom = get_page_dom($issues_list_path);
    $issues_links_els = $dom->find($issues_list_search);
    
    $num_links = count($issues_links_els);
    
    for ($g=0; $g < $num_links; $g++) { 
        $issue_dom = get_page_dom($issues_links_els[$g]->href);
        $issue_page_copy = "div[id=copyWrapper]";
        $title = $issue_dom->find("h3[id=pageSubheader]", 0)->plaintext;
        print $title . "\n";
        $content = "";
        $issue_graphs = $issue_dom->find($issue_page_copy . " p");
        $num_graphs = count($issue_graphs);
        // print "num graphs: $num_graphs";
        for ($p=0; $p < $num_graphs; $p++) { 
            $content .=  $issue_graphs[$p]->outertext;
        }
        if (!DEBUG) $gasp->add_issue($title, $content, array("url"=> get_full_url($issues_links_els[$g]->href)));
        
    }
    
}

/**
 * Scrape events
 *      This page has little stuff on it for Sen. Burr. Maybe find better events listing?
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
    // if (!DEBUG) $gasp->add_event($title, $content, array("url"=> get_full_url($issues_links_els[$g]->href)));
}

/**
 * Scrape social media accounts (twitter, youtube, facebook, etc.)
 *
 * @return void
 * @author Daniel Cloud
 **/
function scrape_social_media()
{
}

/**
 * Run whichever scraper functions you need to
 */
// scrape_bio();
// scrape_press_releases();
// scrape_addresses();
//scrape_issues();
//scrape_events();

print phpinfo();

//print scraperwiki::get_var('scrapername');

//print_r(scraperwiki::getInfo());

//print_r(__FILE__);
//print "\n\nAaaannnnndd done.";

?>