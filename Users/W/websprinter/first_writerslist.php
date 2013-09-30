<?php

require 'scraperwiki/simple_html_dom.php'; $html_content = scraperwiki::scrape("http://www.writersservices.com/listings/uk-literary-agent-listing"); $html = str_get_html($html_content);

$wsUrl = "http://www.writersservices.com";
//$wsTable = find("span.field-content a");

//print $wsTable;

$cnt = 0;
foreach ($html->find("span.field-content a") as $el) {  
$cnt++;
//print $el->href . "\n";

$innercontent = $wsUrl .  $el->href;
$innercontent = "http://www.writersservices.com/reference/campbell-thomson-mclaughlin-ltd";


//$html_content2 = file_get_html($innercontent); //scraperwiki::scrape($innercontent);
//$linkpage= str_get_html($html_content);
$linkpage = file_get_html($innercontent);

//$linkpage="http://www.writersservices.com/reference/brie-burkeman-serafina-clarke-ltd";
//print $linkpage;
//$linkpage="http://www.writersservices.com/reference/b-personal-management-ltd";

//get data from each link
$printout=true;

$linkel=$linkpage->find("div.pane-content", 0); //Company Name
$coname = $linkel->plaintext;

if ($printout){
// print $el . "\n";
// print $coname;
}

$linkel=$linkpage->find("div.field-item", 0); //address
$address = $linkel->plaintext;
if ($printout){

print $coname ."\n" . $address . "\n";
}

//scraperwiki::save_sqlite(array("writers"), array("recordid"=>$cnt, "name"=>$coname, "addr"=>$address));
//scraperwiki::save_sqlite(array("id"),array("id"=>"$id", "recordid"=>$cnt, "name"=>$coname, "addr"=>$address));

$linkel=$linkpage->find("div.pane-content", 4); //description text
$codesc = $linkel->plaintext;
if ($printout){
//print $el . "\n";
print $codesc . "\n";
}

$linkel=$linkpage->find("div.pane-content", 5); // Company telephone
$cotel = $linkel->plaintext;
if ($printout){
//print $el . "\n";
print $cotel . "\n";
}

$linkel=$linkpage->find("div.pane-content", 7); //Company email
$coemail = $linkel->plaintext;

if ($printout){
//print $el . "\n";
print $coemail . "\n";
}

$linkel=$linkpage->find("div.pane-content", 8)->find("div.field-item a",0); //Company site
$cosite = $linkel->href;

if ($printout){
//print $el . "\n";
print $cosite . "*** end of output ***" . "\n";

}

//ok got data now go back for the next link
 
$record[] = array(
    '_dbkey' => mktime(),                    
    'recordid'=>$cnt, 'name'=>$coname, 
    'addr'=>$address, 'codesc'=>$codesc, 
    'cotel'=>$cotel, 'coemail'=>$coemail, 
    'cosite'=>$cosite);
//$message =scraperwiki::save_sqlite(array($unique_keys'_dbkey' => mktime(),array($record),$table_name="dpdata", $verbose=2);
$message =scraperwiki::save_sqlite($unique_keys,$record,$table_name="dpdata", $verbose=2);

print_r($message);
exit;
}
 
?>

<?php

require 'scraperwiki/simple_html_dom.php'; $html_content = scraperwiki::scrape("http://www.writersservices.com/listings/uk-literary-agent-listing"); $html = str_get_html($html_content);

$wsUrl = "http://www.writersservices.com";
//$wsTable = find("span.field-content a");

//print $wsTable;

$cnt = 0;
foreach ($html->find("span.field-content a") as $el) {  
$cnt++;
//print $el->href . "\n";

$innercontent = $wsUrl .  $el->href;
$innercontent = "http://www.writersservices.com/reference/campbell-thomson-mclaughlin-ltd";


//$html_content2 = file_get_html($innercontent); //scraperwiki::scrape($innercontent);
//$linkpage= str_get_html($html_content);
$linkpage = file_get_html($innercontent);

//$linkpage="http://www.writersservices.com/reference/brie-burkeman-serafina-clarke-ltd";
//print $linkpage;
//$linkpage="http://www.writersservices.com/reference/b-personal-management-ltd";

//get data from each link
$printout=true;

$linkel=$linkpage->find("div.pane-content", 0); //Company Name
$coname = $linkel->plaintext;

if ($printout){
// print $el . "\n";
// print $coname;
}

$linkel=$linkpage->find("div.field-item", 0); //address
$address = $linkel->plaintext;
if ($printout){

print $coname ."\n" . $address . "\n";
}

//scraperwiki::save_sqlite(array("writers"), array("recordid"=>$cnt, "name"=>$coname, "addr"=>$address));
//scraperwiki::save_sqlite(array("id"),array("id"=>"$id", "recordid"=>$cnt, "name"=>$coname, "addr"=>$address));

$linkel=$linkpage->find("div.pane-content", 4); //description text
$codesc = $linkel->plaintext;
if ($printout){
//print $el . "\n";
print $codesc . "\n";
}

$linkel=$linkpage->find("div.pane-content", 5); // Company telephone
$cotel = $linkel->plaintext;
if ($printout){
//print $el . "\n";
print $cotel . "\n";
}

$linkel=$linkpage->find("div.pane-content", 7); //Company email
$coemail = $linkel->plaintext;

if ($printout){
//print $el . "\n";
print $coemail . "\n";
}

$linkel=$linkpage->find("div.pane-content", 8)->find("div.field-item a",0); //Company site
$cosite = $linkel->href;

if ($printout){
//print $el . "\n";
print $cosite . "*** end of output ***" . "\n";

}

//ok got data now go back for the next link
 
$record[] = array(
    '_dbkey' => mktime(),                    
    'recordid'=>$cnt, 'name'=>$coname, 
    'addr'=>$address, 'codesc'=>$codesc, 
    'cotel'=>$cotel, 'coemail'=>$coemail, 
    'cosite'=>$cosite);
//$message =scraperwiki::save_sqlite(array($unique_keys'_dbkey' => mktime(),array($record),$table_name="dpdata", $verbose=2);
$message =scraperwiki::save_sqlite($unique_keys,$record,$table_name="dpdata", $verbose=2);

print_r($message);
exit;
}
 
?>

