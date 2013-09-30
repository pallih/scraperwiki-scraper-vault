<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://agency.governmentjobs.com/seattle/default.cfm");

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);

$count = 0;
$headers[] = 'id';
$headers[] = 'link';
$headers[] = 'position';
$headers[] = 'employment_type';
$headers[] = 'salary';
$headers[] = 'opening';
$headers[] = 'closing';
foreach($dom->find('table.NEOGOV_joblist tr') as $data) {
    $records = array();
    
    // First row is headers
    if ($count != 0) {
        $records['id'] = $count;
        $subcount = 2;

        foreach ($data->find('td') as $subdata) {
            // Get link from first column
            if ($subcount == 2) {
                $subelements = $subdata->find('a');
                $records['link'] = 'http://agency.governmentjobs.com/seattle/' . $subelements[0]->href;
            }
            $records[$headers[$subcount]] = trim(str_replace('&nbsp;', '', strip_tags($subdata->plaintext)));
            $subcount += 1;
        }
    }

    // Store data in the datastore
    if (!empty($records)) {
        scraperwiki::save(array('id'), $records);
    }

    $count += 1;
}

?><?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://agency.governmentjobs.com/seattle/default.cfm");

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);

$count = 0;
$headers[] = 'id';
$headers[] = 'link';
$headers[] = 'position';
$headers[] = 'employment_type';
$headers[] = 'salary';
$headers[] = 'opening';
$headers[] = 'closing';
foreach($dom->find('table.NEOGOV_joblist tr') as $data) {
    $records = array();
    
    // First row is headers
    if ($count != 0) {
        $records['id'] = $count;
        $subcount = 2;

        foreach ($data->find('td') as $subdata) {
            // Get link from first column
            if ($subcount == 2) {
                $subelements = $subdata->find('a');
                $records['link'] = 'http://agency.governmentjobs.com/seattle/' . $subelements[0]->href;
            }
            $records[$headers[$subcount]] = trim(str_replace('&nbsp;', '', strip_tags($subdata->plaintext)));
            $subcount += 1;
        }
    }

    // Store data in the datastore
    if (!empty($records)) {
        scraperwiki::save(array('id'), $records);
    }

    $count += 1;
}

?>