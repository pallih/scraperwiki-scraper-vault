<?php
require 'scraperwiki/simple_html_dom.php';

$manufacturers = array("Adaptive Systems", "Inc.", "Advanced Tools for the Arts (ATA)", "Akai", "Ampron", "Aries", "ARP", "Atlantex", "Boss", "Buchla", "Casio", "Con Brio", "CRB Elettronica", "Crumar", "Davoli", "Delta Music Research (DMR)", "Digisound", "Digital Keyboards", "Bruce Duncan's Modular", "Electro-Harmonix", "Electronic Dream Plant (EDP)", "Electronic Music Laboratories (EML)", "Electronic Music Studios (EMS)", "Elektor", "Elka", "E-mu", "Ensoniq", "Fairlight", "Firstman", "GDS", "Gray Laboratories", "Erik G", "Hammond", "Jen", "Kawai", "KineticSound", "Korg", "Kurzweil", "Linn Electronics", "McLeyvier", "Moog", "MPC Electronics", "Multivox", "MXR", "New England Digital", "Oberheim", "Octave", "Optigan", "PAiA", "pollard International", "Performance Music Systems", "Polyfusion", "Polyvox", "PPG", "Realistic (Radio Shack)", "RCA", "Rhodes", "Rocky Mount Instruments", "Roland", "Sequential Circuits", "Serge", "Solton", "Steiner-Parker", "Stramp", "Synclavier (New England Digital)", "Synergy", "Synton", "Technos", "Teisco", "Thomas Organ", "T.O.N.T.O.", "Triadex", "Univox", "Whitehall", "Wasatch Music Systems (WMS)", "Wurlitzer", "Yamaha");

//Delete existing data
$info = scraperwiki::table_info($name="swdata");
if(!empty($info)){
    scraperwiki::sqliteexecute("DELETE FROM swdata"); //Truncate the table before adding new results
}
           
//print $html . "\n";
$depth = 150; //Set the link depth (mostly for testing)
$sub_depth = 500;
$counter = 0; //To check the depth
$sub_counter = 0;
$testing = true; //Test variable activates the depth search

$html = scraperWiki::scrape("http://www.synthmuseum.com/sitemap.html");
$dom = new simple_html_dom();
$dom->load($html); //Load the HTML

$synths = array();
$counter = 0;
foreach($dom->find("center table tbody tr td[rowspan=12] font a") as $data){
    if(!empty($data->href)){
        $indexPageURL = "http://www.synthmuseum.com/".trim($data->href);

        $html2 = scraperWiki::scrape($indexPageURL);
        $dom2 = new simple_html_dom();
        $dom2->load($html2); //Load the HTML
        
        foreach($dom2->find("table[width=640] tbody tr td[width=120] font a") as $data2){
            $prevLinkURL = str_replace('index.html','',$indexPageURL);
            if(!empty($data2->href)){
                $synths[$counter]['manufacturer'] = trim($data->innertext);
                $data2->innertext = strip_tags($data2->innertext);
                echo $data2->innertext."\n";
                $synths[$counter]['name'] = trim($data2->innertext);
                $synths[$counter]['url'] = $prevLinkURL.trim($data2->href);
                $counter++;
            }else{
                //Scrape the synth names without links
                $sidebarContainer = $dom2->find("table[width=640] tbody tr td[width=120] font",0);
                if(!empty($sidebarContainer->innertext)){
                    $sideBarInnerText = trim($sidebarContainer->innertext);
                    $sideBarInnerText = preg_replace('/<\!--.*-->/','',$sideBarInnerText);
                    $sideBarInnerText = trim($sideBarInnerText);
                    $sideBarInnerText = preg_replace('/<b>.*<\/b>/','',$sideBarInnerText);
                    $sideBarInnerText = strip_tags($sideBarInnerText,"<br>"); //Strip HTML Tags
                    $sideBarInnerText = preg_replace('/>\s+/','>',$sideBarInnerText);
                    $sideBarInnerText = preg_replace('/<br.*>/',',',$sideBarInnerText);
                    $sideBarInnerText = strip_tags($sideBarInnerText);
                    $sideBarInnerText = preg_replace('/<*.>/',' ',$sideBarInnerText);
                    $sideBarInnerText = preg_replace('/&nbsp;+/',' ',$sideBarInnerText);
                    $sideBarInnerText = preg_replace('/<[a-z][a-z]+>/',' ',$sideBarInnerText);
                    $sideBarInnerText = trim($sideBarInnerText);
                    $sideBarInnerText = preg_replace('/\,$/','',$sideBarInnerText);
                    if(!empty($sideBarInnerText)){
                        if($sideBarInnerText[0] == ","){ 
                            $sideBarInnerText[0] = "";
                        }
                    }
                    echo $sideBarInnerText."\n";
                    //echo strlen($sideBarInnerText)."\n";
                    if(strlen($sideBarInnerText) > 1){
                        $sideBarInnerTextArray = explode(',',$sideBarInnerText);
                        foreach($sideBarInnerTextArray as $sythName){
                            $synths[$counter]['manufacturer'] = trim($data->innertext);
                            $synths[$counter]['name'] = trim($sythName);
                            $synths[$counter]['url'] = "";
                            $counter++;
                        }
                        //print_r($sideBarInnerTextArray);
                    }
                }
            }
        }
        

        //Scrape the description
        /*$description = "";
        foreach($dom2->find("table[width=640] td[width=505] p") as $par){
            $description .= $par->plaintext."<br/>";
        }
        foreach($dom2->find("table[width=640] td[width=505] blockquote") as $block){
            $description .= $block->plaintext."<br/>";
        }
        $description = preg_replace("/\[.*\]/","",$description);
        $description = preg_replace("/<br\/><br\/>+/","",$description);
        if(strlen($description) > 1){
            echo $description;
        }*/
    }
}



/*echo "<pre>";
print_r($synths);
echo "</pre>";*/

if(!empty($synths)){
    //$dbName = "vintagesynth-scrape-".$today = date("m-d-Y");
    $saveMessage = scraperWiki::save_sqlite(array('manufacturer','url'), $synths);
    //print strval($saveMessage);
    
    scraperwiki::save_var('total_results', count($synths));           
    print scraperWiki::get_var('total_results');
}

?>
<?php
require 'scraperwiki/simple_html_dom.php';

$manufacturers = array("Adaptive Systems", "Inc.", "Advanced Tools for the Arts (ATA)", "Akai", "Ampron", "Aries", "ARP", "Atlantex", "Boss", "Buchla", "Casio", "Con Brio", "CRB Elettronica", "Crumar", "Davoli", "Delta Music Research (DMR)", "Digisound", "Digital Keyboards", "Bruce Duncan's Modular", "Electro-Harmonix", "Electronic Dream Plant (EDP)", "Electronic Music Laboratories (EML)", "Electronic Music Studios (EMS)", "Elektor", "Elka", "E-mu", "Ensoniq", "Fairlight", "Firstman", "GDS", "Gray Laboratories", "Erik G", "Hammond", "Jen", "Kawai", "KineticSound", "Korg", "Kurzweil", "Linn Electronics", "McLeyvier", "Moog", "MPC Electronics", "Multivox", "MXR", "New England Digital", "Oberheim", "Octave", "Optigan", "PAiA", "pollard International", "Performance Music Systems", "Polyfusion", "Polyvox", "PPG", "Realistic (Radio Shack)", "RCA", "Rhodes", "Rocky Mount Instruments", "Roland", "Sequential Circuits", "Serge", "Solton", "Steiner-Parker", "Stramp", "Synclavier (New England Digital)", "Synergy", "Synton", "Technos", "Teisco", "Thomas Organ", "T.O.N.T.O.", "Triadex", "Univox", "Whitehall", "Wasatch Music Systems (WMS)", "Wurlitzer", "Yamaha");

//Delete existing data
$info = scraperwiki::table_info($name="swdata");
if(!empty($info)){
    scraperwiki::sqliteexecute("DELETE FROM swdata"); //Truncate the table before adding new results
}
           
//print $html . "\n";
$depth = 150; //Set the link depth (mostly for testing)
$sub_depth = 500;
$counter = 0; //To check the depth
$sub_counter = 0;
$testing = true; //Test variable activates the depth search

$html = scraperWiki::scrape("http://www.synthmuseum.com/sitemap.html");
$dom = new simple_html_dom();
$dom->load($html); //Load the HTML

$synths = array();
$counter = 0;
foreach($dom->find("center table tbody tr td[rowspan=12] font a") as $data){
    if(!empty($data->href)){
        $indexPageURL = "http://www.synthmuseum.com/".trim($data->href);

        $html2 = scraperWiki::scrape($indexPageURL);
        $dom2 = new simple_html_dom();
        $dom2->load($html2); //Load the HTML
        
        foreach($dom2->find("table[width=640] tbody tr td[width=120] font a") as $data2){
            $prevLinkURL = str_replace('index.html','',$indexPageURL);
            if(!empty($data2->href)){
                $synths[$counter]['manufacturer'] = trim($data->innertext);
                $data2->innertext = strip_tags($data2->innertext);
                echo $data2->innertext."\n";
                $synths[$counter]['name'] = trim($data2->innertext);
                $synths[$counter]['url'] = $prevLinkURL.trim($data2->href);
                $counter++;
            }else{
                //Scrape the synth names without links
                $sidebarContainer = $dom2->find("table[width=640] tbody tr td[width=120] font",0);
                if(!empty($sidebarContainer->innertext)){
                    $sideBarInnerText = trim($sidebarContainer->innertext);
                    $sideBarInnerText = preg_replace('/<\!--.*-->/','',$sideBarInnerText);
                    $sideBarInnerText = trim($sideBarInnerText);
                    $sideBarInnerText = preg_replace('/<b>.*<\/b>/','',$sideBarInnerText);
                    $sideBarInnerText = strip_tags($sideBarInnerText,"<br>"); //Strip HTML Tags
                    $sideBarInnerText = preg_replace('/>\s+/','>',$sideBarInnerText);
                    $sideBarInnerText = preg_replace('/<br.*>/',',',$sideBarInnerText);
                    $sideBarInnerText = strip_tags($sideBarInnerText);
                    $sideBarInnerText = preg_replace('/<*.>/',' ',$sideBarInnerText);
                    $sideBarInnerText = preg_replace('/&nbsp;+/',' ',$sideBarInnerText);
                    $sideBarInnerText = preg_replace('/<[a-z][a-z]+>/',' ',$sideBarInnerText);
                    $sideBarInnerText = trim($sideBarInnerText);
                    $sideBarInnerText = preg_replace('/\,$/','',$sideBarInnerText);
                    if(!empty($sideBarInnerText)){
                        if($sideBarInnerText[0] == ","){ 
                            $sideBarInnerText[0] = "";
                        }
                    }
                    echo $sideBarInnerText."\n";
                    //echo strlen($sideBarInnerText)."\n";
                    if(strlen($sideBarInnerText) > 1){
                        $sideBarInnerTextArray = explode(',',$sideBarInnerText);
                        foreach($sideBarInnerTextArray as $sythName){
                            $synths[$counter]['manufacturer'] = trim($data->innertext);
                            $synths[$counter]['name'] = trim($sythName);
                            $synths[$counter]['url'] = "";
                            $counter++;
                        }
                        //print_r($sideBarInnerTextArray);
                    }
                }
            }
        }
        

        //Scrape the description
        /*$description = "";
        foreach($dom2->find("table[width=640] td[width=505] p") as $par){
            $description .= $par->plaintext."<br/>";
        }
        foreach($dom2->find("table[width=640] td[width=505] blockquote") as $block){
            $description .= $block->plaintext."<br/>";
        }
        $description = preg_replace("/\[.*\]/","",$description);
        $description = preg_replace("/<br\/><br\/>+/","",$description);
        if(strlen($description) > 1){
            echo $description;
        }*/
    }
}



/*echo "<pre>";
print_r($synths);
echo "</pre>";*/

if(!empty($synths)){
    //$dbName = "vintagesynth-scrape-".$today = date("m-d-Y");
    $saveMessage = scraperWiki::save_sqlite(array('manufacturer','url'), $synths);
    //print strval($saveMessage);
    
    scraperwiki::save_var('total_results', count($synths));           
    print scraperWiki::get_var('total_results');
}

?>
