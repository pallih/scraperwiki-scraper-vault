<?php
define('_SPOTIFY_TRACK_SEARCH_URL_','http://ws.spotify.com/search/1/track.json');
$checkNation = "FR";
$limit=200;
function getSpotifyTrackInfo( $q )
{
    $url = _SPOTIFY_TRACK_SEARCH_URL_.'?q='.urlencode($q);
   $json = json_decode(file_get_contents($url));
//   print_r($json);
return $json;
}


function cleanString($in,$offset=null)  
{ 
    $out = trim($in); 
    if (!empty($out)) 
    { 
        $entity_start = strpos($out,'&',$offset); 
        if ($entity_start === false) 
        { 
            // ideal 
            return $out;    
        } 
        else 
        { 
            $entity_end = strpos($out,';',$entity_start); 
            if ($entity_end === false) 
            { 
                 return $out; 
            } 
            // zu lang um eine entity zu sein 
            else if ($entity_end > $entity_start+7) 
            { 
                 // und weiter gehts 
                 $out = cleanString($out,$entity_start+1); 
            } 
            // gottcha! 
            else 
            { 
                 $clean = substr($out,0,$entity_start); 
                 $subst = substr($out,$entity_start+1,1); 
                 // &scaron; => "s" / &#353; => "_" 
                 $clean .= ($subst != "#") ? $subst : "_"; 
                 $clean .= substr($out,$entity_end+1); 
                 // und weiter gehts 
                 $out = cleanString($clean,$entity_start+1); 
            } 
        } 
    } 
    return $out; 
} 

$html = scraperWiki::scrape("http://www.radio3.rai.it/dl/radio3/programmi/archivio/ContentSet-5a1cc629-e11e-4140-bd7e-1877c56b9436.html");           
require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
$urls = Array();
foreach($dom->find("a[@class='linkPuntata']") as $data){
    $urls[] = ($data->href);
}
$playlistProgr = 0;
echo "SCRAPE URLS:".sizeof($urls)."\n";
for($i=0; $i< sizeof($urls) AND $i < 15;$i++)
{

$html = scraperWiki::scrape('http://www.radio3.rai.it'.$urls[$i]);
echo "\nURL:".$urls[$i]."\n";
$dom->load($html);
$titolo = ($dom->find("h2[@class='titolo']", 0));
$internalProg =1;
$titparts = explode(' ', trim($titolo->plaintext));
$day = $titparts[ 0 ];
$dateelements = explode('/', $day);
$timestamp = $dateelements[2].str_pad($dateelements[1], 2, "0", STR_PAD_LEFT).str_pad($dateelements[0], 2, "0", STR_PAD_LEFT);
foreach($dom->find("div[@id='ContentHtml']") as $data){
     if($playlistProgr>=$limit)
                            {
                                break;
                            }
    foreach($data->find("span[style]") as $element)
    {
         if($playlistProgr>=$limit)
                            {
                                break;
                            }
        //$text = cleanString(html_entity_decode($element->plaintext));
        $text = str_replace("\n","",html_entity_decode($element->plaintext,ENT_QUOTES));
        $text = str_replace("&rsquo;","'",$text);
        $text = str_replace("&lsquo;","'",$text);
        $text = str_replace("&rdquo;",'"',$text);
        $text = str_replace("&ldquo;",'"',$text);
        $text = str_replace("&ndash;", '-',$text);

        if(strlen( trim($text)))
            {
               //  echo "text:".$text."\n";
                $parts = explode('-',$text);
                if(is_array($parts) AND sizeof($parts) >=2 )
                {
                    $label = isset($parts[1])?$parts[1]:''; 
                    $artist_record =  explode(', ', $parts[0]);
                    if(is_array($artist_record) AND sizeof($artist_record) >=2 )
                    {
                          list( $artist, $track ) = $artist_record;
                       // $artist = html_entity_decode($artist,ENT_QUOTES);
                        // $track = html_entity_decode($record,ENT_QUOTES);
                        //echo "DECODED: $track::$artist\n"; 
                        $json = getSpotifyTrackInfo($track.' '. $artist);
                        if(0 AND $json->info->num_results == 0)
                        {
                             $json = getSpotifyTrackInfo($track);
                        }
                        if($json->info->num_results > 0)
                        {
                            $track = $json->tracks[0];
                            //print_r($track);
                            $albumname = $track->album->name.' ('. $track->album->released.')';
                            $albumlink = $track->album->href;
                            $trackname = $track->name;
                            $artistname = $track->artists[0]->name;
                            $artistlink = $track->artists[0]->href;
                            $tracklink =  $track->href;
                          
                            echo $timestamp."#".$internalProg.'::'.$trackname.",".$artistname.":".$tracklink."\n";
                              //  $unique =
                           scraperwiki::save_sqlite(array("id", "track"),array("id"=>$timestamp.$internalProg, "date"=>$timestamp,"album"=>$albumname, "albumlink"=>$albumlink,"artist"=>$artistname,"artistlink"=>$artistlink,"track"=>$tracklink, "trackname"=>$trackname));   
                              $playlistProgr++;
                            $internalProg++;
                        }
                    }
               }
        
            }
    }
}

}

?>
