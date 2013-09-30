<?php
require  'scraperwiki/simple_html_dom.php';
# Welcome to the second ScraperWiki PHP tutorial

# stahni vsechny prijemce dotaci z MFCR CEDR v roce 2010 s pravni formou Obcanske sdruzeni
$html = scraperwiki::scrape("http://www.isvav.cz/findProjectByFilter.do?typVyhledavani=advanced&prjIntCode=&prjIntName=&druhSoutezeKod=&kodSouteze=&providerCode=&celkoveNakladyMin=&celkoveNakladyMax=&celkoveNakladyStatniMin=&celkoveNakladyStatniMax=&categoryCode=3&activityCode=&branchCode=&typOboru=1&keyword=&currentYear=2011&stavPosledniFazeKod=&stavFazeKod=&stavovyFiltrRok=2011&yearStartFrom=&yearStartTo=&yearEndFrom=&yearEndTo=&pocetPrijemcuMin=&pocetPrijemcuMax=&pocetSpoluprijemcuMin=&pocetSpoluprijemcuMax=&pocetVysledkuMin=&pocetVysledkuMax=&evalCode=&rolePrijemce=2&orgName=&orgICO=&kodSubjektu=&nazevOrgJednotky=&kodOrgJednotky=&prijmeniPrijemce=&jmenoPrijemce=&vyzOrgRok=2011&vyzOrg=0&roleResitele=3&personSurname=&personName=&sortType=0&formType=1");
#print $html;

# transcode
$html = iconv("UTF-8", "ISO-8859-1", $html);

# Next we use the PHP Simple HTML DOM Parser to extract the values from the HTML 
# source. Uncomment the next six lines (i.e. delete the # at the start of the lines)
# and run the scraper again. There should be output in the console.

$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find('tr') as $tr)
{
   $tds = $tr->find('td');
   $t0 = $tds[0]->plaintext;
   $t1 = $tds[1]->plaintext;

   $as = $tds[1]->find('a');
   $a0 = $as[0]->plaintext;
   $h0 = $as[0]->href;

   $spans = $tds[1]->find('span');
 
   $s0 = $spans[0]->plaintext;
   $s1 = $spans[1]->plaintext;
   $s2 = $spans[2]->plaintext;
   $s3 = $spans[3]->plaintext;
   $s4 = $spans[4]->plaintext;
   $s5 = $spans[5]->plaintext;
   $s6 = $spans[6]->plaintext;

   # print "a0=[$a0] h0=[$h0] s0=[$s0] s1=[$s1] s2=[$s2] s3=[$s3] s4=[$s4] s5=[$s5] s6=[$s6]";
   print "id [$a0] nazev [$s0] poskytovatel [$s2] prijemce [$s4] obdobi [$s6]\n"; 

   # save data to the datastore
   scraperwiki::save(array('id'), array('id' => $a0, 'nazev' => $s0, 'poskytovatel' => $s2, 'prijemce' => $s4, 'obdobi' => $s6));
}

# Check the 'Data' tab - here you'll see the data saved in the ScraperWiki store.
?><?php
require  'scraperwiki/simple_html_dom.php';
# Welcome to the second ScraperWiki PHP tutorial

# stahni vsechny prijemce dotaci z MFCR CEDR v roce 2010 s pravni formou Obcanske sdruzeni
$html = scraperwiki::scrape("http://www.isvav.cz/findProjectByFilter.do?typVyhledavani=advanced&prjIntCode=&prjIntName=&druhSoutezeKod=&kodSouteze=&providerCode=&celkoveNakladyMin=&celkoveNakladyMax=&celkoveNakladyStatniMin=&celkoveNakladyStatniMax=&categoryCode=3&activityCode=&branchCode=&typOboru=1&keyword=&currentYear=2011&stavPosledniFazeKod=&stavFazeKod=&stavovyFiltrRok=2011&yearStartFrom=&yearStartTo=&yearEndFrom=&yearEndTo=&pocetPrijemcuMin=&pocetPrijemcuMax=&pocetSpoluprijemcuMin=&pocetSpoluprijemcuMax=&pocetVysledkuMin=&pocetVysledkuMax=&evalCode=&rolePrijemce=2&orgName=&orgICO=&kodSubjektu=&nazevOrgJednotky=&kodOrgJednotky=&prijmeniPrijemce=&jmenoPrijemce=&vyzOrgRok=2011&vyzOrg=0&roleResitele=3&personSurname=&personName=&sortType=0&formType=1");
#print $html;

# transcode
$html = iconv("UTF-8", "ISO-8859-1", $html);

# Next we use the PHP Simple HTML DOM Parser to extract the values from the HTML 
# source. Uncomment the next six lines (i.e. delete the # at the start of the lines)
# and run the scraper again. There should be output in the console.

$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find('tr') as $tr)
{
   $tds = $tr->find('td');
   $t0 = $tds[0]->plaintext;
   $t1 = $tds[1]->plaintext;

   $as = $tds[1]->find('a');
   $a0 = $as[0]->plaintext;
   $h0 = $as[0]->href;

   $spans = $tds[1]->find('span');
 
   $s0 = $spans[0]->plaintext;
   $s1 = $spans[1]->plaintext;
   $s2 = $spans[2]->plaintext;
   $s3 = $spans[3]->plaintext;
   $s4 = $spans[4]->plaintext;
   $s5 = $spans[5]->plaintext;
   $s6 = $spans[6]->plaintext;

   # print "a0=[$a0] h0=[$h0] s0=[$s0] s1=[$s1] s2=[$s2] s3=[$s3] s4=[$s4] s5=[$s5] s6=[$s6]";
   print "id [$a0] nazev [$s0] poskytovatel [$s2] prijemce [$s4] obdobi [$s6]\n"; 

   # save data to the datastore
   scraperwiki::save(array('id'), array('id' => $a0, 'nazev' => $s0, 'poskytovatel' => $s2, 'prijemce' => $s4, 'obdobi' => $s6));
}

# Check the 'Data' tab - here you'll see the data saved in the ScraperWiki store.
?>