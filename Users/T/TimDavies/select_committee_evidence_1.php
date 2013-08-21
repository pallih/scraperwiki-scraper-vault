<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';
$evidence_url = "http://www.publications.parliament.uk/pa/cm201011/cmselect/cmeduc/uc744-ii/uc74401.htm";
$yahoo_app_id = "fa05gqzV34Ek0FpP8c7JDF08DS0TEum2HRixVDcUE4yjHE0LjqwrOWHFxXMVj4JqKg--";

$html = scraperwiki::scrape($evidence_url);

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find("p.memberName") as $member) {
    $members[] = $member->plaintext;
}

foreach($dom->find(".ParaSingleLine") as $para) {
    if(stripos($para,"Witnesses")) {
        echo $para->plaintext;
        foreach($para->find("strong") as $witness) {
            $witnesses[] = $witness->plaintext;
        }
    }
}

scraperwiki::save(array('data'), array('n'=>'-1','speaker'=>'na', 'type'=>'details', 'data' => json_encode(array('members'=>$members,'witness'=>$witnesses))));


foreach($dom->find('p.Para, p.question, p.AnswerIndent') as $data)
{
    $type = $data->class == "question" ? "question" : "answer";
    if($speaker_data = $data->find("strong")) {
        $speaker = trim(str_replace(":","",$data->find("strong",0)->plaintext));
        if(preg_match("/Q[1-9]/",$speaker)) {
           $speaker = trim(str_replace(":","",$data->find("strong",1)->plaintext));
        }
    }

    $tags = json_decode(scraperwiki::scrape("http://search.yahooapis.com/ContentAnalysisService/V1/termExtraction?appid={$yahoo_app_id}&output=json&context=".urlencode($data->plaintext)));
    $tag_string = join("|",$tags->ResultSet->Result);

    $sentiment = json_decode(scraperwiki::scrape("http://twittersentiment.appspot.com/api/classify?text=".urlencode($data->plaintext)));
    $polarity = ($sentiment->results->polarity == 2) ? "Neutral" : (($sentiment->results->polarity == 4) ? "Positive" : "Negative");
    

    $speech = strip_tags(substr($data,strrpos($data,"</strong>")));  

    # Store data in the datastore
    print $data->plaintext . "\n";
    scraperwiki::save(array('data'), array('n'=>$n++,'speaker'=>$speaker, 'type'=> $type, 'data' => $speech,'tags'=>$tag_string,'polarity'=>$polarity));
}

?>