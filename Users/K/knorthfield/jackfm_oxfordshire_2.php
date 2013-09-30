<?php
$html = scraperWiki::scrape("https://www.iod.com/processes/Directory_Results.aspx?lf=&cc=&li=oxford");
require 'scraperwiki/simple_html_dom.php';
$directory = new simple_html_dom();
$directory->load($html);

foreach($directory->find(".directorytable") as $company){

    $name = explode ( ',', $company->find(".selectedleft strong", 0)->plaintext );

    $record = array(
        'company' => $company->find(".selectedleft strong strong a", 0)->plaintext,
        'name' => $name[0],
        'address' => str_replace ( 'Address:', '', $company->find("td", 2)->plaintext ),
        'phone' => $company->find(".phonelink", 0)->plaintext,
        'email' => $company->find(".mailtolink a", 0)->plaintext,
        'website' => $company->find(".weblink a", 0)->href,
        'notes' => str_replace ( 'Description: ', '', $company->find("td p", 1)->plaintext ),
    );

    scraperwiki::save(array('company'), $record);
    //print json_encode($record) . "\n";

}
?>
<?php
$html = scraperWiki::scrape("https://www.iod.com/processes/Directory_Results.aspx?lf=&cc=&li=oxford");
require 'scraperwiki/simple_html_dom.php';
$directory = new simple_html_dom();
$directory->load($html);

foreach($directory->find(".directorytable") as $company){

    $name = explode ( ',', $company->find(".selectedleft strong", 0)->plaintext );

    $record = array(
        'company' => $company->find(".selectedleft strong strong a", 0)->plaintext,
        'name' => $name[0],
        'address' => str_replace ( 'Address:', '', $company->find("td", 2)->plaintext ),
        'phone' => $company->find(".phonelink", 0)->plaintext,
        'email' => $company->find(".mailtolink a", 0)->plaintext,
        'website' => $company->find(".weblink a", 0)->href,
        'notes' => str_replace ( 'Description: ', '', $company->find("td p", 1)->plaintext ),
    );

    scraperwiki::save(array('company'), $record);
    //print json_encode($record) . "\n";

}
?>
