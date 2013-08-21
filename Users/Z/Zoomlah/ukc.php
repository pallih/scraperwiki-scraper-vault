<?php

$html = scraperWiki::scrape("http://www.kent.ac.uk/courses/modulecatalogue/modules/FR300");           
print $html . "\n";

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[@id='tab1']") as $data){
    $content = $data->find("div[@class='moduleText']");
    $record = array(
        'moduleContent' => $content[0]->plaintext, 
    );
    scraperwiki::save(array('moduleContent'), $record);
}

?>

<?php

$html = scraperWiki::scrape("http://www.kent.ac.uk/courses/modulecatalogue/modules/FR301");           
print $html . "\n";

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[@id='tab1']") as $data){
    $content = $data->find("div[@class='moduleText']");
    $record = array(
        'moduleContent' => $content[0]->plaintext, 
    );
    scraperwiki::save(array('moduleContent'), $record);
}

?>

<?php

$html = scraperWiki::scrape("http://www.kent.ac.uk/courses/modulecatalogue/modules/FR302");           
print $html . "\n";

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[@id='tab1']") as $data){
    $content = $data->find("div[@class='moduleText']");
    $record = array(
        'moduleContent' => $content[0]->plaintext, 
    );
    scraperwiki::save(array('moduleContent'), $record);
}

?>

<?php

$html = scraperWiki::scrape("http://www.kent.ac.uk/courses/modulecatalogue/modules/FR308");           
print $html . "\n";

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[@id='tab1']") as $data){
    $content = $data->find("div[@class='moduleText']");
    $record = array(
        'moduleContent' => $content[0]->plaintext, 
    );
    scraperwiki::save(array('moduleContent'), $record);
}

?>

<?php

$html = scraperWiki::scrape("http://www.kent.ac.uk/courses/modulecatalogue/modules/FR310");           
print $html . "\n";

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[@id='tab1']") as $data){
    $content = $data->find("div[@class='moduleText']");
    $record = array(
        'moduleContent' => $content[0]->plaintext, 
    );
    scraperwiki::save(array('moduleContent'), $record);
}

?>

<?php

$html = scraperWiki::scrape("http://www.kent.ac.uk/courses/modulecatalogue/modules/FR326");           
print $html . "\n";

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[@id='tab1']") as $data){
    $content = $data->find("div[@class='moduleText']");
    $record = array(
        'moduleContent' => $content[0]->plaintext, 
    );
    scraperwiki::save(array('moduleContent'), $record);
}

?>

<?php

$html = scraperWiki::scrape("http://www.kent.ac.uk/courses/modulecatalogue/modules/FR327");           
print $html . "\n";

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[@id='tab1']") as $data){
    $content = $data->find("div[@class='moduleText']");
    $record = array(
        'moduleContent' => $content[0]->plaintext, 
    );
    scraperwiki::save(array('moduleContent'), $record);
}

?>

<?php

$html = scraperWiki::scrape("http://www.kent.ac.uk/courses/modulecatalogue/modules/FR328");           
print $html . "\n";

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[@id='tab1']") as $data){
    $content = $data->find("div[@class='moduleText']");
    $record = array(
        'moduleContent' => $content[0]->plaintext, 
    );
    scraperwiki::save(array('moduleContent'), $record);
}

?>

<?php

$html = scraperWiki::scrape("http://www.kent.ac.uk/courses/modulecatalogue/modules/FR330");           
print $html . "\n";

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[@id='tab1']") as $data){
    $content = $data->find("div[@class='moduleText']");
    $record = array(
        'moduleContent' => $content[0]->plaintext, 
    );
    scraperwiki::save(array('moduleContent'), $record);
}

?>

<?php

$html = scraperWiki::scrape("http://www.kent.ac.uk/courses/modulecatalogue/modules/FR331");           
print $html . "\n";

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[@id='tab1']") as $data){
    $content = $data->find("div[@class='moduleText']");
    $record = array(
        'moduleContent' => $content[0]->plaintext, 
    );
    scraperwiki::save(array('moduleContent'), $record);
}

?>

<?php

$html = scraperWiki::scrape("http://www.kent.ac.uk/courses/modulecatalogue/modules/FR332");           
print $html . "\n";

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[@id='tab1']") as $data){
    $content = $data->find("div[@class='moduleText']");
    $record = array(
        'moduleContent' => $content[0]->plaintext, 
    );
    scraperwiki::save(array('moduleContent'), $record);
}

?>

<?php

$html = scraperWiki::scrape("http://www.kent.ac.uk/courses/modulecatalogue/modules/FR334");           
print $html . "\n";

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[@id='tab1']") as $data){
    $content = $data->find("div[@class='moduleText']");
    $record = array(
        'moduleContent' => $content[0]->plaintext, 
    );
    scraperwiki::save(array('moduleContent'), $record);
}

?>

<?php

$html = scraperWiki::scrape("http://www.kent.ac.uk/courses/modulecatalogue/modules/FR335");           
print $html . "\n";

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[@id='tab1']") as $data){
    $content = $data->find("div[@class='moduleText']");
    $record = array(
        'moduleContent' => $content[0]->plaintext, 
    );
    scraperwiki::save(array('moduleContent'), $record);
}

?>