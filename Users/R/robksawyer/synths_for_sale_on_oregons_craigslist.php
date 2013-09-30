<style type="text/css">
    body{
        font-family: sans-serif;
        color: #666666;
    }
    h1,h2,h3,h4,th {
        color: #000000;
    }
    a{
        color: #000000;
    }
</style>
<?php
/* Synth Manufacturers
"ARP","Access Music","Akai","Alesis","Analogue Systems","Applied Acoustics","Aries","Arturia","BOSS","BitHeadz","Bomb Factory Studios","Casio","Chamberlin","Cheetah","Chimera Synthesis","Clavia","Con Brio","Creamware","Crumar","Dave Smith Instruments","Doepfer","E-mu Systems","EDP","EML","EMS","Electrix Pro","Electro Harmonix","Elektron","Elka","Encore Electronics","Ensoniq","FBT Electronica","Fairlight","Farfisa","Formanta","Future Retro","GForce Software","Generalmusic","Gleeman","Hammond","Hartmann","Hohner","IK Multimedia","Image Line","Jen Electronics","JoMoX","Kawai","Kenton Electronics","KeyFax Hardware","Koblo","Korg","Kurzweil","Linn Electronics","Logan Electronics","MAM","MOTU","MacBeth Studio Systems","Marion Systems","Metasonix","Miscellaneous","Moog Music","Mutronics","Native Instruments","New England Digital","Novation","OSC","Oberheim","Octave","PAiA","PPG","Propellerheads","Prosoniq","Quasimidi","Red Sound Systems","Rhodes","Roland"
*/

$manufacturers = array("ARP","Access Music","Akai","Alesis","Analogue Systems","Applied Acoustics","Aries","Arturia","BOSS","BitHeadz","Bomb Factory Studios","Casio","Chamberlin","Cheetah","Chimera Synthesis","Clavia","Con Brio","Creamware","Crumar","Dave Smith Instruments","Doepfer","E-mu Systems","EDP","EML","EMS","Electrix Pro","Electro Harmonix","Elektron","Elka","Encore Electronics","Ensoniq","FBT Electronica","Fairlight","Farfisa","Formanta","Future Retro","GForce Software","Generalmusic","Gleeman","Hammond","Hartmann","Hohner","IK Multimedia","Image Line","Jen Electronics","JoMoX","Kawai","Kenton Electronics","KeyFax Hardware","Koblo","Korg","Kurzweil","Linn Electronics","Logan Electronics","MAM","MOTU","MacBeth Studio Systems","Marion Systems","Metasonix","Miscellaneous","Moog Music","Mutronics","Native Instruments","New England Digital","Novation","OSC","Oberheim","Octave","PAiA","PPG","Propellerheads","Prosoniq","Quasimidi","Red Sound Systems","Rhodes","Roland");

$ignored_manufacturers = array();
foreach($manufacturers as $manufacturer){
    if(!in_array($manufacturer,$ignored_manufacturers)){
        $tempName = "oregon_".strtolower(trim(str_replace(" ","_",$manufacturer)))."_craigslist_synth_scraper";
        if(strlen($tempName) > 50){
            $dif = strlen($tempName) - 50;
            //echo $dif."<br/>";
            $tempName = substr($tempName,0,-$dif);
        }
        //echo "DB Name: ".$tempName."<br/>";
        $scrapers[] = $tempName;
    }
}

print "<h1 align='center'>Synths found in <a href='http://geo.craigslist.org/iso/us/or' target='_blank'>Oregon</a> from Craigslist.</h1>";
foreach($scrapers as $scraper){
    //echo "Attaching DB: <a href='https://scraperwiki.com/scrapers/".$scraper."' target='_blank'>".$scraper."</a><br/>";
    try {
        $data = file_get_contents("https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=$scraper&query=select%20*%20from%20%60swdata%60");
        //print_r($data);
        /*scraperwiki::attach($scraper);
        $data = scraperwiki::select(           
            "* from $scraper.swdata order by post_item_date asc"
        );*/
        if(!empty($data)){
            $dataDecoded = json_decode($data);
            //print_r($dataDecoded);
            if(!empty($dataDecoded)){
                if(!isset($dataDecoded->error)){
                    print "<br/>";
                    print "<h2>".$dataDecoded[0]->manufacturer." (<a href='https://scraperwiki.com/scrapers/".$scraper."' target='_blank'>".$scraper."</a>)"."</h2>";
                    buildTable($dataDecoded);
                }else{
                    //echo $dataDecoded->error;
                }
            }
        }
    }catch(Exception $e){
        //echo "There is no data for this manufacturer.<br/>";
    }
}

//print_r($data);

function buildTable($data){
    print "<table width='100%' style='margin:0 auto;text-align:left;'>";        
    print "<tr><th></th><th>Post</th><th>Synth</th><th>Item price</th><th>Item date</th>";
    foreach($data as $d){
        $imageSources = $d->post_item_images;
        print "<tr>";
        print "<td>";
        if(!empty($imageSources)){
            $imageSources = explode(',',$imageSources);
            foreach($imageSources as $imgSrc){
                print "<a href='".$d->link."' target='_blank' title='".$d->post_item_description."'><img src='".$imgSrc."' style='width: 150px; height: auto;max-height: 250px;'/></a>";
            }
        }
        print "&nbsp;</td>";
        //print "<td><a href='" . $d->post_item_link . "' target='_blank'>" . $d->post_item_link . "</a></td>";
        print "<td><a href='" . $d->link . "' target='_blank' title='".$d->post_item_description."'>". $d->post_item_name. "</a></td>";
        //print "<td>" . $d->manufacturer . "</td>";
        print "<td>" . $d->synth_name . "</td>";
        print "<td>" . $d->post_item_price . "</td>";
        print "<td>" . $d->post_item_date . "</td>";
        //print "<td><a href='" . $d->link . "' target='_blank'>".$d->link."</a></td>";
        print "</tr>";
    }
    print "</table>";
}
/*
function buildTable($data){
    print "<table width='100%' style='margin:0 auto;text-align:left;'>";        
    print "<tr><th></th><th>Post</th><th>Synth</th><th>Item price</th><th>Item date</th>";
    foreach($data as $d){
        $imageSources = $d['post_item_images'];
        print "<tr>";
        print "<td>";
        if(!empty($imageSources)){
            $imageSources = explode(',',$imageSources);
            foreach($imageSources as $imgSrc){
                print "<a href='".$d["link"]."' target='_blank' title='".$d["post_item_description"]."'><img src='".$imgSrc."' style='width: 150px; height: auto;max-height: 250px;'/></a>";
            }
        }
        print "&nbsp;</td>";
        //print "<td><a href='" . $d["post_item_link"] . "' target='_blank'>" . $d["post_item_link"] . "</a></td>";
        print "<td><a href='" . $d["link"] . "' target='_blank' title='".$d["post_item_description"]."'>". $d["post_item_name"] . "</a></td>";
        //print "<td>" . $d["manufacturer"] . "</td>";
        print "<td>" . $d["synth_name"] . "</td>";
        print "<td>" . $d["post_item_price"] . "</td>";
        print "<td>" . $d["post_item_date"] . "</td>";
        //print "<td><a href='" . $d["link"] . "' target='_blank'>".$d["link"]."</a></td>";
        print "</tr>";
    }
    print "</table>";
}*/
?>
<style type="text/css">
    body{
        font-family: sans-serif;
        color: #666666;
    }
    h1,h2,h3,h4,th {
        color: #000000;
    }
    a{
        color: #000000;
    }
</style>
<?php
/* Synth Manufacturers
"ARP","Access Music","Akai","Alesis","Analogue Systems","Applied Acoustics","Aries","Arturia","BOSS","BitHeadz","Bomb Factory Studios","Casio","Chamberlin","Cheetah","Chimera Synthesis","Clavia","Con Brio","Creamware","Crumar","Dave Smith Instruments","Doepfer","E-mu Systems","EDP","EML","EMS","Electrix Pro","Electro Harmonix","Elektron","Elka","Encore Electronics","Ensoniq","FBT Electronica","Fairlight","Farfisa","Formanta","Future Retro","GForce Software","Generalmusic","Gleeman","Hammond","Hartmann","Hohner","IK Multimedia","Image Line","Jen Electronics","JoMoX","Kawai","Kenton Electronics","KeyFax Hardware","Koblo","Korg","Kurzweil","Linn Electronics","Logan Electronics","MAM","MOTU","MacBeth Studio Systems","Marion Systems","Metasonix","Miscellaneous","Moog Music","Mutronics","Native Instruments","New England Digital","Novation","OSC","Oberheim","Octave","PAiA","PPG","Propellerheads","Prosoniq","Quasimidi","Red Sound Systems","Rhodes","Roland"
*/

$manufacturers = array("ARP","Access Music","Akai","Alesis","Analogue Systems","Applied Acoustics","Aries","Arturia","BOSS","BitHeadz","Bomb Factory Studios","Casio","Chamberlin","Cheetah","Chimera Synthesis","Clavia","Con Brio","Creamware","Crumar","Dave Smith Instruments","Doepfer","E-mu Systems","EDP","EML","EMS","Electrix Pro","Electro Harmonix","Elektron","Elka","Encore Electronics","Ensoniq","FBT Electronica","Fairlight","Farfisa","Formanta","Future Retro","GForce Software","Generalmusic","Gleeman","Hammond","Hartmann","Hohner","IK Multimedia","Image Line","Jen Electronics","JoMoX","Kawai","Kenton Electronics","KeyFax Hardware","Koblo","Korg","Kurzweil","Linn Electronics","Logan Electronics","MAM","MOTU","MacBeth Studio Systems","Marion Systems","Metasonix","Miscellaneous","Moog Music","Mutronics","Native Instruments","New England Digital","Novation","OSC","Oberheim","Octave","PAiA","PPG","Propellerheads","Prosoniq","Quasimidi","Red Sound Systems","Rhodes","Roland");

$ignored_manufacturers = array();
foreach($manufacturers as $manufacturer){
    if(!in_array($manufacturer,$ignored_manufacturers)){
        $tempName = "oregon_".strtolower(trim(str_replace(" ","_",$manufacturer)))."_craigslist_synth_scraper";
        if(strlen($tempName) > 50){
            $dif = strlen($tempName) - 50;
            //echo $dif."<br/>";
            $tempName = substr($tempName,0,-$dif);
        }
        //echo "DB Name: ".$tempName."<br/>";
        $scrapers[] = $tempName;
    }
}

print "<h1 align='center'>Synths found in <a href='http://geo.craigslist.org/iso/us/or' target='_blank'>Oregon</a> from Craigslist.</h1>";
foreach($scrapers as $scraper){
    //echo "Attaching DB: <a href='https://scraperwiki.com/scrapers/".$scraper."' target='_blank'>".$scraper."</a><br/>";
    try {
        $data = file_get_contents("https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=$scraper&query=select%20*%20from%20%60swdata%60");
        //print_r($data);
        /*scraperwiki::attach($scraper);
        $data = scraperwiki::select(           
            "* from $scraper.swdata order by post_item_date asc"
        );*/
        if(!empty($data)){
            $dataDecoded = json_decode($data);
            //print_r($dataDecoded);
            if(!empty($dataDecoded)){
                if(!isset($dataDecoded->error)){
                    print "<br/>";
                    print "<h2>".$dataDecoded[0]->manufacturer." (<a href='https://scraperwiki.com/scrapers/".$scraper."' target='_blank'>".$scraper."</a>)"."</h2>";
                    buildTable($dataDecoded);
                }else{
                    //echo $dataDecoded->error;
                }
            }
        }
    }catch(Exception $e){
        //echo "There is no data for this manufacturer.<br/>";
    }
}

//print_r($data);

function buildTable($data){
    print "<table width='100%' style='margin:0 auto;text-align:left;'>";        
    print "<tr><th></th><th>Post</th><th>Synth</th><th>Item price</th><th>Item date</th>";
    foreach($data as $d){
        $imageSources = $d->post_item_images;
        print "<tr>";
        print "<td>";
        if(!empty($imageSources)){
            $imageSources = explode(',',$imageSources);
            foreach($imageSources as $imgSrc){
                print "<a href='".$d->link."' target='_blank' title='".$d->post_item_description."'><img src='".$imgSrc."' style='width: 150px; height: auto;max-height: 250px;'/></a>";
            }
        }
        print "&nbsp;</td>";
        //print "<td><a href='" . $d->post_item_link . "' target='_blank'>" . $d->post_item_link . "</a></td>";
        print "<td><a href='" . $d->link . "' target='_blank' title='".$d->post_item_description."'>". $d->post_item_name. "</a></td>";
        //print "<td>" . $d->manufacturer . "</td>";
        print "<td>" . $d->synth_name . "</td>";
        print "<td>" . $d->post_item_price . "</td>";
        print "<td>" . $d->post_item_date . "</td>";
        //print "<td><a href='" . $d->link . "' target='_blank'>".$d->link."</a></td>";
        print "</tr>";
    }
    print "</table>";
}
/*
function buildTable($data){
    print "<table width='100%' style='margin:0 auto;text-align:left;'>";        
    print "<tr><th></th><th>Post</th><th>Synth</th><th>Item price</th><th>Item date</th>";
    foreach($data as $d){
        $imageSources = $d['post_item_images'];
        print "<tr>";
        print "<td>";
        if(!empty($imageSources)){
            $imageSources = explode(',',$imageSources);
            foreach($imageSources as $imgSrc){
                print "<a href='".$d["link"]."' target='_blank' title='".$d["post_item_description"]."'><img src='".$imgSrc."' style='width: 150px; height: auto;max-height: 250px;'/></a>";
            }
        }
        print "&nbsp;</td>";
        //print "<td><a href='" . $d["post_item_link"] . "' target='_blank'>" . $d["post_item_link"] . "</a></td>";
        print "<td><a href='" . $d["link"] . "' target='_blank' title='".$d["post_item_description"]."'>". $d["post_item_name"] . "</a></td>";
        //print "<td>" . $d["manufacturer"] . "</td>";
        print "<td>" . $d["synth_name"] . "</td>";
        print "<td>" . $d["post_item_price"] . "</td>";
        print "<td>" . $d["post_item_date"] . "</td>";
        //print "<td><a href='" . $d["link"] . "' target='_blank'>".$d["link"]."</a></td>";
        print "</tr>";
    }
    print "</table>";
}*/
?>
