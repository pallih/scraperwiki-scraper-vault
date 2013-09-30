<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';


//print $html;
$base_url = "http://www.euskara.euskadi.net/r59-15172x/eu/hizt_el/emaitza.asp?";


$pages_to_scrape = array(
"azpisar=giltzurrun+gaineko+guruin+guruin+suprarrenal&sarrera=guruin&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gurutz&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gurutzada&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gurutzadura&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gurutzagune&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gurutzaketa&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gurutzaldi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gurutzaldiabiadura+gurutzaldierregimen&sarrera=gurutzaldi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gurutzaldiabiadura+gurutzaldierregimen&sarrera=gurutzaldi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gurutzaldiestropada&sarrera=gurutzaldi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gurutzaldimisil&sarrera=gurutzaldi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gurutzatu++1&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gurutzatu++2&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gurutze++1&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gurutze++2&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gurutze+santuaren+seinalea+egin&sarrera=gurutze++2&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gurutze+santuaren+seinalea+egin&sarrera=gurutze++2&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gurutzearen+seinale&sarrera=gurutze++2&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gurutzearen+seinalea+egin&sarrera=gurutze++2&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gurutzebide&sarrera=gurutze++2&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gurutzedun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gurutzefika&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gurutzefikapen&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gurutzefikatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gurutzefikatzaile&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gurutzeganga&sarrera=ganga++2&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gurutzegrama&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gurutzeontzi&sarrera=gurutze++2&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gurutzepuntu&sarrera=puntu&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gurutzeria&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gurutzeta&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gurutzetaezpata&sarrera=gurutzeta&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gurutzetako&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gurutziltzaile&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gurutziltzaketa&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gurutziltzatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=guruzpide&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=guruztoki&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gustagarri&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gustatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gustavo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gustu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gustudun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gustugabe&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gustugabetasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gustuko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gustura&sarrera=gustu&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gusu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutapertxa&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutar++1&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutar++2&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutaratu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutartean&sarrera=gu&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutarteko&sarrera=gu&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=guti&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutixko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutiz+gehienak&sarrera=guti&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutizia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutiziagarri&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutiziamendu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutiziatsu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutiziatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutiziatzaile&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutizioso&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutizioso&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutun+pastoral&sarrera=pastoral&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutunazal&sarrera=gutun&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutunirekitzeko&sarrera=gutun&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutunliburu&sarrera=gutun&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutunontzi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutxi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutxi+balitz+bezala&sarrera=gutxi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutxi+bat&sarrera=gutxi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutxi+gorabehera&sarrera=gorabehera&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutxiago&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutxiago+izan&sarrera=gutxiago&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutxiagotasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutxiagotu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutxiasko&sarrera=gutxi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutxiegi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutxiegitasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutxien&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutxien+uste+denean+erbia+azaldu&sarrera=erbi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutxien+uste+dugun+lekuan+erbia+lo&sarrera=erbi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutxienean&sarrera=gutxien&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutxieneko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutxieneko+zerbitzu&sarrera=zerbitzu&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutxienekoa+izan&sarrera=gutxieneko&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutxienez&sarrera=gutxien&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutxiengo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutxienik&sarrera=gutxien&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutxiesgarri&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutxiespen&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutxietsi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutxigarri&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutxigatik&sarrera=gutxi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutxik+egin+du++ez+enean%2Fbait%2Ftzea%2Fnola&sarrera=gutxi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutxik+egin+du++ez+enean%2Fbait%2Ftzea%2Fnola&sarrera=gutxi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutxik+egin+du++ez+enean%2Fbait%2Ftzea%2Fnola&sarrera=gutxi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutxik+egin+du++ez+enean%2Fbait%2Ftzea%2Fnola&sarrera=gutxi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutxik+egin+du++ez+enean%2Fbait%2Ftzea%2Fnola&sarrera=gutxi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutxik+egin+du++ez+enean%2Fbait%2Ftzea%2Fnola&sarrera=gutxi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutxika&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutxika%2Fxeheka+saldu&sarrera=saldu&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutxitan&sarrera=gutxi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutxitu++1&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutxitu++2&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutxitxo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutxixeago&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutxiz+gehiena&sarrera=gehien&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=guyana&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=guyana+frantsesa&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=guyana+nederlandarra&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=guyanar&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=guzi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=guzti&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=guztiahaldun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=guztiahalduntasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=guztiahalmen&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=guztiahaltsu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=guztiarekin+ere&sarrera=guzti&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=guztiaz+ere&sarrera=guzti&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=guztira&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=guztitara&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=guztiz&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=guztizko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza="
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

?><?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';


//print $html;
$base_url = "http://www.euskara.euskadi.net/r59-15172x/eu/hizt_el/emaitza.asp?";


$pages_to_scrape = array(
"azpisar=giltzurrun+gaineko+guruin+guruin+suprarrenal&sarrera=guruin&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gurutz&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gurutzada&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gurutzadura&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gurutzagune&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gurutzaketa&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gurutzaldi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gurutzaldiabiadura+gurutzaldierregimen&sarrera=gurutzaldi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gurutzaldiabiadura+gurutzaldierregimen&sarrera=gurutzaldi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gurutzaldiestropada&sarrera=gurutzaldi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gurutzaldimisil&sarrera=gurutzaldi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gurutzatu++1&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gurutzatu++2&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gurutze++1&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gurutze++2&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gurutze+santuaren+seinalea+egin&sarrera=gurutze++2&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gurutze+santuaren+seinalea+egin&sarrera=gurutze++2&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gurutzearen+seinale&sarrera=gurutze++2&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gurutzearen+seinalea+egin&sarrera=gurutze++2&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gurutzebide&sarrera=gurutze++2&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gurutzedun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gurutzefika&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gurutzefikapen&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gurutzefikatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gurutzefikatzaile&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gurutzeganga&sarrera=ganga++2&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gurutzegrama&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gurutzeontzi&sarrera=gurutze++2&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gurutzepuntu&sarrera=puntu&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gurutzeria&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gurutzeta&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gurutzetaezpata&sarrera=gurutzeta&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gurutzetako&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gurutziltzaile&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gurutziltzaketa&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gurutziltzatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=guruzpide&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=guruztoki&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gustagarri&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gustatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gustavo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gustu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gustudun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gustugabe&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gustugabetasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gustuko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gustura&sarrera=gustu&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gusu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutapertxa&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutar++1&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutar++2&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutaratu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutartean&sarrera=gu&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutarteko&sarrera=gu&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=guti&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutixko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutiz+gehienak&sarrera=guti&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutizia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutiziagarri&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutiziamendu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutiziatsu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutiziatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutiziatzaile&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutizioso&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutizioso&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutun+pastoral&sarrera=pastoral&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutunazal&sarrera=gutun&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutunirekitzeko&sarrera=gutun&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutunliburu&sarrera=gutun&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutunontzi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutxi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutxi+balitz+bezala&sarrera=gutxi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutxi+bat&sarrera=gutxi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutxi+gorabehera&sarrera=gorabehera&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutxiago&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutxiago+izan&sarrera=gutxiago&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutxiagotasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutxiagotu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutxiasko&sarrera=gutxi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutxiegi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutxiegitasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutxien&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutxien+uste+denean+erbia+azaldu&sarrera=erbi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutxien+uste+dugun+lekuan+erbia+lo&sarrera=erbi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutxienean&sarrera=gutxien&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutxieneko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutxieneko+zerbitzu&sarrera=zerbitzu&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutxienekoa+izan&sarrera=gutxieneko&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutxienez&sarrera=gutxien&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutxiengo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutxienik&sarrera=gutxien&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutxiesgarri&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutxiespen&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutxietsi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutxigarri&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutxigatik&sarrera=gutxi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutxik+egin+du++ez+enean%2Fbait%2Ftzea%2Fnola&sarrera=gutxi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutxik+egin+du++ez+enean%2Fbait%2Ftzea%2Fnola&sarrera=gutxi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutxik+egin+du++ez+enean%2Fbait%2Ftzea%2Fnola&sarrera=gutxi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutxik+egin+du++ez+enean%2Fbait%2Ftzea%2Fnola&sarrera=gutxi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutxik+egin+du++ez+enean%2Fbait%2Ftzea%2Fnola&sarrera=gutxi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutxik+egin+du++ez+enean%2Fbait%2Ftzea%2Fnola&sarrera=gutxi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutxika&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutxika%2Fxeheka+saldu&sarrera=saldu&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutxitan&sarrera=gutxi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutxitu++1&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutxitu++2&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutxitxo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=gutxixeago&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=gutxiz+gehiena&sarrera=gehien&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=guyana&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=guyana+frantsesa&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=guyana+nederlandarra&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=guyanar&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=guzi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=guzti&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=guztiahaldun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=guztiahalduntasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=guztiahalmen&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=guztiahaltsu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=guztiarekin+ere&sarrera=guzti&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"azpisar=guztiaz+ere&sarrera=guzti&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=guztira&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=guztitara&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=guztiz&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=", 
"sarrera=guztizko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza="
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