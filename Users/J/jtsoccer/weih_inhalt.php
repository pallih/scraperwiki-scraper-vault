<?php
require  'scraperwiki/simple_html_dom.php';


$url=array('http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-auf-gut-altenhof-bei-eckernfoerde.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-bad-bramstedt.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/adventsmarkt-in-bad-oldesloe.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/erzgebirgischer-kunsthandwerker-weihnachtsmarkt-in-bad-schwartau.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-bad-schwartau.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/zwergenwald-weihnachtsmarkt-in-bad-schwartau.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/adventsmarkt-auf-der-schlossinsel-in-barmstedt.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-barmstedt.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-auf-gut-basthorst.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/hobby-und-kreativmarkt-winterzauber-in-bilsen.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-bordesholm.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-dagebuell-ot-suederwaygaard.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-zauberhafte-weihnacht-auf-gut-emkendorf.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/werkstatt-der-engel-am-schloss-eutin.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-flensburg.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-gluecksburg.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-glueckstadt.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/adventmarkt-in-der-kupfermuehle-in-glinde.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-mit-eiswelt-in-heide.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-husum.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-christmas-camping-in-kayhude-bei-hamburg.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-kiel.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/historischer-weihnachtsmarkt-in-luebeck.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/kinder-und-familienweihnachtsmarkt-in-luebeck.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/kunsthandwerkermarkt-in-luebeck.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/kunsthandwerkermarkt-luebsche-wiehnacht-in-luebeck.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/luebecker-weihnachtsmarkt.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/schwul-lesbischer-weihnachtsmarkt-pink-x-mas-in-luebeck.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmaerchenwald-in-luebeck.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-am-heiligen-geist-hospital-in-luebeck.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-bei-niederegger-in-luebeck.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-lauenburg-elbe.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-moelln.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/motorrad-weihnachtsmarkt-in-neumuenster.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-neumuenster.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-neustadt-in-holstein.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/fischers-wiehnacht-in-niendorf.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-norderstedt.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/maritimer-weihnachtsmarkt-im-ostseebad-eckernfoerde.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/silvestermarkt-im-ostseebad-eckernfoerde.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/nikolausmarkt-in-der-drostei-in-pinneberg.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/nikolausmarkt-in-ploen.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/romantischer-weihnachtsmarkt-in-preetz.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-des-eulenrings-in-quickborn.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/ratzeburger-inseladvent.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-rieseby-ot-saxtorf.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-schoenberg-holstein.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/wintermarkt-in-scharbeutz.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-der-stadt-schenefeld.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-schleswig.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-auf-gut-stockseehof-in-stocksee.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-joeoeltir-oen-muasem-in-sylt-ost-ot-morsum.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-toenning.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/musikalischer-weihnachtsmarkt-in-timmendorfer-strand.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-im-landgestuet-traventhal.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/nikolausmarkt-in-trittau.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/adventsmarkt-in-der-museumsscheune-in-uetersen.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-uetersen.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/kleines-weihnachtsfest-in-wilster.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-der-rumflether-muehle-in-wilster.html','http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-altenburg.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/lichterfest-in-apolda.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-arnstadt.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-artern.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-bad-berka.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-bad-berka-ot-tannroda.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-bad-blankenburg.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/lichterfest-in-bad-frankenhausen.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-bad-koestritz.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-bad-langensalza.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-bad-lobenstein.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-bad-salzungen.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-bleicherode.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-mit-krippenausstellung-auf-burg-hanstein-in-bornhagen-rimbach.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-auf-schloss-burgk-an-der-saale.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/historischer-weihnachtsmarkt-auf-der-wartburg-in-eisenach.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-eisenach.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/nachtweihnachtsmarkt-in-eisenberg.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-im-rittergut-endschuetz.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-mit-weihnachtsbindeschau-in-erfurt.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-goessnitz.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/maerchenmarkt-in-gera.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-gotha.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-greiz.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-mit-kunsthandwerk-in-grossbodungen.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-im-heilbad-heiligenstadt.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-auf-schloss-heringen.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/gluehweinmarkt-in-hildburghausen.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/hildburghaeuser-weihnachtsmesse-in-hildburghausen.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-ilmenau.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-jena.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-kranichfeld.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-langenwolschendorf.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/kugelmarkt-in-lauscha.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/maerchenhafte-weihnachten-auf-burg-scharfenstein-in-leinefelde-worbis.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/mittelalterlicher-adventsmarkt-auf-burg-scharfenstein-in-leinefelde-worbis.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/zauber-der-weihnacht-auf-burg-scharfenstein-in-leinefelde-worbis.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/adventsmarkt-an-der-bergbahn-in-lichtenhain.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/nostalgischer-adventsmarkt-in-liebstedt.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/advents-und-kunstmarkt-in-muehlhausen-thueringen.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-meiningen.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-im-kulturbahnhof-meuselwitz.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/hinternaher-weihnachtsmarkt-in-nahetal-waldau.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-neuhaus-am-rennweg.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/adventsmarkt-in-neustadt-an-der-orla.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-ehrenhain.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-nordhausen.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-poessneck.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-im-renaissanceschloss-ponitz.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/pyramidenfest-in-ronneburg-in-thueringen.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-auf-schloss-heidecksburg-in-rudolstadt.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-ruhla.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-soemmerda.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-der-feengrottenstadt-saalfeld.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-schleiz.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-im-kuenstlerhof-in-schleusingen.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-schleusingen.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/herrscheklasmarkt-in-schmalkalden.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/mittelalterlicher-weihnachtsmarkt-auf-dem-schloss-wilhelmsburg-in-schmalkalden.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-sondershausen.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/museums-weihnachtsmarkt-in-sonneberg.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-sonneberg.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/griffel-und-weihnachtsmarkt-in-steinach.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/chrisamelmart-in-suhl.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-tabarz.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/adventszauber-auf-schloss-tonndorf.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/kochberger-nikolausmarkt-in-uhlstaedt-ot-grosskochberg.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/kuenstler-und-kunsthandwerkermarkt-in-voelkershausen-rhoen.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/adventsmarkt-auf-dem-klostergut-volkenroda.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/adventsmarkt-im-deutschen-bienenmuseum-in-weimar.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-weimar.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-wiehe.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-zeulenroda.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-zeulenroda-ot-triebes.html');
$url_c=count($url);

for($k=133;$k<$url_c;$k++){

print $k."\n";

$html = scraperwiki::scrape($url[$k]);



$plz='';

$ort='';
$web='';
$name='';
$str='';
$kurz='';
$bundesland='';


    # Use the PHP Simple HTML DOM Parser to extract <td> tags
    $dom = new simple_html_dom();
    $dom->load($html);

foreach($dom->find('h1') as $name){
         # Store data in the datastore
         $name=$name->innertext;
        //print $name."\n";
         break;
        }

$n = 1;
foreach($dom->find('div.label_val a') as $web){
         

        if($n==5){
           # Store data in the datastore
          $web=$web->href;
         //print $web."\n";
          break;
        }
//print $web."\n";
        $n++;  
         }


$n = 1;
foreach($dom->find('div.label_val') as $div){
        if($n==1){
            $datum = $div->innertext;
        }if($n==2){
            $stra = $div->innertext;
        }if($n==6){
            $uhr = $div->plaintext;
        }

        $n++;         
}


$datum= str_replace('<br>','',$datum);
$datum= str_replace('<br />','',$datum);

$stra = explode('<br />',$stra);
$str = $stra[0];

$stra1 = explode(' ',$stra[1]);
$stra1_c = count($stra1);

$plz = $stra1[0];

if($stra1_c == 2){
    $ort = $stra1[1];
}else{
    for($x = 1; $x < $stra1_c; $x++){
         $ort = $ort." ".$stra1[$x];
    }
}

$kurz = $datum." ".$uhr;




foreach($dom->find('div#subnav a') as $bund){
        $bundesland= $bund->innertext;    
}

//print $bundesland."\n";







//PLACE DE STRING
$str=html_entity_decode($str);
$ort=html_entity_decode($ort);
$name=html_entity_decode($name);
$kurz=html_entity_decode($kurz);
$bundesland=html_entity_decode($bundesland);

$str=utf8_encode($str);
$ort=utf8_encode($ort);
$name=utf8_encode($name);
$kurz=utf8_encode($kurz);
$bundesland=utf8_encode($bundesland);

$name=str_replace('"','',$name);


$plz=trim($plz);
$ort=trim($ort);
$web=trim($web);
$name=trim($name);
$str=trim($str);
$bundesland=trim($bundesland);
$kurz=trim($kurz);





scraperwiki::save(array('name','str','plz','ort','web','kurz','bundesland'), array('name' => $name ,'str' => $str, 'plz' => $plz, 'ort' => $ort, 'web' => $web , 'kurz' => $kurz ,'bundesland' => $bundesland));


}

?>
<?php
require  'scraperwiki/simple_html_dom.php';


$url=array('http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-auf-gut-altenhof-bei-eckernfoerde.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-bad-bramstedt.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/adventsmarkt-in-bad-oldesloe.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/erzgebirgischer-kunsthandwerker-weihnachtsmarkt-in-bad-schwartau.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-bad-schwartau.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/zwergenwald-weihnachtsmarkt-in-bad-schwartau.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/adventsmarkt-auf-der-schlossinsel-in-barmstedt.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-barmstedt.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-auf-gut-basthorst.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/hobby-und-kreativmarkt-winterzauber-in-bilsen.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-bordesholm.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-dagebuell-ot-suederwaygaard.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-zauberhafte-weihnacht-auf-gut-emkendorf.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/werkstatt-der-engel-am-schloss-eutin.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-flensburg.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-gluecksburg.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-glueckstadt.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/adventmarkt-in-der-kupfermuehle-in-glinde.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-mit-eiswelt-in-heide.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-husum.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-christmas-camping-in-kayhude-bei-hamburg.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-kiel.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/historischer-weihnachtsmarkt-in-luebeck.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/kinder-und-familienweihnachtsmarkt-in-luebeck.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/kunsthandwerkermarkt-in-luebeck.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/kunsthandwerkermarkt-luebsche-wiehnacht-in-luebeck.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/luebecker-weihnachtsmarkt.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/schwul-lesbischer-weihnachtsmarkt-pink-x-mas-in-luebeck.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmaerchenwald-in-luebeck.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-am-heiligen-geist-hospital-in-luebeck.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-bei-niederegger-in-luebeck.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-lauenburg-elbe.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-moelln.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/motorrad-weihnachtsmarkt-in-neumuenster.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-neumuenster.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-neustadt-in-holstein.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/fischers-wiehnacht-in-niendorf.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-norderstedt.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/maritimer-weihnachtsmarkt-im-ostseebad-eckernfoerde.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/silvestermarkt-im-ostseebad-eckernfoerde.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/nikolausmarkt-in-der-drostei-in-pinneberg.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/nikolausmarkt-in-ploen.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/romantischer-weihnachtsmarkt-in-preetz.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-des-eulenrings-in-quickborn.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/ratzeburger-inseladvent.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-rieseby-ot-saxtorf.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-schoenberg-holstein.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/wintermarkt-in-scharbeutz.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-der-stadt-schenefeld.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-schleswig.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-auf-gut-stockseehof-in-stocksee.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-joeoeltir-oen-muasem-in-sylt-ost-ot-morsum.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-toenning.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/musikalischer-weihnachtsmarkt-in-timmendorfer-strand.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-im-landgestuet-traventhal.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/nikolausmarkt-in-trittau.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/adventsmarkt-in-der-museumsscheune-in-uetersen.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-uetersen.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/kleines-weihnachtsfest-in-wilster.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-der-rumflether-muehle-in-wilster.html','http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-altenburg.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/lichterfest-in-apolda.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-arnstadt.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-artern.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-bad-berka.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-bad-berka-ot-tannroda.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-bad-blankenburg.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/lichterfest-in-bad-frankenhausen.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-bad-koestritz.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-bad-langensalza.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-bad-lobenstein.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-bad-salzungen.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-bleicherode.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-mit-krippenausstellung-auf-burg-hanstein-in-bornhagen-rimbach.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-auf-schloss-burgk-an-der-saale.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/historischer-weihnachtsmarkt-auf-der-wartburg-in-eisenach.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-eisenach.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/nachtweihnachtsmarkt-in-eisenberg.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-im-rittergut-endschuetz.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-mit-weihnachtsbindeschau-in-erfurt.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-goessnitz.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/maerchenmarkt-in-gera.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-gotha.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-greiz.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-mit-kunsthandwerk-in-grossbodungen.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-im-heilbad-heiligenstadt.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-auf-schloss-heringen.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/gluehweinmarkt-in-hildburghausen.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/hildburghaeuser-weihnachtsmesse-in-hildburghausen.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-ilmenau.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-jena.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-kranichfeld.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-langenwolschendorf.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/kugelmarkt-in-lauscha.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/maerchenhafte-weihnachten-auf-burg-scharfenstein-in-leinefelde-worbis.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/mittelalterlicher-adventsmarkt-auf-burg-scharfenstein-in-leinefelde-worbis.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/zauber-der-weihnacht-auf-burg-scharfenstein-in-leinefelde-worbis.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/adventsmarkt-an-der-bergbahn-in-lichtenhain.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/nostalgischer-adventsmarkt-in-liebstedt.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/advents-und-kunstmarkt-in-muehlhausen-thueringen.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-meiningen.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-im-kulturbahnhof-meuselwitz.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/hinternaher-weihnachtsmarkt-in-nahetal-waldau.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-neuhaus-am-rennweg.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/adventsmarkt-in-neustadt-an-der-orla.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-ehrenhain.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-nordhausen.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-poessneck.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-im-renaissanceschloss-ponitz.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/pyramidenfest-in-ronneburg-in-thueringen.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-auf-schloss-heidecksburg-in-rudolstadt.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-ruhla.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-soemmerda.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-der-feengrottenstadt-saalfeld.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-schleiz.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-im-kuenstlerhof-in-schleusingen.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-schleusingen.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/herrscheklasmarkt-in-schmalkalden.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/mittelalterlicher-weihnachtsmarkt-auf-dem-schloss-wilhelmsburg-in-schmalkalden.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-sondershausen.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/museums-weihnachtsmarkt-in-sonneberg.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-sonneberg.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/griffel-und-weihnachtsmarkt-in-steinach.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/chrisamelmart-in-suhl.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-tabarz.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/adventszauber-auf-schloss-tonndorf.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/kochberger-nikolausmarkt-in-uhlstaedt-ot-grosskochberg.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/kuenstler-und-kunsthandwerkermarkt-in-voelkershausen-rhoen.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/adventsmarkt-auf-dem-klostergut-volkenroda.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/adventsmarkt-im-deutschen-bienenmuseum-in-weimar.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-weimar.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-wiehe.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-zeulenroda.html', 'http://www.weihnachtsmaerkte-in-deutschland.de/weihnachtsmarkt-in-zeulenroda-ot-triebes.html');
$url_c=count($url);

for($k=133;$k<$url_c;$k++){

print $k."\n";

$html = scraperwiki::scrape($url[$k]);



$plz='';

$ort='';
$web='';
$name='';
$str='';
$kurz='';
$bundesland='';


    # Use the PHP Simple HTML DOM Parser to extract <td> tags
    $dom = new simple_html_dom();
    $dom->load($html);

foreach($dom->find('h1') as $name){
         # Store data in the datastore
         $name=$name->innertext;
        //print $name."\n";
         break;
        }

$n = 1;
foreach($dom->find('div.label_val a') as $web){
         

        if($n==5){
           # Store data in the datastore
          $web=$web->href;
         //print $web."\n";
          break;
        }
//print $web."\n";
        $n++;  
         }


$n = 1;
foreach($dom->find('div.label_val') as $div){
        if($n==1){
            $datum = $div->innertext;
        }if($n==2){
            $stra = $div->innertext;
        }if($n==6){
            $uhr = $div->plaintext;
        }

        $n++;         
}


$datum= str_replace('<br>','',$datum);
$datum= str_replace('<br />','',$datum);

$stra = explode('<br />',$stra);
$str = $stra[0];

$stra1 = explode(' ',$stra[1]);
$stra1_c = count($stra1);

$plz = $stra1[0];

if($stra1_c == 2){
    $ort = $stra1[1];
}else{
    for($x = 1; $x < $stra1_c; $x++){
         $ort = $ort." ".$stra1[$x];
    }
}

$kurz = $datum." ".$uhr;




foreach($dom->find('div#subnav a') as $bund){
        $bundesland= $bund->innertext;    
}

//print $bundesland."\n";







//PLACE DE STRING
$str=html_entity_decode($str);
$ort=html_entity_decode($ort);
$name=html_entity_decode($name);
$kurz=html_entity_decode($kurz);
$bundesland=html_entity_decode($bundesland);

$str=utf8_encode($str);
$ort=utf8_encode($ort);
$name=utf8_encode($name);
$kurz=utf8_encode($kurz);
$bundesland=utf8_encode($bundesland);

$name=str_replace('"','',$name);


$plz=trim($plz);
$ort=trim($ort);
$web=trim($web);
$name=trim($name);
$str=trim($str);
$bundesland=trim($bundesland);
$kurz=trim($kurz);





scraperwiki::save(array('name','str','plz','ort','web','kurz','bundesland'), array('name' => $name ,'str' => $str, 'plz' => $plz, 'ort' => $ort, 'web' => $web , 'kurz' => $kurz ,'bundesland' => $bundesland));


}

?>
