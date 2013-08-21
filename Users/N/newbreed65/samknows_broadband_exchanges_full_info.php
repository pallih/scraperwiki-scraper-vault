<?php
require 'scraperwiki/simple_html_dom.php';
    //  The following is a list of Exchange SAUIDs gleaned from SamKnows

$codes =
array('WSERS','WSESK','WSFAI','WSFEN','WSFIN','WSFIO','WSFIV','WSFOR','WSFOT','WSFUR','WSGAE','WSGAI','WSGAL','WSGAR','WSGAT','WSGIF','WSGIG','WSGIR','WSGLC','WSGLE','WSGLG','WSGLL','WSGLU','WSGOU','WSGOV','WSGRE','WSGRS','WSGRT','WSHAL','WSHAM','WSHAU','WSHEL','WSHOL','WSIBR','WSINN','WSINS','WSINV','WSIRS','WSIRV','WSJOB','WSJOH','WSJOP','WSJUR','WSKBN','WSKET','WSKGE','WSKIA','WSKIB','WSKIC','WSKID','WSKIE','WSKIF','WSKIG','WSKII','WSKIK','WSKIL','WSKIM','WSKIN','WSKIO','WSKIP','WSKIR','WSKIU','WSKIW','WSKIY','WSKKC','WSKKD','WSKKE','WSKKF','WSKKL','WSKKN','WSKKO','WSKKR','WSKKT','WSKKZ','WSKLM','WSKLN','WSKRK','WSLAA','WSLAB','WSLAH','WSLAK','WSLAL','WSLAM','WSLAN','WSLAR','WSLAU','WSLEA','WSLED','WSLEN','WSLES','WSLEW','WSLEX','WSLID','WSLIS','WSLOA','WSLOC','WSLOD','WSLOE','WSLOG','WSLOH','WSLOI','WSLON','WSLOS','WSLOT','WSLUI','WSLUS','WSMAB','WSMAC','WSMAH','WSMAR','WSMAU','WSMAY','WSMER','WSMIL','WSMIN','WSMIT','WSMOC','WSMOD','WSMOF','WSMON','WSMOS','WSMOT','WSMOU','WSMUI','WSNEA','WSNEB','WSNEC','WSNEG','WSNEL','WSNES','WSNEW','WSOBA','WSOCH','WSOLD','WSORM','WSPAI','WSPAL','WSPAN','WSPAR','WSPAT','WSPEN','WSPIN','WSPIR','WSPOA','WSPOC','WSPOE','WSPOL','WSPOP','WSPOR','WSPOS','WSPOW','WSPRE','WSPRO','WSPTH','WSPTN','WSREN','WSRHU','WSRIN','WSROC','WSROT','WSRUT','WSSAL','WSSAN','WSSAQ','WSSCA','WSSCO','WSSHE','WSSHI','WSSKI','WSSKL','WSSLI','WSSOE','WSSOK','WSSOR','WSSOU','WSSPR','WSSTD','WSSTE','WSSTN','WSSTO','WSSTR','WSSTT','WSSTU','WSSTW','WSSYM','WSTAB','WSTAH','WSTAR','WSTAT','WSTAY','WSTHL','WSTHO','WSTIG','WSTIN','WSTIR','WSTOB','WSTOD','WSTOR','WSTOW','WSTRO','WSTUR','WSTWE','WSTWY','WSTYN','WSUDD','WSULV','WSUPL','WSWAT','WSWEK','WSWEM','WSWES','WSWHB','WSWHH','WSWHI','WSWIG','WSWIS','WWANST','WWASHB','WWASHC','WWASHR','WWASHW','WWAXMI','WWBAMP','WWBARN','WWBAWT','WWBCAU','WWBCKL','WWBCKN','WWBCLY','WWBDON','WWBEAF','WWBEAW','WWBERE','WWBFAS','WWBIDE','WWBIGB','WWBKNO','WWBLAG','WWBLYD','WWBNYM','WWBODM','WWBOSC','WWBOW','WWBRAN','WWBRAU','WWBRAY','WWBRDY','WWBREA','WWBRIX','WWBROA','WWBROM','WWBRUL','WWBSTM','WWBSTW','WWBTON','WWBTOR','WWBTRA','WWBUDE','WWBUDL','WWBURN','WWBURR','WWBWAT','WWCALL','WWCAMB','WWCAME','WWCANW','WWCARD','WWCARY','WWCBIS','WWCCKW','WWCFIT','WWCHAG','WWCHEL','WWCHID','WWCHIS','WWCHIT','WWCHIV','WWCHLL','WWCHRD','WWCHRI','WWCHRM','WWCHRS','WWCHUD','WWCHUL','WWCLAY','WWCLOV','WWCMAC','WWCMAR','WWCOAD','WWCOLY','WWCONS','WWCOPP','WWCORN','WWCORS','WWCORT','WWCPOL','WWCRAD','WWCRAL','WWCRAN','WWCRED','WWCREW','WWCROY','WWCRWC','WWCRWN','WWCSTN','WWCULL','WWCWIC','WWDART','WWDAWL','WWDITT','WWDOBW','WWDOLT','WWDOWN','WWDPRT','WWDRAN','WWDREW','WWDULV','WWDUNS','WWEALL','WWEVER','WWEXBO','WWEXFO','WWEXMN','WWEXMO','WWEXTR','WWFALM','WWFARW','WWFENI','WWFILL','WWFOWE','WWFRAD','WWFROG','WWGARA','WWGERM','WWGHAM','WWGRAM','WWGUNN','WWHARB','WWHART','WWHATH','WWHAWK','WWHAYL','WWHBCK','WWHBCM','WWHCRX','WWHELE','WWHELS','WWHEMY','WWHENL','WWHOLB','WWHOLF','WWHOLN','WWHOLS','WWHONI','WWHTOR','WWILCH','WWILFR','WWILMI','WWINST','WWIPPL','WWISLE','WWIVYB','WWKENN','WWKENT','WWKGWR','WWKILK','WWKKWL','WWKNGB','WWKSTM','WWLAND','WWLANR','WWLAPF','WWLAUN','WWLDOW','WWLEED','WWLIFT','WWLISK','WWLLAW','WWLODD','WWLOOE','WWLOST','WWLPRT','WWLSTL','WWLSUT','WWLTRE','WWLUPP','WWLVET','WWLWDN','WWLYDF','WWLYME','WWLYNT','WWMABT','WWMARA','WWMARK','WWMART','WWMAWG','WWMBSH','WWMCAN','WWMDAM','WWMEVA','WWMILV','WWMINE','WWMITC','WWMLBK','WWMMAG','WWMODY','WWMORT','WWMORW','WWMOUS','WWMPRT','WWMSMT','WWMTON','WWMTVY','WWMULL','WWNABB','WWNANP','WWNCAD','WWNCUR','WWNCYR','WWNETH','WWNEWQ','WWNFER','WWNMOL','WWNPTN','WWNPWI','WWNTAM','WWNTAW','WWNTCY','WWOAKF','WWOKEH','WWOSMY','WWOSTN','WWPADS','WWPAIG','WWPAR','WWPCMB','WWPENZ','WWPERR','WWPINH','WWPIPE','WWPISA','WWPLRN','WWPOLP','WWPORL','WWPOST','WWPOUN','WWPRAZ','WWPREA','WWPRIN','WWPRYN','WWPSCO','WWPSTK','WWPTON','WWPTRE','WWPTWN','WWPURI','WWPYTH','WWRACK','WWREDR','WWRILL','WWROBO','WWROCH','WWRUMF','WWSAGN','WWSALC','WWSALT','WWSAMP','WWSAUS','WWSBNT','WWSBUD','WWSBUR','WWSCAN','WWSCHD','WWSCIL','WWSCLM','WWSCOL','WWSDAY','WWSDOM','WWSEAT','WWSENN','WWSFLM','WWSGAB','WWSGEN','WWSGER','WWSHAL','WWSHAU','WWSHEB','WWSHER','WWSHIP','WWSHIR','WWSIDB','WWSIDM','WWSILV','WWSIVE','WWSJUS','WWSKEV','WWSMAB','WWSMAR','WWSMER','WWSMOL','WWSMWG','WWSMWS','WWSOME','WWSOWT','WWSPAX','WWSPET','WWSTAL','WWSTAR','WWSTAV','WWSTEN','WWSTIC','WWSTIT','WWSTOC','WWSTOG','WWSTUD','WWSUTT','WWSWIM','WWTAUN','WWTAVI','WWTEDB','WWTEIG','WWTEMP','WWTHRE','WWTIMB','WWTINT','WWTIVE','WWTLIZ','WWTOPS','WWTORQ','WWTORR','WWTORX','WWTOTN','WWTPNT','WWTREB','WWTREG','WWTRES','WWTRUR','WWUPOT','WWVERY','WWWADE','WWWASH','WWWBAY','WWWCKR','WWWDGT','WWWDWN','WWWEEK','WWWELL','WWWEMB','WWWFRD','WWWHEA','WWWHIM','WWWILL','WWWILM','WWWINC','WWWITH','WWWIVE','WWWKLH','WWWMON','WWWMOR','WWWOOD','WWWOOL','WWWSHM','WWWZOY','WWYEAL','WWYELV','WWYEOV','WWYETM','WWZELA');

foreach($codes as $code) {

    echo "Loading " . $code . "...";
    $html = scraperWiki::scrape("http://www.samknows.com/broadband/exchange/" . $code);
    echo "Loaded";
    $dom = new simple_html_dom();
    $dom->load($html);
    $line = array('code' => $code );
    
    foreach ($dom->find("div.item-content tr") as $row) {
      $headers = $row->find("th");
      $columns = $row->find("td");
      
      if (preg_match("/Exchange name/", $headers[0]->plaintext)) { $line["Exchange"] = $columns[0]->plaintext; }
      
      if (preg_match("/Location/", $headers[0]->plaintext)) { $line["Location"] = $columns[0]->plaintext; }
      if (preg_match("/Postcode/", $headers[0]->plaintext)) { $line["postcode"] = $columns[0]->plaintext; }
      
      /* Broadband availability overview */
      if (preg_match("/ADSL:/", $headers[0]->plaintext)) { $line["ADSL"] = $columns[0]->plaintext; }
      if (preg_match("/SDSL:/", $headers[0]->plaintext)) { $line["SDSL"] = $columns[0]->plaintext; }
      if (preg_match("/LLU services:/", $headers[0]->plaintext)) { $line["LLU"] = $columns[0]->plaintext; }
      if (preg_match("/Cable:/", $headers[0]->plaintext)) { $line["Cable"] = $columns[0]->plaintext; }
      if (preg_match("/Wireless:/", $headers[0]->plaintext)) { $line["Wireless"] = $columns[0]->plaintext; }
      
      /* Cable Broadband Availability */
      if (preg_match("/Virgin Media/", $headers[0]->plaintext)) { $line["VirginMedia"] = $columns[0]->plaintext; }
      if (preg_match("/Smallworld Media/", $headers[0]->plaintext)) { $line["SmallworldMedia"] = $columns[0]->plaintext; }
      
      /* LLU operator presence */
      if (preg_match("/AOL:/", $headers[0]->plaintext)) { $line["AOL"] = $columns[0]->plaintext; }
      if (preg_match("/O2/", $headers[0]->plaintext)) { $line["O2"] = $columns[0]->plaintext; }
      if (preg_match("/Be/", $headers[0]->plaintext)) { $line["Be"] = $columns[0]->plaintext; }
      if (preg_match("/C&W:/", $headers[0]->plaintext)) { $line["CW"] = $columns[0]->plaintext; }
      if (preg_match("/Digital Region:/", $headers[0]->plaintext)) { $line["DigitalRegion"] = $columns[0]->plaintext; }
      if (preg_match("/Edge Telecom:/", $headers[0]->plaintext)) { $line["EdgeTelecom"] = $columns[0]->plaintext; }
      if (preg_match("/Entanet:/", $headers[0]->plaintext)) { $line["Entanet"] = $columns[0]->plaintext; }
      if (preg_match("/KC (Kingston):/", $headers[0]->plaintext)) { $line["KC"] = $columns[0]->plaintext; }
      if (preg_match("/Lumison:/", $headers[0]->plaintext)) { $line["Lumison"] = $columns[0]->plaintext; }
      if (preg_match("/NewNet:/", $headers[0]->plaintext)) { $line["NewNet"] = $columns[0]->plaintext; }
      if (preg_match("/Node4:/", $headers[0]->plaintext)) { $line["Node4"] = $columns[0]->plaintext; }
      if (preg_match("/Pipex:/", $headers[0]->plaintext)) { $line["Pipex"] = $columns[0]->plaintext; }
      if (preg_match("/Redstone:/", $headers[0]->plaintext)) { $line["Redstone"] = $columns[0]->plaintext; }
      if (preg_match("/Rutland Telecom:/", $headers[0]->plaintext)) { $line["Rutland"] = $columns[0]->plaintext; }
      if (preg_match("/Sky/", $headers[0]->plaintext)) { $line["Sky"] = $columns[0]->plaintext; }
      if (preg_match("/Easynet:/", $headers[0]->plaintext)) { $line["Easynet"] = $columns[0]->plaintext; }
      if (preg_match("/Smallworld:/", $headers[0]->plaintext)) { $line["Smallworld"] = $columns[0]->plaintext; }
      if (preg_match("/TalkTalk/", $headers[0]->plaintext)) { $line["TalkTalk "] = $columns[0]->plaintext; }
      if (preg_match("/Tiscali:/", $headers[0]->plaintext)) { $line["Tiscali"] = $columns[0]->plaintext; }
      if (preg_match("/Tiscali TV:/", $headers[0]->plaintext)) { $line["TiscaliTV"] = $columns[0]->plaintext; }
      if (preg_match("/WB Internet:/", $headers[0]->plaintext)) { $line["WB"] = $columns[0]->plaintext; }
      if (preg_match("/Zen Internet:/", $headers[0]->plaintext)) { $line["Zen"] = $columns[0]->plaintext; }

   }        
   
   scraperwiki::save(array("code"),$line);

}
?>