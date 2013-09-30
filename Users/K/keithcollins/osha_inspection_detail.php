<?php
require 'scraperwiki/simple_html_dom.php';
//$start_urls[] = "http://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=200626513";

$start_urls[] = "http://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=200626513&id=200452969&id=200375798&id=201925450&id=200264133&id=202317939&id=200515229&id=202567566&id=202600060";
$start_urls[] ="http://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=201262656&id=201562287&id=201942778&id=200083491&id=200053445&id=201039997&id=201169976&id=201184025&id=200263382";
$start_urls[] ="http://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=200212215&id=200624393&id=200612562&id=200356210&id=200924710&id=202341699&id=200012524&id=201371093&id=200823441";
$start_urls[] ="http://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=201042884&id=201923950&id=201992575&id=201182979&id=200924538&id=201182870&id=201488558&id=202358891&id=200690782";
$start_urls[] ="http://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=202340923&id=200012300&id=202004594&id=200513679&id=202344669&id=100510387&id=202352639&id=200773562&id=200540953";
$start_urls[] ="http://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=201362076&id=200451425&id=201124427&id=201503810&id=200150753&id=170002547&id=202004230&id=201406352&id=200642510";
$start_urls[] ="http://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=202340139&id=201181070&id=201953080&id=202340097&id=200120871&id=202329892&id=200740843&id=200551844&id=202003950";
$start_urls[] ="http://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=200621357&id=201094562&id=200672830&id=14222673&id=202003885&id=201404068&id=200120525&id=200840494&id=100101021";
$start_urls[] ="http://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=200021723&id=202289138&id=200850824&id=200850758&id=200850709&id=812735&id=171056500&id=200620235&id=201520350";
$start_urls[] ="http://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=200020956&id=201630217&id=170075139&id=202085346&id=170628671&id=201401148&id=17074857&id=200670529&id=202287678";
$start_urls[] ="http://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=170900310&id=200780088&id=201320074&id=200030112&id=170664213&id=170340020&id=170204820&id=170748321&id=170824031";
$start_urls[] ="http://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=14244024&id=170722532&id=14373922&id=170620314&id=649418&id=14326912&id=14482640&id=170379192&id=880468&id=170566178";
$start_urls[] ="http://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=170084024&id=648824&id=644625&id=14316459&id=886119&id=561522&id=14423081&id=723908&id=170126288&id=604892&id=14419451";
$start_urls[] ="http://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=14321582&id=644252&id=767640&id=170020663&id=14512214&id=170235774&id=170116503&id=170110076&id=170186837&id=170176697";
$start_urls[] ="http://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=14243802&id=14325526&id=170176119&id=14476477&id=170116230&id=170118186&id=14308837&id=819417&id=14317820&id=14328470";
$start_urls[] ="http://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=14225973&id=932293&id=904243&id=14321145&id=14446751&id=849372&id=14466361&id=14497093&id=14278915&id=758540&id=14294276";
$start_urls[] ="http://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=14314538&id=14314546&id=14409924&id=14496657&id=14490437&id=707208&id=14348932&id=704254&id=14199988&id=14320881";
$start_urls[] ="http://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=630178&id=659664&id=14382675&id=14301048&id=14195978&id=14488126&id=14424311&id=14424345&id=14529853&id=570911";
$start_urls[] ="http://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=14540496&id=14307375&id=732990&id=14491179&id=570440&id=14455661&id=14459788&id=14488035&id=14235907&id=14196984";
$start_urls[] ="http://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=14415186&id=14518864";

$inspection_links = array();
foreach ($start_urls as $start_url) {
    $html = scraperWiki::scrape($start_url);
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find("td.blueTen a") as $inspection_link){
        $integ = NULL;
        $integ = strstr($inspection_link, 'establishment.inspection_detail');
        if ($integ) {
            if (!in_array($inspection_link->href, $inspection_links)) {
                $inspection_links[] = $inspection_link->href;
            }
            
        }
    }
}


$i = 0;
$a = 0;
$b = 0;
$takeaway = array();
foreach ($inspection_links as $link) {
    $ins_html = scraperWiki::scrape("http://www.osha.gov/pls/imis/".$link);
    $ins_dom = new simple_html_dom();
    $ins_dom->load($ins_html );
    foreach($ins_dom->find("div tr") as $data){
        $tds = $data->find("td.blueTen");
        foreach ($tds as $t => $td) {
            if ($td->width == "60%") {
                $address = 0;
                $summarynr = 0;
                if ($i<1) {
                    //$takeaway['address'] = $td->plaintext;
                    //scraperwiki::save_sqlite(array("address"),$td->plaintext); 
                    scraperwiki::save_sqlite(array("a"), array("a"=>$td->plaintext));
                    //scraperwiki::save_sqlite(array("a"), array("a"=>1, "aa"=>$td->plaintext));
                    //$address = $td->plaintext;
                }
                $i++;
            }
            if ($td->valign == "middle") {
                if ($a<1) {
                    //$takeaway['summarynr'] = $td->plaintext;
                    //scraperwiki::save_sqlite(array("summarynr"),$td->plaintext); 
                    scraperwiki::save_sqlite(array("a"), array("b"=>$td->plaintext));
                    //scraperwiki::save_sqlite(array("a"), array("a"=>1, "bb"=>$td->plaintext));
                    //$summarynr = $td->plaintext;
                }
                $a++;
            }
            //scraperwiki::save_sqlite(array("a"), array("a"=>0, "address"=>$address, "summarynr"=>$summarynr));

        }
        /*
        if(count($tds)==4){
            $detailrecord1 = array(
                'inspection number'=>$tds[0]->plaintext,
                'establishment name'=>$tds[3]->plaintext
            );
        }
        if (count ($tds)===6){
            $detailrecord2=array(
                'end use'=>$tds[0]->plaintext,
                'project type'=>$tds[1]->plaintext,
                'project cost'=>$tds[2]->plaintext);
        }
        if (count ($tds)===7){
            $detailrecord3=array(
                'accident details link'=>$tds[0]);
        }
        */
    }
    $i = 0;
    $a = 0;
    $b++;
}
//print json_encode($tables) . "\n";

?>
<?php
require 'scraperwiki/simple_html_dom.php';
//$start_urls[] = "http://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=200626513";

$start_urls[] = "http://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=200626513&id=200452969&id=200375798&id=201925450&id=200264133&id=202317939&id=200515229&id=202567566&id=202600060";
$start_urls[] ="http://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=201262656&id=201562287&id=201942778&id=200083491&id=200053445&id=201039997&id=201169976&id=201184025&id=200263382";
$start_urls[] ="http://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=200212215&id=200624393&id=200612562&id=200356210&id=200924710&id=202341699&id=200012524&id=201371093&id=200823441";
$start_urls[] ="http://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=201042884&id=201923950&id=201992575&id=201182979&id=200924538&id=201182870&id=201488558&id=202358891&id=200690782";
$start_urls[] ="http://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=202340923&id=200012300&id=202004594&id=200513679&id=202344669&id=100510387&id=202352639&id=200773562&id=200540953";
$start_urls[] ="http://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=201362076&id=200451425&id=201124427&id=201503810&id=200150753&id=170002547&id=202004230&id=201406352&id=200642510";
$start_urls[] ="http://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=202340139&id=201181070&id=201953080&id=202340097&id=200120871&id=202329892&id=200740843&id=200551844&id=202003950";
$start_urls[] ="http://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=200621357&id=201094562&id=200672830&id=14222673&id=202003885&id=201404068&id=200120525&id=200840494&id=100101021";
$start_urls[] ="http://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=200021723&id=202289138&id=200850824&id=200850758&id=200850709&id=812735&id=171056500&id=200620235&id=201520350";
$start_urls[] ="http://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=200020956&id=201630217&id=170075139&id=202085346&id=170628671&id=201401148&id=17074857&id=200670529&id=202287678";
$start_urls[] ="http://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=170900310&id=200780088&id=201320074&id=200030112&id=170664213&id=170340020&id=170204820&id=170748321&id=170824031";
$start_urls[] ="http://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=14244024&id=170722532&id=14373922&id=170620314&id=649418&id=14326912&id=14482640&id=170379192&id=880468&id=170566178";
$start_urls[] ="http://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=170084024&id=648824&id=644625&id=14316459&id=886119&id=561522&id=14423081&id=723908&id=170126288&id=604892&id=14419451";
$start_urls[] ="http://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=14321582&id=644252&id=767640&id=170020663&id=14512214&id=170235774&id=170116503&id=170110076&id=170186837&id=170176697";
$start_urls[] ="http://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=14243802&id=14325526&id=170176119&id=14476477&id=170116230&id=170118186&id=14308837&id=819417&id=14317820&id=14328470";
$start_urls[] ="http://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=14225973&id=932293&id=904243&id=14321145&id=14446751&id=849372&id=14466361&id=14497093&id=14278915&id=758540&id=14294276";
$start_urls[] ="http://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=14314538&id=14314546&id=14409924&id=14496657&id=14490437&id=707208&id=14348932&id=704254&id=14199988&id=14320881";
$start_urls[] ="http://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=630178&id=659664&id=14382675&id=14301048&id=14195978&id=14488126&id=14424311&id=14424345&id=14529853&id=570911";
$start_urls[] ="http://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=14540496&id=14307375&id=732990&id=14491179&id=570440&id=14455661&id=14459788&id=14488035&id=14235907&id=14196984";
$start_urls[] ="http://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=14415186&id=14518864";

$inspection_links = array();
foreach ($start_urls as $start_url) {
    $html = scraperWiki::scrape($start_url);
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find("td.blueTen a") as $inspection_link){
        $integ = NULL;
        $integ = strstr($inspection_link, 'establishment.inspection_detail');
        if ($integ) {
            if (!in_array($inspection_link->href, $inspection_links)) {
                $inspection_links[] = $inspection_link->href;
            }
            
        }
    }
}


$i = 0;
$a = 0;
$b = 0;
$takeaway = array();
foreach ($inspection_links as $link) {
    $ins_html = scraperWiki::scrape("http://www.osha.gov/pls/imis/".$link);
    $ins_dom = new simple_html_dom();
    $ins_dom->load($ins_html );
    foreach($ins_dom->find("div tr") as $data){
        $tds = $data->find("td.blueTen");
        foreach ($tds as $t => $td) {
            if ($td->width == "60%") {
                $address = 0;
                $summarynr = 0;
                if ($i<1) {
                    //$takeaway['address'] = $td->plaintext;
                    //scraperwiki::save_sqlite(array("address"),$td->plaintext); 
                    scraperwiki::save_sqlite(array("a"), array("a"=>$td->plaintext));
                    //scraperwiki::save_sqlite(array("a"), array("a"=>1, "aa"=>$td->plaintext));
                    //$address = $td->plaintext;
                }
                $i++;
            }
            if ($td->valign == "middle") {
                if ($a<1) {
                    //$takeaway['summarynr'] = $td->plaintext;
                    //scraperwiki::save_sqlite(array("summarynr"),$td->plaintext); 
                    scraperwiki::save_sqlite(array("a"), array("b"=>$td->plaintext));
                    //scraperwiki::save_sqlite(array("a"), array("a"=>1, "bb"=>$td->plaintext));
                    //$summarynr = $td->plaintext;
                }
                $a++;
            }
            //scraperwiki::save_sqlite(array("a"), array("a"=>0, "address"=>$address, "summarynr"=>$summarynr));

        }
        /*
        if(count($tds)==4){
            $detailrecord1 = array(
                'inspection number'=>$tds[0]->plaintext,
                'establishment name'=>$tds[3]->plaintext
            );
        }
        if (count ($tds)===6){
            $detailrecord2=array(
                'end use'=>$tds[0]->plaintext,
                'project type'=>$tds[1]->plaintext,
                'project cost'=>$tds[2]->plaintext);
        }
        if (count ($tds)===7){
            $detailrecord3=array(
                'accident details link'=>$tds[0]);
        }
        */
    }
    $i = 0;
    $a = 0;
    $b++;
}
//print json_encode($tables) . "\n";

?>
