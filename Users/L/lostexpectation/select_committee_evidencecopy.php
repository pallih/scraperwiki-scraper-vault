<?php
######################################
# Basic PHP scraper
######################################
require  'scraperwiki/simple_html_dom.php';

$committee_url = "http://www.publications.parliament.uk/pa/cm201011/cmselect/cmeduc/writev/744/contents.htm";
$yahoo_app_id = "fa05gqzV34Ek0FpP8c7JDF08DS0TEum2HRixVDcUE4yjHE0LjqwrOWHFxXMVj4JqKg--";

$html = scraperwiki::scrape($committee_url);
#Assuming all committee pages start with 'contents.htm'
$committee_url_root = str_replace('contents.htm','',$committee_url);

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);

$table = $dom->find("table",1);

$data_committee = strip_tags($table->find("font",0)->plaintext);
$data_enquiry = str_replace("CONTENTS: ","",trim(strip_tags($table->find("p[align='center']",0)->plaintext)));
$data_session = trim(str_replace("Session"," ",$dom->find("table",0)->find("td[width='60%']",0)->find("b",0)->plaintext));


$submission_dom = new simple_html_dom(); #Not sure where I should create this to be efficient...

foreach($table->find('p a') as $data)
{
    if(stristr($data->href,'htm')) {
        $data_respondent = $data->plaintext;

        $submission_url = $committee_url_root.$data->href;
        $submission = scraperwiki::scrape($submission_url); 
        
        $submission_dom = new simple_html_dom(); #Not sure where I should create this to be efficient...
        $submission_dom->load($submission);
        $submission_text = (string)$submission_dom->find("table",0);
              

        
$tags = json_decode(scraperwiki::scrape("http://search.yahooapis.com/ContentAnalysisService/V1/termExtraction?appid={$yahoo_app_id}&output=json&context=".urlencode(substr($submission_text,1,5000))));
    
        $tag_string = join("|",$tags->ResultSet->Result);
       
        $submission_id = $data->href;

        $entry = array('type'=>'submission','submission_id'=>$submission_id, 'committee' => $data_committee,'session'=>$data_session, 'enquiry' => $data_enquiry,'respondent' => $data_respondent,'submission_url'=>$submission_url,'tags'=>$tag_string);
    
    

    # Store data in the datastore
    print $data->plaintext . "\n";
    scraperwiki::save(array('submission_id'), $entry);


    }

}

?><?php
######################################
# Basic PHP scraper
######################################
require  'scraperwiki/simple_html_dom.php';

$committee_url = "http://www.publications.parliament.uk/pa/cm201011/cmselect/cmeduc/writev/744/contents.htm";
$yahoo_app_id = "fa05gqzV34Ek0FpP8c7JDF08DS0TEum2HRixVDcUE4yjHE0LjqwrOWHFxXMVj4JqKg--";

$html = scraperwiki::scrape($committee_url);
#Assuming all committee pages start with 'contents.htm'
$committee_url_root = str_replace('contents.htm','',$committee_url);

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);

$table = $dom->find("table",1);

$data_committee = strip_tags($table->find("font",0)->plaintext);
$data_enquiry = str_replace("CONTENTS: ","",trim(strip_tags($table->find("p[align='center']",0)->plaintext)));
$data_session = trim(str_replace("Session"," ",$dom->find("table",0)->find("td[width='60%']",0)->find("b",0)->plaintext));


$submission_dom = new simple_html_dom(); #Not sure where I should create this to be efficient...

foreach($table->find('p a') as $data)
{
    if(stristr($data->href,'htm')) {
        $data_respondent = $data->plaintext;

        $submission_url = $committee_url_root.$data->href;
        $submission = scraperwiki::scrape($submission_url); 
        
        $submission_dom = new simple_html_dom(); #Not sure where I should create this to be efficient...
        $submission_dom->load($submission);
        $submission_text = (string)$submission_dom->find("table",0);
              

        
$tags = json_decode(scraperwiki::scrape("http://search.yahooapis.com/ContentAnalysisService/V1/termExtraction?appid={$yahoo_app_id}&output=json&context=".urlencode(substr($submission_text,1,5000))));
    
        $tag_string = join("|",$tags->ResultSet->Result);
       
        $submission_id = $data->href;

        $entry = array('type'=>'submission','submission_id'=>$submission_id, 'committee' => $data_committee,'session'=>$data_session, 'enquiry' => $data_enquiry,'respondent' => $data_respondent,'submission_url'=>$submission_url,'tags'=>$tag_string);
    
    

    # Store data in the datastore
    print $data->plaintext . "\n";
    scraperwiki::save(array('submission_id'), $entry);


    }

}

?><?php
######################################
# Basic PHP scraper
######################################
require  'scraperwiki/simple_html_dom.php';

$committee_url = "http://www.publications.parliament.uk/pa/cm201011/cmselect/cmeduc/writev/744/contents.htm";
$yahoo_app_id = "fa05gqzV34Ek0FpP8c7JDF08DS0TEum2HRixVDcUE4yjHE0LjqwrOWHFxXMVj4JqKg--";

$html = scraperwiki::scrape($committee_url);
#Assuming all committee pages start with 'contents.htm'
$committee_url_root = str_replace('contents.htm','',$committee_url);

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);

$table = $dom->find("table",1);

$data_committee = strip_tags($table->find("font",0)->plaintext);
$data_enquiry = str_replace("CONTENTS: ","",trim(strip_tags($table->find("p[align='center']",0)->plaintext)));
$data_session = trim(str_replace("Session"," ",$dom->find("table",0)->find("td[width='60%']",0)->find("b",0)->plaintext));


$submission_dom = new simple_html_dom(); #Not sure where I should create this to be efficient...

foreach($table->find('p a') as $data)
{
    if(stristr($data->href,'htm')) {
        $data_respondent = $data->plaintext;

        $submission_url = $committee_url_root.$data->href;
        $submission = scraperwiki::scrape($submission_url); 
        
        $submission_dom = new simple_html_dom(); #Not sure where I should create this to be efficient...
        $submission_dom->load($submission);
        $submission_text = (string)$submission_dom->find("table",0);
              

        
$tags = json_decode(scraperwiki::scrape("http://search.yahooapis.com/ContentAnalysisService/V1/termExtraction?appid={$yahoo_app_id}&output=json&context=".urlencode(substr($submission_text,1,5000))));
    
        $tag_string = join("|",$tags->ResultSet->Result);
       
        $submission_id = $data->href;

        $entry = array('type'=>'submission','submission_id'=>$submission_id, 'committee' => $data_committee,'session'=>$data_session, 'enquiry' => $data_enquiry,'respondent' => $data_respondent,'submission_url'=>$submission_url,'tags'=>$tag_string);
    
    

    # Store data in the datastore
    print $data->plaintext . "\n";
    scraperwiki::save(array('submission_id'), $entry);


    }

}

?>