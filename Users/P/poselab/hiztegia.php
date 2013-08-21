<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';


//print $html;
$base_url = "http://www.euskara.euskadi.net/r59-15172x/eu/hizt_el/emaitza.asp?";


$pages_to_scrape = array(
    "sarrera=etxe&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",
    "mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=&azpisar=herriko+etxe&sarrera=etxe"
);


foreach($pages_to_scrape as $page){

    $html = scraperwiki::scrape($base_url.$page);
    $sections_dom = new simple_html_dom();
    $sections_dom->load($html);

     foreach($sections_dom->find('h2 span.azpisarrera') as $datah2)
    {       
        $datah2X=$datah2->plaintext;
        print "h2: ".$datah2X. "\n";

    } 
    if (!isset($datah2X)){
     foreach($sections_dom->find('h1 span') as $datah2)
        {   
            $datah2X=$datah2->plaintext;
            print "h1: ".$datah2X. "\n";

        } 
    } 
    
    $alldata='';
    $i=0;
    $arraydom = $sections_dom->find('dt.ordaina strong');

    foreach($arraydom  as $data){
        $sep="|";
        if($i == count($arraydom )-1){
            $sep="";
        }
        
        $alldata .= $data->plaintext. $sep;
        $i++;
    }
    print "data: ".$alldata. "\n----------------\n";
           $entry['Term'] = $datah2X;
           $entry['Definition'] = $alldata;
           scraperwiki::save(array('Definition'), $entry);
            
}

?>