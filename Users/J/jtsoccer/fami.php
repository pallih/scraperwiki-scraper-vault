<?php
require  'scraperwiki/simple_html_dom.php';



$url=array('cafe-junge-L791.html', 'nationalpark-unteres-odertal-L924.html', 'hochseilgarten-schloss-dreiluetzow-L1328.html', 'fussball-center-pagelsdorf-L1423.html', 'windmuehle-osterbruch-ferienwohnung-und-museum-L2196.html', 'goertz-kinder-club-im-aez-hamburg-L2706.html', 'tala-300-aktivhalle-langenhorn-L3686.html', 'haus-der-natur-ahrensburg-wulfdsorf-jordsand-verein-L3746.html', 'bogenschule-stellmoor-L4216.html', 'spiel-spass-scheune-L511.html', 'reiterhof-thormaehlen-L755.html', 'spielplatz-woehrendamm-L836.html', 'arriba-erlebnisbad-norderstedt-L913.html', 'spielplatz-am-blockhaus-L1252.html', 'forsthaus-seebergen-L1399.html', 'hochseilgarten-luetjensee-L1400.html', 'siemerssche-hof-L1507.html', 'circus-allmendus-projekt-L1931.html', 'atelier-sinnes-art-L2496.html', 'natureum-niederelbe-L742.html', 'wasserspielplatz-ahrensburg-L822.html', 'fannyhoeh-gastronomie-und-kegelbahn-L1285.html', 'badlantic-halle-sauna-freibad-L1286.html', 'haus-am-schuehberg-skulpturenpark-L1321.html', 'feuerwehrmuseum-L1584.html', 'stormarnsches-dorfmuseum-L1688.html', 'hotel-restaurant-cafeseehof-luetjensee-L1818.html', 'halimos-hochseilgarten-elmshorn-L2203.html', 'wasserski-und-wakeboarding-neuhaus-oste-L3891.html', 'indoo-spielwerk-L533.html', 'schloss-ahrensburg-L761.html', 'wildpark-moelln-L879.html', 'tourismus-und-naturzentrum-erlebnisreich-moelln-L1004.html', 'eulenspiegelmuseum-moelln-L1031.html', 'der-laemmerhof-biomarkt-kinderwerkstatt-L1331.html', 'ein-labyrinth-im-irrgarten-L1777.html', 'maerchenland-frau-holle-L2737.html', 'pinguin-museum-cuxhaven-L3801.html', 'treibholz-kanu-floss-herberge-L4278.html', 'freizeitzentrum-lohe-bargteheide-L1065.html', 'heuherberge-dargow-L1089.html', 'land-cafe-beimoor-L1191.html', 'aquarium-schwedt-L1443.html', 'mueritztherme-roebel-L1630.html', 'luftfahrttechnisches-museum-rechlin-L1668.html', 'bahnhofsmuseum-roebel-L1669.html', 'erdbeerhof-glantz-und-glantz-gloria-restaurant-L1728.html', 'hofladen-gut-wulksfelde-L3809.html', 'cafe-und-velohotel-auf-vokuhls-bauernhof-L4364.html', 'erlebnisbahn-ratzeburg-L1005.html', 'funtasia-L1304.html', 'drei-seen-schiffahrt-in-plau-am-see-L1461.html', 'pension-gutshaus-barkow-L1477.html', 'gaststaette-waldesruh-L1547.html', 'freibad-mueritzbad-L1631.html', 'swin-golf-L1667.html', 'tellerwerk-keramik-malstudio-L1746.html', 'kleines-theater-bargteheide-kino-L2490.html', 'bio-hofladen-domaene-fredeburg-L4363.html', 'kindertobeland-wumbawu-L366.html', 'pferdehof-ruhnau-L740.html', 'schweriner-schloss-L1146.html', 'fun-arena-neu-ab-20maerz-2011-L3824.html', 'tiergarten-neustrelitz-L4087.html', 'slawendorf-neustrelitz-L4088.html', 'atrium-museum-an-der-schleuse-L4160.html', 'copacanala-strandbar-L4163.html', 'freilichtmuseum-fuer-volkskunde-schwerin-muess-L4458.html', 'schweriner-kletterwald-L4459.html', 'grenzhus-museum-cafe-grenzstein-L1030.html', 'holsten-therme-kaltenkirchen-L1093.html', 'wildnisschule-teerofenbruecke-L1262.html', 'sommerrodelbahn-malchow-L1474.html', 'affenwald-malchow-L1475.html', 'holstentherme-kaltenkirchen-L2022.html', 'naturerlebnis-grabau-L2186.html', 'halimos-hochseilgarten-kaltenkirchen-L2204.html', 'loedings-bauernhof-am-see-L3107.html', 'private-indianerausstellung-L3653.html', 'robinson-club-fleesensee-L351.html', 'wal-indoorspielpark-L471.html', 'seehundstation-friedrichskoog-L1180.html', 'agrarhistorisches-museum-alt-schwerin-L1670.html', 'freibad-poggensee-bad-oldesloe-L2041.html', 'abenteuerzug-mecklenburg-L2198.html', 'hof-caf-gross-niendorf-L4067.html', 'mueritzer-bauernmarkt-L4106.html', 'quacki-quads-kids-L4107.html', 'europas-laengster-obst-lehrpfad-L4746.html', 'mueritzeum-L330.html', 'deichrestaurant-zur-spitze-L1114.html', 'waldschwimmbad-burg-L1561.html', 'kletterwald-mueritz-L1672.html', 'wisent-reservat-L1673.html', 'gesteinssprechstunde-L2933.html', 'king-louii-indoor-spielplatz-L3559.html', 'friesengestuet-alt-wittenbergen-L4010.html', 'roland-oase-warmwasserfreibad-bad-bramstedt-L4164.html', 'spielzeug-ausstellung-wiking-und-siku-modelle-L4629.html', 'wildpark-eekholt-L906.html', 'draegerpark-spielplatz-rodelberg-luebeck-L932.html', 'marzipan-land-L1022.html', 'kinderplaneta-spielpark-L1156.html', 'kino-koki-L1158.html', 'museum-fuer-puppentheater-theaterfigurenmuseum-L1298.html', 'van-der-valk-resort-linstow-L1468.html', 'buddenbrookhaus-L2159.html', 'golfbauernhof-L2202.html', 'hofcafe-und-hofladen-hof-weide-L3105.html', 'indoorspielplatz-susi-und-die-kleinen-strolche-L666.html', 'segeberger-kalkberghoehlen-L802.html', 'noctalis-welt-der-fledermaeuse-L803.html', 'piraten-meer-spassbad-buesum-L990.html', 'piraten-meer-buesum-L1083.html', 'sportpark-huelshorst-L1797.html', 'indian-village-L2034.html', 'abacolino-L3006.html', 'die-krakower-seenlandschaft-L3114.html', 'indoor-freizeithalle-auszeit-inside-L4305.html', 'erlebnis-und-tigerpark-L221.html', 'gartenbahn-schackendorf-L801.html', 'blanker-hans-buesum-sturmflutenwelt-L987.html', 'restaurant-blanker-hans-L1112.html', 'agrarmuseum-dorf-mecklenburg-L1126.html', 'bauspielplatz-roter-hahn-L1332.html', 'archaeologisches-freilichtmuseum-gross-raden-L1787.html', 'outdoor-kartbahn-nordseering-buesum-L3205.html', 'hanse-soccer-L3561.html', 'indianermuseum-gevezin-L4108.html', 'erlebnis-wald-trappenkamp-L772.html', 'steinzeitpark-L1081.html', 'dat-ole-hus-L1330.html', 'maislabyrinth-waren-mueritz-L1589.html', 'feinklettern-hochseilgarten-hanerau-hademarschen-L1665.html', 'erlebnisdorf-daldorf-L3007.html', 'steinzeitdorf-kussow-L3847.html', 'falknerei-damm-L3880.html', 'geburtstagsfeier-auf-dem-westernreiterhof-L4841.html', 'westernreiten-in-der-holsteinischen-schweiz-L4843.html', 'kunti-bunt-L485.html', 'karls-erlebnishof-L933.html', 'museum-tuch-und-technik-L1003.html', 'bad-am-stadtwald-hallefreibad-L1033.html', 'land-und-leute-erlebnispark-L1084.html', 'gestuet-hof-am-see-L1094.html', 'mumpitz-L1437.html', 'viermastbark-passat-L1448.html', 'freizeitbad-albersdorf-L1582.html', 'ostseestation-priwall-L2038.html', 'tierpark-neumuenster-L875.html', 'sea-life-timmendorfer-strand-L927.html', 'tierpark-wismar-L970.html', 'vogelpark-niendorf-L1204.html', 'wonnemar-wismar-L1228.html', 'berlin-in-schleswig-holstein-L1309.html', 'hollis-kinderparadies-L1426.html', 'evershof-L1778.html', 'miniaturgolf-und-fahrradverleih-L1903.html', 'pelotero-fun-city-indoorspielpark-wesselburen-L3889.html', 'natur-und-umweltpark-guestrow-L316.html', 'ostseetherme-scharbeutz-L931.html', 'club-hotel-maritim-timmendorfer-strand-L1167.html', 'schmetterlingspark-L1580.html', 'kirschenhof-stocksee-L2050.html', 'duenengolfen-L3146.html', 'gumdas-spielstrand-L3148.html', 'seebrueckenvorplatz-scharbeutz-L3340.html', 'theaterstrand-L3572.html', 'seebrueckenvorplatz-in-scharbeutz-L4046.html', 'reiterferien-in-schleswig-holstein-L753.html', 'westkuestenpark-L1131.html', 'bananenmuseum-L1207.html', 'duenen-therme-L1237.html', 'schwebefaehre-rendsburg-L1299.html', 'falkenhof-schalkholz-L1315.html', 'kraeuterpark-und-kraeutermuseum-L1548.html', 'wasserskianlage-suesel-L2199.html', 'wildtierland-gut-klepelshagen-L4064.html', 'swingolf-boltenhagen-L4079.html', 'familotel-landhaus-pfahlershof-L18.html', 'poeler-piratenland-L620.html', 'arche-warder-L1132.html', 'eiscafe-und-adventure-golf-minigolf-L1326.html', 'kuestenwache-studio-besichtigung-L1747.html', 'hofanlage-marienhof-cafe-spielplatz-bauernmarkt-L2187.html', 'ferienland-salem-kolping-urlaub-L2692.html', 'hansapark-sierksdorf-L3005.html', 'reiterhof-und-ponyhof-hohelieth-bei-ploen-L4063.html', 'zeittor-museum-der-stadt-neustadt-in-holstein-L4348.html', 'rappel-zappel-tobehalle-L667.html', 'groemitzer-welle-L1111.html', 'modellbahn-zauber-L1240.html', 'mais-labyrinth-sieversdorf-L1812.html', 'wunderweltwasser-L2055.html', 'landmaschinen-modellausstellung-L2185.html', 'glasblaeserei-malente-L2472.html', 'hochseilgarten-malente-L2473.html', 'wildgehege-bad-malente-und-arboretum-L2499.html', 'friesische-schafskaeserei-L4239.html', 'silly-billy-groemitz-L617.html', 'arche-noah-zoo-groemitz-L982.html', 'minigolfanlage-kiel-L1276.html', 'freilichtmuseum-molfsee-L1310.html', 'miniland-mecklenburg-vorpommern-L2280.html', 'naturpark-draisine-L3065.html', 'bebo-funsports-center-ostsee-soccer-L3136.html', 'waldschwimmbad-lensahn-L4012.html', 'gehege-hammer-L4137.html', 'kraxelmaxel-ostsee-kletterpark-groemitz-L4334.html', 'eselpark-nessendorf-L882.html', 'museumshof-lensahn-L1206.html', 'musiculum-L1287.html', 'aquarium-kiel-L1347.html', 'trampolino-kiel-kinder-spiel-park-L1902.html', 'ostseereitschule-luett-piergon-L2882.html', 'leuchtturm-dahmeshoeved-L2883.html', 'jugendherberge-dahme-ostsee-L2885.html', 'task-schauspielschule-fuer-kinder-und-jugendliche-kiel-L3311.html', 'industriemuseum-howaldtsche-metallgiesserei-ev-L4347.html', 'pellewelle-freizeitbad-L1086.html', 'mediendom-kiel-L1348.html', 'nordseemuseum-husum-L1613.html', 'fussball-akademie-dahme-L2879.html', 'aquarell-malkurs-L2893.html', 'ostenfelder-bauernhaus-L3078.html', 'historische-spiellinie-husum-L3142.html', 'dockkoog-badestrand-in-husum-L3143.html', 'milchbar-dahme-L3436.html', 'molli-schmalspurbahn-und-molli-museum-L4029.html', 'rostocker-kinderclub-L618.html', 'zoo-rostock-L984.html', 'minigolf-am-haffbad-L1162.html', 'eiszeitmuseum-L1235.html', 'maislabyrinth-wittbek-L1780.html', 'turmhuegelburg-luetjenburg-L2044.html', 'kinderhafen-dahme-L2860.html', 'strand-spa-sport-und-gesundheitszentrum-dahme-L2880.html', 'obst-erlebnis-garten-L3402.html', 'wildgehege-hasseldieksdamm-L4138.html', 'kinderland-rostock-L621.html', 'ferienhof-plagmann-L752.html', 'columbuspark-weissenhaeuser-strand-L907.html', 'badeparadies-weissenhaeuser-strand-halle-L915.html', 'tierpark-gettorf-L1130.html', 'irrgarten-probsteihagen-mit-minigolfplatz-L1813.html', 'obst-erlebnis-garten-und-maislabyrinth-L1929.html', 'oldenburger-wallmuseum-L2028.html', 'stranddorf-augustenhof-L2206.html', 'abenteuer-dschungelland-am-weissenhaeuser-strand-L2714.html', 'wikinger-museum-haithabu-L73.html', 'u-boot-und-marineehrenmahl-laboe-L1308.html', 'meerwasserschwimmhalle-L1333.html', 'wikingerschaenke-runenstein-L1451.html', 'high-spirits-hochseilgarten-L1493.html', 'hochseilgarten-eckernfoerde-L1551.html', 'stadtmuseum-schleswig-L1612.html', 'probstei-museum-schoenberg-L1799.html', 'krummbeker-kerzenscheune-L3664.html', 'minigolf-und-mee-h-r-L4349.html', 'kinderabenteuerland-wendtorf-ostsee-L908.html', 'schloss-gottorf-L955.html', 'kiddies-fun-center-L1082.html', 'ostsee-info-center-L1155.html', 'restaurant-cafe-strandcottage-schoenberger-strand-L1510.html', 'museumsbahnen-schoenberger-strand-L1562.html', 'piratennest-L3077.html', 'eichhoernchern-station-L4276.html', 'bonbonkocherei-L4277.html', 'wetwind-wassersportschule-L4357.html', 'yachthafenresidenz-hohe-duene-L339.html', 'erlebnisdorf-roevershagen-L619.html', 'erlebnisfreibad-bredstedt-L1115.html', 'vogelpark-marlow-L1457.html', 'naturerlebnisraum-stollberg-L1550.html', 'robbenzentrum-warnemuende-L1803.html', 'spielscheune-amrum-L2570.html', 'aktiv-hus-heiligenhafen-L3814.html', 'ostsee-welten-5d-direkt-am-leuchtturm-in-warnemuende-L4080.html', 'heuherberge-gut-sophienhof-L4387.html', 'schatzinsel-L664.html', 'fun-park-foehr-L665.html', 'reitanlage-kastanienhof-L758.html', 'aquafoehr-L1085.html', 'pfannkuchen-haus-L1110.html', 'freilichtmuseum-klockenhagen-L1125.html', 'swingolf-cafegrave-gut-sophienhof-L4386.html', 'tolk-schau-L4438.html', 'spiel-und-freizeitpark-L4745.html', 'kreativer-erlebnisgeburtstag-bei-istwerkde-L4815.html', 'meereszentrum-fehmarn-L308.html', 'fehmare-schwimmbad-L1109.html', 'u-boot-museum-fehmarn-L1251.html', 'planet-erde-L1581.html', 'naturschatzkammer-paradiesgarten-L2281.html', 'deutsches-bernsteinmuseum-L2282.html', 'naturerlebniswelt-L3355.html', 'museum-katharinenhof-freilichtmuseum-L3815.html', 'ponyhof-und-ferienhof-ogriseck-insel-fehmarn-L3907.html', 'adventure-golf-fehmarn-L4385.html', 'angelner-dampfeisenbahn-L72.html', 'naturerlebnispark-gristow-L329.html', 'phaenomenta-flensburg-L925.html', 'sylt-aquarium-L1175.html', 'tier-und-freizeitpark-L1238.html', 'naturerlebniszentrum-maasholm-L1243.html', 'draisinenbahnhof-leck-L1549.html', 'mr-scandis-funpark-L3681.html', 'barfusspark-schwackendorf-L4552.html', 'eiszeit-haus-flensburg-L4580.html', 'meeresmuseum-L68.html', 'hansedom-L284.html', 'ozeaneum-L354.html', 'sum-sum-indoorspielpark-L663.html', 'tierpark-stralsund-L976.html', 'nautineum-L1046.html', 'technik-erlebnis-museum-zuckerfabrik-barth-L1334.html', 'maislabyrinth-in-oestergaard-L1779.html', 'landschaftsmuseum-angeln-unewatt-L1798.html', 'artefact-powerpark-L1811.html', 'ruegenpark-L283.html', 'experimentarium-L328.html', 'natureum-darsser-ort-L874.html', 'erlebniszentrum-naturgewalten-L1057.html', 'maislabyrinth-lieschow-L1596.html', 'inselrodelbahn-bergen-L3352.html', 'pirateninsel-ruegen-L3674.html', 'foerdeland-therme-gluecksburg-L4390.html', 'seilgarten-prora-L4460.html', 'ferienwohnungen-zingst-darss-L4625.html', 'alaris-schmetterlingspark-sassnitz-L332.html');
$url_c=count($url);

for($k=329;$k<$url_c;$k++){

print $k."\n";



$html = scraperwiki::scrape('http://www.familion.de/'.$url[$k]);

    # Use the PHP Simple HTML DOM Parser to extract <td> tags
    $dom = new simple_html_dom();
    $dom->load($html);



$plz='';
$stadt='';
$web='';
$mail='';
$name='';
$tel='';
$str='';
$nr='';


//Name
foreach($dom->find('td h1') as $name){
         # Store data in the datastore
         $name=$name->innertext;
        //print $name."\n";
         break;
        }


//web
foreach($dom->find('td noindex a') as $web){
          # Store data in the datastore
          $web=$web->innertext;
         //print $web."\n";
         break;
        }

//mail
foreach($dom->find('table.sobiDetails tr td script') as $mail){
          # Store data in the datastore
          $mail=$mail->innertext;
         //print $mail."\n";
         }

$mail = explode(';',$mail);
$mail = str_replace('s = unescape(','',str_replace(')','',str_replace('\'','',$mail[0])));
//print $mail."\n";

//PLZ
foreach($dom->find('span#sobi2Details_field_postcode') as $plz){
           # Store data in the datastore
           $plz=$plz->innertext;
          //print $plz."\n";
          }

//Stadt
foreach($dom->find('span#sobi2Details_field_city') as $stadt){
            # Store data in the datastore
            $stadt=$stadt->innertext;
           //print $stadt."\n";
           }

//str
$stra='';
foreach($dom->find('span#sobi2Details_field_street') as $stra){
             # Store data in the datastore
             $stra=$stra->innertext;
            //print $stra."\n";
            }

$stra = explode(' ',$stra);
$str_c = count($stra);

if($str_c>0){
    $nr = $stra[$str_c-1];
    $str = '';
    for($st = 0; $st<$str_c-1; $st++){
        $str = $str." ".$stra[$st];
    }
}else{
    $nr = '';
    $str = $stra;   
}
//print "st: ".$str."nr ".$nr."\n";


$tel1 ='';
foreach($dom->find('td.det_addr') as $tel1){
             # Store data in the datastore
             $tel1=$tel1->innertext;
            //print $tel1."\n";
            }

$tel1= explode('<br>',$tel1);


$tel= $tel1[2];

$tel= str_replace('Telefon: ','',$tel);

//print $tel."\n";

//BUNDESLAND
$x=1;
foreach($dom->find('td.det_addr b') as $land){
               if($x==2){
                    $bundesland=$land->innertext;
                    break;
                }
                $x++;
            }


//print $land."\n";


//STRING PALACE

$str=utf8_encode($str);
$ort=utf8_encode($stadt);
$name=utf8_encode($name);


$bundesland=utf8_encode($bundesland);

$name=str_replace('"','',$name);


$plz=trim($plz);
$ort=trim($stadt);
$web=trim($web);
$mail=trim($mail);
$name=trim($name);
$tel=trim($tel);
$str=trim($str);
$nr=trim($nr);
$bundesland=trim($bundesland);





scraperwiki::save(array('name','str','nr','plz','ort','tel','mail','web','bundesland'), array('name' => $name ,'str' => $str, 'nr' => $nr, 'plz' => $plz, 'ort' => $stadt, 'tel' => $tel, 'mail' => $mail ,'web' => $web ,'bundesland' => $bundesland));
}
?>
