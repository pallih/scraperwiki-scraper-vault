<?php

# Blank PHP

require 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("http://casesearch.courts.state.md.us/inquiry/inquiryDetail.jis?caseId=2D00282711&loc=23&detailLoc=DSCR");
$html = str_get_html($html_content);

foreach ($html->find("div.bodywindow") as $el) {
    print $el . "value";
    print $el->href . "value";
}

$el = $html->find("div#bodywindow",0);
print $el . "value";

print $el->innertext . "value";








?>
<?php

# Blank PHP

require 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("http://casesearch.courts.state.md.us/inquiry/inquiryDetail.jis?caseId=2D00282711&loc=23&detailLoc=DSCR");
$html = str_get_html($html_content);

foreach ($html->find("div.bodywindow") as $el) {
    print $el . "value";
    print $el->href . "value";
}

$el = $html->find("div#bodywindow",0);
print $el . "value";

print $el->innertext . "value";








?>
