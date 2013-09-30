<?php
require 'scraperwiki/simple_html_dom.php';  

$pageurl = "http://education.staffordshire.gov.uk/Directories/SchoolDirectory/Search.aspx?txtName=&txtArea=&lstSchoolType=All&lstDistricts=All&txtPostcode=&recordCount=458&pageId=0";

$html = scraperWiki::scrape($pageurl); 
                  
$dom = new simple_html_dom();
$dom->load($html);

$panel = $dom->find('#Panel1 > table h3', 0);

$totals = explode("of", $panel->plaintext);

$pages = $totals[1];

$num = 0;

for ($i = 0; $i <= $pages; $i++) {

$html = scraperWiki::scrape("http://education.staffordshire.gov.uk/Directories/SchoolDirectory/Search.aspx?txtName=&txtArea=&lstSchoolType=All&lstDistricts=All&txtPostcode=&recordCount=458&pageId=". $i); 

$dom = new simple_html_dom();
$dom->load($html);

$records = $dom->find('tr.topicRow');

foreach ($records as $record) {

    $col = $record->find('td');

    $school = Array(
        'name' => "",
        'url' => "",
        'WWW Address' => "",
        'Address (Line 1)' => "",
        'Address (Line 2)' => "",
        'Address (Line 3)' => "",
        'Town' => "",
        'Fax' => "",
        'Telephone' => "",
        'District' => "",
        'E-Mail' => "",
        'DfES Number' => "",
        'lat' => "",
        'lng' => "",
        'District' => "",
        'School Type' => "",
        'Post Code' => "",
    );
    
    $school['name'] = trim($col[1]->plaintext);
    $school['url'] = trim("http://education.staffordshire.gov.uk/Directories/SchoolDirectory/". html_entity_decode($col[1]->find('a', 0)->href));

    $html = scraperWiki::scrape($school['url']); 
    
    $dom = new simple_html_dom();
    $dom->load($html);
    
    $rows = $dom->find('#tblDetails tr');
    
    foreach ($rows as $row) {
        $school[trim($row->find('td', 0)->plaintext)] = trim($row->find('td', 1)->plaintext);
    }
    
    if ($school['WWW Address'] == "Add your Schools Web site by clicking this link!") {
        $school['WWW Address'] = "";
    }
    
    if (empty($school['Address (Line 2)'])) {
        $school['Address (Line 2)'] = "";
    }
    
    if (empty($school['Address (Line 3)'])) {
        $school['Address (Line 3)'] = "";
    }

    if (empty($school['Town'])) {
        $school['Town'] = "";
    }

    if (empty($school['Fax'])) {
        $school['Fax'] = "";
    }
    
    if (empty($school['District'])) {
        $school['District'] = trim($col[2]->plaintext);
    }

    unset($school['E-Mail WWW Address']);

    $school['easting'] = $dom->find('#MapControl1_hidCentreEasting', 0)->value;
    $school['northing'] = $dom->find('#MapControl1_hidCentreNorthing', 0)->value;
    
    $json = json_decode(scraperWiki::scrape("http://www.uk-postcodes.com/eastingnorthing.php?easting=". $school['easting'] ."&northing=". $school['northing']));
    
    $school['lat'] = $json->lat;
    $school['lng'] = $json->lng;
    
    scraperwiki::save_sqlite(array('DfES Number'), $school); 

}

}
?>
<?php
require 'scraperwiki/simple_html_dom.php';  

$pageurl = "http://education.staffordshire.gov.uk/Directories/SchoolDirectory/Search.aspx?txtName=&txtArea=&lstSchoolType=All&lstDistricts=All&txtPostcode=&recordCount=458&pageId=0";

$html = scraperWiki::scrape($pageurl); 
                  
$dom = new simple_html_dom();
$dom->load($html);

$panel = $dom->find('#Panel1 > table h3', 0);

$totals = explode("of", $panel->plaintext);

$pages = $totals[1];

$num = 0;

for ($i = 0; $i <= $pages; $i++) {

$html = scraperWiki::scrape("http://education.staffordshire.gov.uk/Directories/SchoolDirectory/Search.aspx?txtName=&txtArea=&lstSchoolType=All&lstDistricts=All&txtPostcode=&recordCount=458&pageId=". $i); 

$dom = new simple_html_dom();
$dom->load($html);

$records = $dom->find('tr.topicRow');

foreach ($records as $record) {

    $col = $record->find('td');

    $school = Array(
        'name' => "",
        'url' => "",
        'WWW Address' => "",
        'Address (Line 1)' => "",
        'Address (Line 2)' => "",
        'Address (Line 3)' => "",
        'Town' => "",
        'Fax' => "",
        'Telephone' => "",
        'District' => "",
        'E-Mail' => "",
        'DfES Number' => "",
        'lat' => "",
        'lng' => "",
        'District' => "",
        'School Type' => "",
        'Post Code' => "",
    );
    
    $school['name'] = trim($col[1]->plaintext);
    $school['url'] = trim("http://education.staffordshire.gov.uk/Directories/SchoolDirectory/". html_entity_decode($col[1]->find('a', 0)->href));

    $html = scraperWiki::scrape($school['url']); 
    
    $dom = new simple_html_dom();
    $dom->load($html);
    
    $rows = $dom->find('#tblDetails tr');
    
    foreach ($rows as $row) {
        $school[trim($row->find('td', 0)->plaintext)] = trim($row->find('td', 1)->plaintext);
    }
    
    if ($school['WWW Address'] == "Add your Schools Web site by clicking this link!") {
        $school['WWW Address'] = "";
    }
    
    if (empty($school['Address (Line 2)'])) {
        $school['Address (Line 2)'] = "";
    }
    
    if (empty($school['Address (Line 3)'])) {
        $school['Address (Line 3)'] = "";
    }

    if (empty($school['Town'])) {
        $school['Town'] = "";
    }

    if (empty($school['Fax'])) {
        $school['Fax'] = "";
    }
    
    if (empty($school['District'])) {
        $school['District'] = trim($col[2]->plaintext);
    }

    unset($school['E-Mail WWW Address']);

    $school['easting'] = $dom->find('#MapControl1_hidCentreEasting', 0)->value;
    $school['northing'] = $dom->find('#MapControl1_hidCentreNorthing', 0)->value;
    
    $json = json_decode(scraperWiki::scrape("http://www.uk-postcodes.com/eastingnorthing.php?easting=". $school['easting'] ."&northing=". $school['northing']));
    
    $school['lat'] = $json->lat;
    $school['lng'] = $json->lng;
    
    scraperwiki::save_sqlite(array('DfES Number'), $school); 

}

}
?>
