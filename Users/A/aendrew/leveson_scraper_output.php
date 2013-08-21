<?php 
//thanks to my girlfriend Siyuan for helping with the colour combination!

function imageCacher($url, $name = NULL) {

    if (!fileexists(strtolower(str_replace(" ","_",$name)))) {
        
        $new_w = 100;
        $new_h = 100;

        $orig_w = imagesx($source_img);
        $orig_h = imagesy($source_img);

        $w_ratio = ($new_w / $orig_w);
        $h_ratio = ($new_h / $orig_h);

        if ($orig_w > $orig_h ) { //landscape
            $crop_w = round($orig_w * $h_ratio);
            $crop_h = $new_h;
            $src_x = ceil( ( $orig_w - $orig_h ) / 2 );
            $src_y = 0;
        } elseif ($orig_w < $orig_h ) { //portrait
            $crop_h = round($orig_h * $w_ratio);
            $crop_w = $new_w;
            $src_x = 0;
            $src_y = ceil( ( $orig_h - $orig_w ) / 2 );
        } else { //square
            $crop_w = $new_w;
            $crop_h = $new_h;
            $src_x = 0;
            $src_y = 0;
        }
        $dest_img = imagecreatetruecolor($new_w,$new_h);
        imagecopyresampled($dest_img, $source_img, 0 , 0 , $src_x, $src_y, $crop_w, $crop_h, $orig_w, $orig_h);

    }
}


function getFace($name){
    $people = array(
        'LORD JUSTICE LEVESON' => array('name' => 'Chief Lord Justice Leveson', 'url' => 'http://www.levesoninquiry.org.uk/wp-content/uploads/2011/11/LEVESON002resized.jpg'),
        'MR JAY' => array('name' => 'Robert Jay QC', 'url' => 'http://www.levesoninquiry.org.uk/wp-content/uploads/2011/11/Robert-Jay-QC.jpg'),
        'MR BARR' => array('name' => 'David Barr', 'url' => 'http://www.levesoninquiry.org.uk/wp-content/uploads/2011/11/Barr-David.jpg'),
        'MS PATRY HOSKINS' => array('name' => 'Carine Patry Hoskins', 'url' => 'http://www.levesoninquiry.org.uk/wp-content/uploads/2011/11/Patry-Hoskins-Carine1.jpg')
    );
    $name = (string) $name;
    if (@$people[$name]['url']) $url = $people[$name]['url']; else $url = NULL;
    if ($url) return '<img src="'.$url.'" />'; //imageCacher($url, $name); 
    else return '<img src="http://www.aendrew.com/files/unknown_user.gif" />';
}

scraperwiki::attach("leveson_inquiry_transcript_scraper");
if (@$_GET['raw'] == TRUE){
    $xmls = scraperwiki::sqliteexecute('SELECT * FROM `swdata`' . (@$_GET['date'] ? 'WHERE `date` = "'.$_GET['date'] .'"' : '') .' LIMIT 1;');
    scraperwiki::httpresponseheader('Content-Type', 'text/xml; charset=utf-8');
    foreach($xmls->data as $xml) {
    $xml[1] = preg_replace('/&(?![#]?[a-z0-9]+;)/i', "&amp;$1", $xml[1]);
        echo $xml[1];
    }
    exit();
}

$hearing_dates = scraperwiki::sqliteexecute('SELECT DISTINCT `date` from `swdata`;');
?>
<html>
    <head>
        <title>Leveson Inquiry Transcript Browser</title>
        <link href='https://fonts.googleapis.com/css?family=Kaushan+Script|Galdeano' rel='stylesheet' type='text/css'>
        <style type="text/css">
            <!-- 
                body {
                /* begin funky bg noize. For some great info: http://snook.ca/archives/html_and_css/multiple-bg-css-gradients */
                background-image: -webkit-gradient(linear, 0 top,  0 bottom, from(#fff), to(#666));
                background-image: -moz-linear-gradient(rgba(255,255,255,0), rgba(0,0,0,0));
                color: black;
                font-family: 'Galdeano', sans-serif;
                }       
                h1#title {font-size: 3em;}
                h1#title a {color: #ccc; text-decoration: none;}
                div.quote {width: 100%; padding: 10px 0px; clear: both;}
                div.speaker-left {width: 10%; float: left; margin-right: 5%; text-align: center;}
                div.speaker-right {width: 10%; float: right; margin-left: 5%; text-align: center;}            
                div.quote_text-left {width: 70%; float: left; opacity: 0.8; background: #CCFFFF; padding: 1%; border-radius: 10px; border: 1px solid black;}
                div.quote_text-right {width: 70%; float: right; opacity: 0.8; background: #99CCCC; padding: 1%; border-radius: 10px; border: 1px solid black;}
                div.event {width: 100%; text-align: center; padding: 10px 0px; clear: both;}
            -->
        </style>
    </head>
    <body>
    <h1 id="title">Simple Leveson Inquiry Testimony Viewer</h1>
    <h2>by <a href="http://www.aendrew.com">Ændrew Rininsland</a> (<a href="#">about</a>)</h2>
    <form method="post" action="#">
        Hearing date: <select name="hearing_select" onchange="window.open(this.options[this.selectedIndex].value,'_top')">
       <?php 
            foreach ($hearing_dates->data as $hearing_date) {
                echo("<option" . ($hearing_date[0] == @$_GET['date'] ? " selected " : '' ). " value='?date=$hearing_date[0]'>$hearing_date[0]</option>");
            }
        ?>
        </select>
        Search: 
        <input type="text" name="s" disabled />
        <input type="submit" disabled /> [<a href="#">?</a>]
    </form>
<?php
$xmls = scraperwiki::sqliteexecute('SELECT * FROM `swdata`' . (@$_GET['date'] ? 'WHERE `date` = "'.$_GET['date'] .'"' : 'LIMIT 1') .';');
foreach ($xmls->data as $xml) {
    $xml[1] = preg_replace('/&(?![#]?[a-z0-9]+;)/i', "&amp;$1", $xml[1]);
    $hearing = new SimpleXMLElement($xml[1]);
    $date = $hearing['date'];
    if (count($xmls->data) == 2 && @$second != TRUE) { //if more than one hearing, separate into morning and afternoon.
            $session = '(morning)';
            $second = TRUE;
        } else if (count($xmls->data) && @$second == TRUE) {
            $session = '(afternoon)';
        } else {
            $session = '';
        }

    echo "<h1>Testimony for: $date $session</h1>";
    foreach ($hearing as $key => $line) {
        if($line['type'] == 'quote' && $line != '') {
            echo('<div class="quote">');
            echo('<a name="Page'.$line['page'].'Line'.$line['line'].'" />');
            if ($line['speaker'] == 'A' && isset($a)) {
                $speaker = $a;

            } else if ($line['speaker'] == 'Q' && isset($q)) {
                $speaker = $q;
                $speaker['side'] = 'left';
            } else {
                $speaker = $line['speaker'];
            }
            if (@$set_next == TRUE) {
                $q = $line['speaker'];
                $set_next = FALSE;
            }
            
            if (($speaker == 'LORD JUSTICE LEVESON') || ($speaker == 'MR BARR') || ($speaker == 'MR JAY') || ($speaker == 'MS PATRY HOSKINS')) 
                $side = 'left'; 
            else 
                $side = 'right';
            echo('<div class="speaker-'.$side.'">'. getFace($speaker) . '<br />' . $speaker . '</div>');
            echo('<div class="quote_text-'.$side.'">'.$line.' <a href="#Page'.$line['page'].'Line'.$line['line'].'" title="Permalink to this quote">#</a></div>');
            echo('</div>');
        } else {
            if (preg_match('#(.*)\((sworn|recalled)\)#', $line, $matches) ) { 
                $a = $matches[1]; //set "a" speakers as the last person sworn in.
                $set_next = true;
            }
            echo('<div class="event">'.$line.'</div>');
        }
    }
}

?>
    </body>
</html>