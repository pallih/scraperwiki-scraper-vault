<?php
$html = scraperWiki::scrape("http://wcedemis.pgwc.gov.za/wced/findschoolO.shtml?2");      
require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
//scraperwiki::sqliteexecute("CREATE TABLE `swdata` (`EMISNumber` text)");
//scraperWiki::save_var('place','none');
//scraperWiki::save_var('place','0130333352');
//exit();
$place=scraperWiki::get_var('place', 'none');
$resume=true;
if ($place=='none') $resume=false;
foreach($dom->find("select[name='EMIS_NO'] option") as $data){ //loop through the list of ordinary schools
    $d=http_build_query(array('EMIS_NO'=>$data->value));
    $dlength=strlen($d);
    if ($resume) { //we need to resume, so find the correct place
        if ($place==$data->value) $resume=false;
        else continue;
    }
    scraperWiki::save_var('place',$data->value);
    //get the school's page
    $html2 = file_get_contents('http://wcedemis.pgwc.gov.za/ibi_apps/WFServlet?IBIF_ex=INERSCHOOLN', false, stream_context_create (array ('http'=>array ('method'=>'POST','header'=>"Connection: close\r\nContent-Length: $dlength\r\n", 'content'=>$d)))) ;
    $dom2 = new simple_html_dom();
    $dom2->load($html2);
    $tosave=array();
    $script = $dom2->find("script");
    $sa=explode(';',str_replace('</script>','',str_replace('<script>  function mapIt() {','',$script[0])));
    foreach ($sa as $a) {
        $d=explode('=',$a);
        if (strpos($d[0],'var longx')!==false) $long=str_replace(' ','',str_replace('\'','',$d[1]));
        if (strpos($d[0],'var latx')!==false) $lat=str_replace(' ','',str_replace('\'','',$d[1]));
    }
    $tosave['lat']=$lat;
    $tosave['long']=$long;
    $tosave['PrimarySource']=str_replace('PRIMARY SOURCE: ','',$dom2->find("table",1)->find("tr",1)->plaintext);
    foreach($dom2->find("table",0)->find("tr") as $tr){
        $tds = $tr->find("td");
        if (count($tds)==2) {
            $add=$tds[1]->plaintext;
            $add=str_replace('  ','',$add); //remove double spaces  
            if ($add=='&nbsp;') $add=''; //format blanks correctly
            //$add=str_replace('ë','\u00CB',$add); //fix UTF error with one school
            //$add=str_replace('Ü','\u00DC',$add); //fix UTF error
            $add=utf8_encode($add);
            $key=$tds[0]->plaintext;
            $key=str_replace(' ','',$key);//remove spaces from key
            $tosave[$key]=$add;
        }
    }
    //print_r($tosave);
    //print $data->value;
    try {
        scraperwiki::save(array('EMISNumber'), $tosave);
    }
    catch (Exception $e) {
        print 'Caught exception ('.$data->value.'): '.$e->getMessage()."\n";
    }
    
    //break; //uncomment to just process one school

}
scraperWiki::save_var('place','none');
?><?php
$html = scraperWiki::scrape("http://wcedemis.pgwc.gov.za/wced/findschoolO.shtml?2");      
require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
//scraperwiki::sqliteexecute("CREATE TABLE `swdata` (`EMISNumber` text)");
//scraperWiki::save_var('place','none');
//scraperWiki::save_var('place','0130333352');
//exit();
$place=scraperWiki::get_var('place', 'none');
$resume=true;
if ($place=='none') $resume=false;
foreach($dom->find("select[name='EMIS_NO'] option") as $data){ //loop through the list of ordinary schools
    $d=http_build_query(array('EMIS_NO'=>$data->value));
    $dlength=strlen($d);
    if ($resume) { //we need to resume, so find the correct place
        if ($place==$data->value) $resume=false;
        else continue;
    }
    scraperWiki::save_var('place',$data->value);
    //get the school's page
    $html2 = file_get_contents('http://wcedemis.pgwc.gov.za/ibi_apps/WFServlet?IBIF_ex=INERSCHOOLN', false, stream_context_create (array ('http'=>array ('method'=>'POST','header'=>"Connection: close\r\nContent-Length: $dlength\r\n", 'content'=>$d)))) ;
    $dom2 = new simple_html_dom();
    $dom2->load($html2);
    $tosave=array();
    $script = $dom2->find("script");
    $sa=explode(';',str_replace('</script>','',str_replace('<script>  function mapIt() {','',$script[0])));
    foreach ($sa as $a) {
        $d=explode('=',$a);
        if (strpos($d[0],'var longx')!==false) $long=str_replace(' ','',str_replace('\'','',$d[1]));
        if (strpos($d[0],'var latx')!==false) $lat=str_replace(' ','',str_replace('\'','',$d[1]));
    }
    $tosave['lat']=$lat;
    $tosave['long']=$long;
    $tosave['PrimarySource']=str_replace('PRIMARY SOURCE: ','',$dom2->find("table",1)->find("tr",1)->plaintext);
    foreach($dom2->find("table",0)->find("tr") as $tr){
        $tds = $tr->find("td");
        if (count($tds)==2) {
            $add=$tds[1]->plaintext;
            $add=str_replace('  ','',$add); //remove double spaces  
            if ($add=='&nbsp;') $add=''; //format blanks correctly
            //$add=str_replace('ë','\u00CB',$add); //fix UTF error with one school
            //$add=str_replace('Ü','\u00DC',$add); //fix UTF error
            $add=utf8_encode($add);
            $key=$tds[0]->plaintext;
            $key=str_replace(' ','',$key);//remove spaces from key
            $tosave[$key]=$add;
        }
    }
    //print_r($tosave);
    //print $data->value;
    try {
        scraperwiki::save(array('EMISNumber'), $tosave);
    }
    catch (Exception $e) {
        print 'Caught exception ('.$data->value.'): '.$e->getMessage()."\n";
    }
    
    //break; //uncomment to just process one school

}
scraperWiki::save_var('place','none');
?>