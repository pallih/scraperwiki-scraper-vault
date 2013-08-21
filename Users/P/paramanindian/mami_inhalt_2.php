<?php
require  'scraperwiki/simple_html_dom.php';

$url=array('http://www.mamilade.de/magdeburg/melange/restaurant/cafe/biergarten/2024620-magdeburg_melange.html', 'http://www.mamilade.de/weilrod/pfannkuchenhaus/2024620-weilrod_pfannkuchenhaus.html', 'http://www.mamilade.de/salue/saarlouis/familie/2024620-saarlouis_salue.html', 'http://www.mamilade.de/osteria/seaside/sylt/familie/2024620-sylt_osteria.html', 'http://www.mamilade.de/moosstube/neumarkt/familie/essen/2024620-neumarkt_moosstube.html', 'http://www.mamilade.de/dorfkrug/oekohof/kuhhorst/2024620-dorfkrug_kuhhorst.html', 'http://www.mamilade.de/fonte/hamburg/essen/familie/2024620-la_fonte.html', 'http://www.mamilade.de/havelberg/gueldene/pfanne/familienessen/2024620-havelberg_gueldenepfanne.html', 'http://www.mamilade.de/zaehringer/burg/freiburg/2024620-freiburg_zaehringer_burg.html', 'http://www.mamilade.de/lenzer/krug/2024620-lenzer_krug.html', 'http://www.mamilade.de/lonetal/breitingen/2024620-breitingen_lonetal.html', 'http://www.mamilade.de/cafe/milchbart/magdeburg/2024620-magdeburg_cafe_milchbart.html', 'http://www.mamilade.de/sonnenhof/stuttgart/familie/2024620-stuttgart_sonnenhof_cafe.html', 'http://www.mamilade.de/el/sombrero/saarbruecken/familie/2024620-saarbruecken_sombrero.html', 'http://www.mamilade.de/gutsschenke/burg/rabenstein/2024620-rabenstein_gutsschenke.html', 'http://www.mamilade.de/steffs/fleetenkieker/friedrichskoog/familie/2024620-friedrichskoog_steffs.html', 'http://www.mamilade.de/alemannenhof/engel/rickenbach/2024620-rickenbach_alemannenhof.html', 'http://www.mamilade.de/rievkooche/lounge/koeln/essen/familie/2024620-rievkooche_lounge.html', 'http://www.mamilade.de/see/camping/neubaeuer/2024620-neubaeuersee_camping.html', 'http://www.mamilade.de/delitzsch/eiscafe/mario/gelato/2024620-delitzsch_eiscafe.html', 'http://www.mamilade.de/landhaus/beckmann/kalkar/familie/essen/2024620-landhaus_beckmann.html', 'http://www.mamilade.de/frankfurt/cafe/museumfuerkommunikation/familienessen/2024620-ffm_cafe_museum.html', 'http://www.mamilade.de/kaffeegarten/ponyhof/wulften/familie/2024620-kaffeegarten_wulften.html', 'http://www.mamilade.de/comodo/lueneburg/familie/essen/2024620-comodo_lueneburg.html', 'http://www.mamilade.de/seaview/bitterfeld/2024620-bitterfeld_seaview.html', 'http://www.mamilade.de/leipzig/cafe/yellow/2024620-lpz_cafeyellow.html', 'http://www.mamilade.de/burgschaenke/bad/dueben/goldenerloewe/2024620-baddueben_burgschaenke.html', 'http://www.mamilade.de/restaurant/wulmstorf/familie/essen/2024620-outland_wulmstorf.html', 'http://www.mamilade.de/cafe/loesch/dresden/2024620-dresden_cafeloesch.html', 'http://www.mamilade.de/waldhotel/heiderhof/obersteinebach/2024620-heiderhof.html', 'http://www.mamilade.de/stern/bad/waldsee/reute/2024620-badwaldsee_stern.html', 'http://www.mamilade.de/troika/restaurant/obergrunstedt/familienessen/2024620-obergrunstedt_troika.html', 'http://www.mamilade.de/bratwurst/roeslein/nuernberg/2024620-nuernberg_bratwurst.html', 'http://www.mamilade.de/scheffellinde/achdorf/familie/essen/2024620-achdorf_scheffellinde.html', 'http://www.mamilade.de/neustadt/marienhof/hofanlage/2024620-neustadt_marienhof.html', 'http://www.mamilade.de/madonie/trattoria/hamburg/2024620-madonie_hamburg.html', 'http://www.mamilade.de/freund/blase/berlin/2024620-freund_blase_berlin.html', 'http://www.mamilade.de/stern/gollhofen/2024620-gollhofen_stern.html', 'http://www.mamilade.de/wunderbar/weite/welt/eppstein/2024620-eppstein_wunderbar.html', 'http://www.mamilade.de/ernos/bistro/frankfurt/2024620-ffm_ernosbistro.html', 'http://www.mamilade.de/waldesruh/see/aumuehle/familie/2024620-aumuehle_waldesruh.html', 'http://www.mamilade.de/makedonia/heidelberg/2024620-heidelberg_makedonia.html', 'http://www.mamilade.de/hofcafe/duxener/strauss/steyerberg/minden/familie/2024620-hofcafe_duxen.html', 'http://www.mamilade.de/seehotel/seebogen/arrach/2024620-arrach_seebogen.html', 'http://www.mamilade.de/bauernmarkt/sietow/2024620-bauernmarkt_sietow_essen.html', 'http://www.mamilade.de/donaublick/scheer/familie/2024620-scheer_donaublick.html', 'http://www.mamilade.de/restaurant/neumann/usingen/2024620-usingen_restaurantneumann.html', 'http://www.mamilade.de/wernigerode/baumkuchen/cafe/2024620-wernigerode_baumkuchenca.html', 'http://www.mamilade.de/bravo/eiscafe/vollmersheim/2024620-vollmershaineiscafe.html', 'http://www.mamilade.de/wenzel/prager/bierstuben/halle/2024620-halle_wenzel.html', 'http://www.mamilade.de/eiscafe/bergziege/dresden/2024620-dresden_eiscafe_berg.html', 'http://www.mamilade.de/pari/csarda/burgstaedt/familienessen/2024620-paricsarda.html', 'http://www.mamilade.de/cafe/fritz/elbschloss/bleckede/2024620-cafe_fritz.html', 'http://www.mamilade.de/wangen/landgasthaus/sonne/2024620-wangen_sonne.html', 'http://www.mamilade.de/vogelbacher/hof/dachsberg/2024620-dachsberg_vogelbacherhof.html', 'http://www.mamilade.de/pony/waldschaenke/hamburg/essen/familien/2024620-hamburg_ponywaldsch.html', 'http://www.mamilade.de/el/comedor/sinzig/familienessen/2024620-elcomedor.html', 'http://www.mamilade.de/falken/wiesloch/baiertal/2024620-wiesloch_falken.html', 'http://www.mamilade.de/enchilada/halle/mexikanisches/restaurant/2024620-halle_enchilada.html', 'http://www.mamilade.de/weingut/fritz/allendorf/georgshof/2024620-allendorf_weingut.html', 'http://www.mamilade.de/schmelz/brauhaus/familie/essen/2024620-brauhaus_schmelz.html', 'http://www.mamilade.de/gruener/baum/steinfurt/familie/2024620-steinfurt_gruenerbaum.html', 'http://www.mamilade.de/giraffe/berlin/2024620-giraffe_berlin.html', 'http://www.mamilade.de/restaurant/abthof/muehlheim/familienessen/2024620-muehlheim_abthof.html', 'http://www.mamilade.de/restaurant/nachtigall/nudel/jena/2024620-jena_nachtigall.html', 'http://www.mamilade.de/deggenhausertal/sternen/2024620-deggenhausertal_sternen.html', 'http://www.mamilade.de/vita/bella/osteria/erlangen/2024620-erlangen_osteria_vita.html', 'http://www.mamilade.de/coenenmuhele/pfannkuchen/wermelskirchen/essen/familie/2024620-coenenmuehle_wermelskirch.html', 'http://www.mamilade.de/charlottchen/berlin/2024620-charlottchen_berlin.html', 'http://www.mamilade.de/zurschoenenmuellerin/frankfurt/apfelweinrestaurant/2024620-ffm_zurschoenenmuellerin.html', 'http://www.mamilade.de/landgasthof/rechberg/hof/familie/essen/2024620-rechberg_landgasthof.html', 'http://www.mamilade.de/gut/welpe/vechta/familie/essen/2024620-gut_welpe.html', 'http://www.mamilade.de/bergschenke/restaurant/biergarten/halle/2024620-halle_bergschenke.html', 'http://www.mamilade.de/vecchio/teatro/xanten/2024620-vecchio_teatro.html', 'http://www.mamilade.de/forsthaus/jaegerhaus/weiler/bingen/2024620-weiler_forsthaus.html', 'http://www.mamilade.de/eiscafe/worms/dresden/2024620-dresden_eiscafe_worms.html', 'http://www.mamilade.de/waldrasthaus/karches/familie/2024620-bischofsgruen_karches.html', 'http://www.mamilade.de/cafe/kap/west/leipzig/2024620-leipzig_cafekap.html', 'http://www.mamilade.de/don/chemnitz/restaurant/familienessen/2024620-chemnitz_don.html', 'http://www.mamilade.de/wirtshaus/mausefalle/bad/liebenstein/2024620-wirtshaus_mausefalle.html', 'http://www.mamilade.de/stadtcafe/kremer/marne/familie/2024620-marne_kremer_cafe.html', 'http://www.mamilade.de/kona/coffee/pustet/regensburg/familie/2024620-regensburg_kona_pustet.html', 'http://www.mamilade.de/dresden/cafe/tortuga/familienessen/2024620-dresden_cafe_tortuga.html', 'http://www.mamilade.de/cafe/steinbruch/duisburg/essen/familie/2024620-cafe_steinbruch.html', 'http://www.mamilade.de/signalstein/obertrubach/familie/2024620-obertrubach_signalstein.html', 'http://www.mamilade.de/bauersfeld/jena/cafe/restaurant/2024620-jena_bauersfeld.html', 'http://www.mamilade.de/mittelalterliches/restaurant/zurtafelrunde/magdeburg/2024620-magdeburg_mittelalterlich.html', 'http://www.mamilade.de/albgasthof/baeren/bernstadt/2024620-bernstadt_baeren.html', 'http://www.mamilade.de/kaiserslautern/papasote/mexikanisches/restaurant/2024620-paasote_kaisrslautern.html', 'http://www.mamilade.de/gaststaette/lindengarten/weissenbrunn/familienessen/2024620-weissenbrunn_lindengarten.html', 'http://www.mamilade.de/anna/krodoland/harzburg/2024620-anna_krodo.html', 'http://www.mamilade.de/asado/koeln/essen/familie/2024620-asado_koeln.html', 'http://www.mamilade.de/muehlenschenke/siegelsbach/essen/2024620-siegelsbach_muehlen_2.html', 'http://www.mamilade.de/pfannkuchen/hannover/2024620-pfannkuchen_h.html', 'http://www.mamilade.de/meyers/hof/zoo/hannover/familie/essen/2024620-meyers_hof.html', 'http://www.mamilade.de/pohlteichschaenke/kirchberg/ausflugsgaststaette/2024620-kirchberg_pohlteichschaen.html', 'http://www.mamilade.de/fabbrica/italianna/hattingen/familie/essen/2024620-fabbrica_italiana.html', 'http://www.mamilade.de/bunte/kuh/helgoland/2024620-helgoland_buntekuh.html', 'http://www.mamilade.de/block/house/hamburg/essen/familie/2024620-block_house_hamburg.html', 'http://www.mamilade.de/bellevue/flensburg/familie/2024620-flensburg_bellevue.html', 'http://www.mamilade.de/roemische/herberge/xanten/2024620-herberge_xanten.html', 'http://www.mamilade.de/aneljapa/berlin/2024620-aneljapa_berlin.html', 'http://www.mamilade.de/wiesbacher/hof/restaurant/wiesbach/2024620-wiesbacherhof.html', 'http://www.mamilade.de/carpe/diem/rehburg/2024620-carpe_diem.html', 'http://www.mamilade.de/meindl/arrach/familie/2024620-arrach_meindl.html', 'http://www.mamilade.de/gasthauszumbaeren/frankfurt/familienessen/2024620-ffm_gasthauszumbaeren.html', 'http://www.mamilade.de/ilsenburg/forellenstube/familienessen/2024620-ilsenburg_forellenstube.html', 'http://www.mamilade.de/cafe/immergruen/jena/2024620-jena_cafe_immergruen.html', 'http://www.mamilade.de/riedenburg/fassl/wirtschaft/2024620-riedenburg_fasslwirt.html', 'http://www.mamilade.de/gasthof/kolb/bayreuth/2024620-bayreuth_kolb.html', 'http://www.mamilade.de/clubhaus/aussicht/gaiberg/2024620-gaiberg_clubhaus.html', 'http://www.mamilade.de/linden/windelsbach/familie/2024620-windelsbach_linden.html', 'http://www.mamilade.de/birke/kulmbach/familie/2024620-kulmbach_birke.html', 'http://www.mamilade.de/lichtenburg/ostheim/essen/familie/2024620-ostheim_lichtenburg_rest.html', 'http://www.mamilade.de/klostergasthof/burgkirchen/familie/essen/2024620-klostergasthof.html', 'http://www.mamilade.de/de/medici/trattoria/rosdorf/familie/essen/2024620-demedici_rosdorf.html', 'http://www.mamilade.de/zschoner/muehle/dresden/2024620-dresden_zschoner_muehle.html', 'http://www.mamilade.de/schoenwald/turm/2024620-schoenwald_turm.html', 'http://www.mamilade.de/saarwellingen/lachwald/familie/2024620-saarwellingen_lachwald.html', 'http://www.mamilade.de/idylle/borchers/surwold/essen/familie/2024620-borchers_idylle.html', 'http://www.mamilade.de/lsc/restaurant/friedrichshafen/2024620-friedrichshafen_lsc.html');

$url_c = count($url);





for($x=120;$x<$url_c;$x++){
print($x."\n");


$plz='';
$ort='';
$web='';
$mail='';
$name='';
$tel='';
$str='';
$nr='';
$kat1='';
$kat2='';
$kat3='';
$kat4='';


$html = scraperwiki::scrape($url[$x]);

    # Use the PHP Simple HTML DOM Parser to extract <td> tags
    $dom = new simple_html_dom();
    $dom->load($html);


//mail+web
    $wm = 1;
foreach($dom->find('a.boxes2') as $mail1){
        # Store data in the datastore
            if($wm==1){
                $mail=$mail1->plaintext;
            }
            if($wm==2){
                $web=$mail1->plaintext;
            }
            $wm++;
}


//Name + tel

foreach($dom->find('td[width=250]') as $name1){
         # Store data in the datastore
         $links=$name1->innertext;
         break;
 }


$teil=explode("<br />",$links);

$name=$teil[1];
$tel = $teil[3];


foreach($dom->find('h1.headline_detail') as $name){
         # Store data in the datastore
         $name=$name->innertext;
         break;
 }

//print $name."\n";


//add


foreach($dom->find('td[width=340]') as $addresse){
          # Store data in the datastore
          $rechts=$addresse->innertext;
         break;
  }



$teil2=explode("<br />",$rechts);
$add_teil=explode(" - ",$teil2[1]);


$str_teil = explode(" ",$add_teil[1]);
$str_teil_c = count($str_teil);


if(($str_teil_c)-1==0){
    $str = $str_teil[($str_teil_c)-1];
}else{
$nr = $str_teil[($str_teil_c)-1];

for($k=0;$k<$str_teil_c-1;$k++){
    $str=$str." ".$str_teil[$k];
}
}

$ort_teil = explode(" ",$add_teil[0]);
$ort_teil_c = count($ort_teil);

$plz = $ort_teil[1];

for($k=2;$k<$ort_teil_c;$k++){
    $ort=$ort." ".$ort_teil[$k];
}


//kat

foreach($dom->find('font.categories') as $kategorie){
          # Store data in the datastore

          $kate=$kategorie->plaintext;
         
  }

//print($kate."\n");
$kate = explode("Kategorien: ",$kate);
$kate = $kate[1];


$kateg = explode(" - ",$kate);

if(count($kateg)==3){
 $bundesland = $kateg[0];
 $kat1 = $kateg[1];
 $kat2 = $kateg[2];
}elseif(count($kateg)==2){
  $bundesland = $kateg[0];
  $kat1 = $kateg[1];
 }elseif(count($kateg)==1){
   $bundesland = $kateg[0];
 }elseif(count($kateg)==4){
 $bundesland = $kateg[0];
  $kat1 = $kateg[1];
  $kat2 = $kateg[2];
 $kat3 = $kateg[3];
}else{
 $bundesland = $kateg[0];
   $kat1 = $kateg[1];
   $kat2 = $kateg[2];

    for($k=3;$k<count($kateg);$k++){
        $kat3 = $kat3." - ".$kateg[$k];
    }
}

    /*print($kat1."\n");
    print($kat2."\n");
    print($kat3."\n");
    print($kat4."\n");*/


$str=utf8_encode($str);
$ort=utf8_encode($ort);
$name=utf8_encode($name);

$kat1=utf8_encode($kat1);
$kat2=utf8_encode($kat2);
$kat3=utf8_encode($kat3);
$bundesland=utf8_encode($bundesland);

$name=str_replace('"','',$name);


$plz=trim($plz);
$ort=trim($ort);
$web=trim($web);
$mail=trim($mail);
$name=trim($name);
$tel=trim($tel);
$str=trim($str);
$nr=trim($nr);
$kat1=trim($kat1);
$kat2=trim($kat2);
$kat3=trim($kat3);
$bundesland=trim($bundesland);


trim($name);


scraperwiki::save(array('name','str','nr','plz','ort','tel','mail','web','kat1','kat2','kat3','bundesland'), array('name' => $name ,'str' => $str, 'nr' => $nr, 'plz' => $plz, 'ort' => $ort, 'tel' => $tel, 'mail' => $mail ,'web' => $web ,'kat1' => $kat1 ,'kat2' => $kat2 ,'kat3' => $kat3 ,'bundesland' => $bundesland));






/*

print('plz '.$plz."\n");
print('ort '.$ort."\n");
print('web '.$web."\n");
print('mail '.$mail."\n");
print('name '.$name."\n");
 print('tel '.$tel."\n");
print('str '.$str."\n");
 print('nr '.$nr."\n");
*/

}

?>
