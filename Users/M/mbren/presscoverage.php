<?php
require  'scraperwiki/simple_html_dom.php';

# start on main press page. 

$html = scraperwiki::scrape("www.avigilon.com/company/coverage/");
$dom = new simple_html_dom();
$dom->load($html);

# grab all content in the div main-col. for each link, <a href> a href="/company/press/070411.htm", load the url and grab title, summary and body.

foreach($dom->find('div[id=main-col]') as $data) {
    foreach($data->find('a') as $item) {
        # print $item;   
        # grab the url that comes between "a href=" and the "&" in the embed code.
        if (preg_match('@a href=([^>]+)@i', $item, $matches)) {
            #print $matches[0];  #a href="/company/press/070411.htm"
            $myUrlEnd = explode('"', $matches[0]);
            #print $myUrlEnd[1]; #  /company/press/070411.htm
            $pressRelUrl = "www.avigilon.com" . $myUrlEnd[1];
            #print $pressRelUrl;
            $html2 = scraperwiki::scrape($pressRelUrl);
            $dom2 = new simple_html_dom();
            $dom2->load($html2);
            print $html2;
            #foreach($dom2->find('div[id=main-col]') as $all) {
                #print $all;                
            #}
        }
    }
}
?>
<?php
require  'scraperwiki/simple_html_dom.php';

# start on main press page. 

$html = scraperwiki::scrape("www.avigilon.com/company/coverage/");
$dom = new simple_html_dom();
$dom->load($html);

# grab all content in the div main-col. for each link, <a href> a href="/company/press/070411.htm", load the url and grab title, summary and body.

foreach($dom->find('div[id=main-col]') as $data) {
    foreach($data->find('a') as $item) {
        # print $item;   
        # grab the url that comes between "a href=" and the "&" in the embed code.
        if (preg_match('@a href=([^>]+)@i', $item, $matches)) {
            #print $matches[0];  #a href="/company/press/070411.htm"
            $myUrlEnd = explode('"', $matches[0]);
            #print $myUrlEnd[1]; #  /company/press/070411.htm
            $pressRelUrl = "www.avigilon.com" . $myUrlEnd[1];
            #print $pressRelUrl;
            $html2 = scraperwiki::scrape($pressRelUrl);
            $dom2 = new simple_html_dom();
            $dom2->load($html2);
            print $html2;
            #foreach($dom2->find('div[id=main-col]') as $all) {
                #print $all;                
            #}
        }
    }
}
?>
