<?php

set_time_limit(0);

require 'scraperwiki/simple_html_dom.php';  

# Blank PHP

// scraperwiki::sqliteexecute("create table reg_info (v_reg_no string, v_owner string, v_type string,v_mfgyr string, v_fuel string,v_color string,v_maker string,v_class string,v_regdate string,v_found string,v_finance string,v_rta string,v_status string,unique(v_reg_no))");           


$startTime = time();
echo "Start Time: ".$startTime."\n";

$crawled = 0;

scraperwiki::attach("registration_numbers", "src");            

$number = scraperwiki::select("* from src.reg_no where reg_no LIKE '%AP09AE7%'"); 

$last = count($number) - 1;
foreach ($number as $i => $row)
{
    $isFirst = ($i == 0);
    $isLast = ($i == $last);
    $v_reg_no = $row['reg_no'] ;
        

$already_crawled = scraperwiki::select("v_found from reg_info where v_reg_no='$v_reg_no'");
if(count($already_crawled)<1)
{
// echo $v_reg_no."\n";
// $v_reg_no = "AP15AZ0333";
$reg_url= "http://210.212.213.82/search/VehicleRegistrationSearch.aspx?__VIEWSTATE=%2FwEPDwUKMTA5NzY2NzY1NWRkaSCbydTZyAN2pWToiXRhAIB06fQ%3D&ctl00%24ContentPlaceHolder1%24txtreg=".$v_reg_no."&ctl00%24ContentPlaceHolder1%24txteng=&ctl00%24ContentPlaceHolder1%24txtchasis=&ctl00%24ContentPlaceHolder1%24txttran=&ctl00%24ContentPlaceHolder1%24Button1=GetData&__EVENTVALIDATION=%2FwEWBwKmqsXRDALKmqGECgKhlYWbCgLkhIPoCAKem4SnDgKA4sljAoPiyWMJB2dMx2HS9oncTDBE8Wsa2ix6Mw%3D%3D";

$html = scraperWiki::scrape($reg_url);           

// print $reg_url."\n";

         
$dom = new simple_html_dom();
$dom->load($html);

$e= $dom->find("span[@id='ctl00_ContentPlaceHolder1_Label1']", 0);
if (!$e)
{
print $v_reg_no."\n";

$e = $dom->find("span[@id='ctl00_ContentPlaceHolder1_lblowner']", 0);
$v_owner = $e->plaintext;
// print $v_owner."\n";

$e = $dom->find("span[@id='ctl00_ContentPlaceHolder1_lblvehclass']", 0);
$v_type = $e->plaintext;
// print $v_type."\n";

$e = $dom->find("span[@id='ctl00_ContentPlaceHolder1_lblmfg']", 0);
$v_mfgyr = $e->plaintext;
// print $v_mfgyr."\n";

$e = $dom->find("span[@id='ctl00_ContentPlaceHolder1_lblfuel']", 0);
$v_fuel = $e->plaintext;
// print $v_fuel."\n";

$e = $dom->find("span[@id='ctl00_ContentPlaceHolder1_lblvehclr']", 0);
$v_color = $e->plaintext;
// print $v_color."\n";

$e = $dom->find("span[@id='ctl00_ContentPlaceHolder1_lblmkrnm']", 0);
$v_maker = $e->plaintext;
print $v_maker."\n";

$e = $dom->find("span[@id='ctl00_ContentPlaceHolder1_lblmkrcls']", 0);
$v_class = $e->plaintext;
// print $v_class."\n";

$e = $dom->find("span[@id='ctl00_ContentPlaceHolder1_lblregdt']", 0);
$v_regdate = $e->plaintext;
// print $v_regdate."\n";

$e = $dom->find("span[@id='ctl00_ContentPlaceHolder1_lblfinnm']", 0);
$v_finance = $e->plaintext;
// print $v_finance."\n";

$e = $dom->find("span[@id='ctl00_ContentPlaceHolder1_lblissauth']", 0);
$v_rta = $e->plaintext;
// print $v_rta."\n";

$e = $dom->find("span[@id='ctl00_ContentPlaceHolder1_lblstatus']", 0);
$v_status = $e->plaintext;
// print $v_status."\n";

// $message = scraperwiki::save_sqlite(array("c"), array("c"=>$reg_no, "v_maker"=>$v_maker, "v_class"=>$v_class));           
// print_r($message);          
// scraperwiki::sqliteexecute("create table reg_info (v_reg_no string, v_owner string, v_type string,v_mfgyr string, v_fuel string,v_color string,v_maker string,v_class string,v_regdate string,v_found string,v_finance string,v_rta string,v_status string,unique(v_reg_no))");           

scraperwiki::sqliteexecute("insert or replace into reg_info values (:v_reg_no,:v_owner,:v_type,:v_mfgyr,:v_fuel,:v_color,:v_maker,:v_class,:v_regdate,:v_found,:v_finance,:v_rta,:v_status)", array("v_reg_no"=>$v_reg_no, "v_owner"=>$v_owner,"v_type"=>$v_type,"v_mfgyr"=>$v_mfgyr,"v_fuel"=>$v_fuel,"v_color"=>$v_color,"v_maker"=>$v_maker,"v_class"=>$v_class,"v_regdate"=>$v_regdate,"v_found"=>"Y","v_finance"=>$v_finance,"v_rta"=>$v_rta,"v_status"=>$v_status));

scraperwiki::sqlitecommit();           

$crawled++;

}
else
{
$found = $e->plaintext;
echo "Vehicle: ".$v_reg_no." ".$found."\n";

scraperwiki::sqliteexecute("insert or replace into reg_info values (:v_reg_no,:v_owner,:v_type,:v_mfgyr,:v_fuel,:v_color,:v_maker,:v_class,:v_regdate,:v_found,:v_finance,:v_rta,:v_status)", array("v_reg_no"=>$v_reg_no, "v_owner"=>"","v_type"=>"","v_mfgyr"=>"","v_fuel"=>"","v_color"=>"","v_maker"=>"","v_class"=>"","v_regdate"=>"","v_found"=>"N","v_finance"=>"","v_rta"=>"","v_status"=>""));

scraperwiki::sqlitecommit();          

}

$dom->__destruct();

}

else {

echo $v_reg_no.": duplicate\n";
$crawled++;
}


}


echo $crawled;

$endTime = time();
echo "Start Time: ".$endTime."\n";

$totalTime = ($endTime-$startTime);

echo "Time taken: ".$totalTime."\n";

?>
