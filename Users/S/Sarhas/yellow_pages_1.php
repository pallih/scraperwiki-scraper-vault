<?php 

require 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("http://www.yellowpages.com/92025/commercial-real-estate?q=commercial+real+estate");
$html = str_get_html($html_content);

foreach ($html->find("div.clearfix//a") as $el) {
    print $el . "\n";
    # scraperwiki.sqlite.save(unique_keys=["a"], data={"a":1});
}





?>
<?php 

require 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("http://www.yellowpages.com/92025/commercial-real-estate?q=commercial+real+estate");
$html = str_get_html($html_content);

foreach ($html->find("div.clearfix//a") as $el) {
    print $el . "\n";
    # scraperwiki.sqlite.save(unique_keys=["a"], data={"a":1});
}





?>
