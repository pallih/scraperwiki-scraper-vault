<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';


//print $html;
$base_url = "http://www.euskara.euskadi.net/r59-15172x/eu/hizt_el/emaitza.asp?";


$pages_to_scrape = array(
"sarrera=c&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=cabanillas&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=cabo+verde&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=caboverdetar&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"azpisar=cabrales+gazta&sarrera=gazta&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=cabredo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=cabrega&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=caceres&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=cadiz&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=cadreita&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=calvados&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=camping&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=campus&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=canberra&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=cancer&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=caniche&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=cante+jondo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=caparroso&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=cappuccino&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"azpisar=cappuccino+kafe&sarrera=cappuccino&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=cappuccino+kafe&sarrera=cappuccino&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=capricornus&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"azpisar=caracalla+babarrun&sarrera=babarrun&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=caracas&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=carborundum&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=carcar&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=carcasona&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=cardan&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"azpisar=cardan+giltzadura&sarrera=cardan&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=cartesianismo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=cartesiar&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=casablanca&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=cascante&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=cashflow&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=cassiopeia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=castejon&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=castello&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=castello+de+la+plana&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=casting&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=castor&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=castrato&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=catch&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=catcher&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=cava&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"azpisar=cavaliere+perspektiba&sarrera=perspektiba&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=cayenne&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=cd++2&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=cdrom&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=centaurus&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=cerdanya&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=ceuta&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=chantilly&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=charleston&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=charter&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=chauvinismo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=chauvinista&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=chef&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=cheviot&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=chicane&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=chicano&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=chihuahua&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=chisinau&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=churrigueresko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=churriguerismo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=cicerone&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=cid&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=cinquecento&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=cintruenigo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=ciudad+real&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=clergyman&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=clown&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=cocker&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=cognac++1&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=coimbra&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=colbertismo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=collage&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=colorado&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=colt&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=columbia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=compact+disc&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=concerto&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=conga&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=continuum&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=copyright&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=cordobilla&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=corella&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=corpus&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"azpisar=delituaren+gorputz+corpus+delicti&sarrera=delitu&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=corrido&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=cortes&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=coru%F1a&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=costa+rica&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=costarricar&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=couche&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"azpisar=couche+paper&sarrera=couche&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=coulomb&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=country&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=courante&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=cowboy&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=crack&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=cracking&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=crawl&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"azpisar=crawl+estiloko+igeriketa&sarrera=igeriketa&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"azpisar=crawl+estiloko+igeriketa&sarrera=igeriketa&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=crescendo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=cricket&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=criterium&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=crochet&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"azpisar=cromagnongo+gizaki&sarrera=gizaki&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=cromlech&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=croquet&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=croupier&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=cuaderna+via&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=cuenca&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=cumbia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=cura%E7ao&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=curie&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=curriculum&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"azpisar=curriculum+vitae&sarrera=curriculum&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=",     
"sarrera=curry&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza="
);


foreach($pages_to_scrape as $page){

    $html = scraperwiki::scrape($base_url.$page);
    $sections_dom = new simple_html_dom();
    $sections_dom->load($html);
    $datah2X='';
     foreach($sections_dom->find('h2 span.azpisarrera') as $datah2)
    {       
        $datah2X=utf8_encode($datah2->plaintext);
        print "h2: ".$datah2X. "\n";

    } 
    if (!isset($datah2X) || $datah2X==''){
     foreach($sections_dom->find('h1 span') as $datah2)
        {   
            $datah2X=utf8_encode($datah2->plaintext);
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
        
        $alldata .= utf8_encode($data->plaintext). $sep;
        $i++;
    }
    print "data: ".$alldata. "\n----------------\n";

           $entry['Term'] = $datah2X;
           $entry['Definition'] = $alldata;
           scraperwiki::save(array('Definition'), $entry);
            
}

?>