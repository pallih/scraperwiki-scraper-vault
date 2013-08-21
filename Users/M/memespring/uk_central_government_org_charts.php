<?php
######################################
# Links to government org charts
######################################

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://transparency.number10.gov.uk/org-charts.php");

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find('ul.section-list li') as $li) {

    # Store data in the datastore
    $department = $li->plaintext;
    $link_partial = $li->children(0)->href;
    $link_full = '';
    if (strpos($link_partial, '/') === 0){
        $link_full = ('http://transparency.number10.gov.uk' + $link_partial);
    }else{
        $link_full = $link_partial;
    }
    print "hello\n";
    scraperwiki::save(array('link'), array('link' => $link_full, 'department' => $department));
}
print "eek"; 

?>