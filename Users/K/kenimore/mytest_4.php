<?php

require 'scraperwiki/simple_html_dom.php'; 
$html_content = scraperwiki::scrape("http://dota2.com/international/prelims/schedule/sunday/");
$html = str_get_html($html_content);
$data['id']=0;

foreach ($html->find("div.sgrMatch a") as $el) {           
    $html_orig = "http://dota2.com/international/gamesummary/" . substr($el->href,-3) . "?l=english"; 
    $game_id = substr($el->href,-3);
    $html_content = scraperwiki::scrape($html_orig);
    $html_final = str_get_html($html_content);
    
/*
    foreach ($html_final->find("div.pn") as $eli) {
        $data['name'] =  $eli->plaintext;
        print $data['name']. "\n";}
*/
    for ($i=0; $i<=9; $i++) {
        $data['id']++;
        $data['name'] = $html_final->find("div.pn",$i)->plaintext;
        $data['hero'] = $html_final->find("div.pcc",$i)->plaintext;
        $data['kda'] = $html_final->find("div.pkda",$i)->plaintext;
        preg_match_all('/\d+/', $data['kda'], $kda);
        $data['kills'] = (int) $kda[0][0];
        $data['deaths'] = (int) $kda[0][1];
        $data['assists'] = (int) $kda[0][2];
        $data['gpm'] = (int) $html_final->find("div.pgm",$i)->plaintext;
        $data['xpm'] = (int) $html_final->find("div.pxm",$i)->plaintext;
        $data['game_id'] = $game_id;
        if ($i<=4) {$data['team'] = $html_final->find("div.tn",0)->plaintext;} else {$data['team'] = $html_final->find("div.tn",1)->plaintext;}
        scraperwiki::save_sqlite(array("id"), array("id"=>$data['id'], "name"=>$data['name'], "hero"=>$data['hero'], "kills"=>$data['kills'], "deaths"=>$data['deaths'], "assists"=>$data['assists'], "gpm"=>$data['gpm'], "xpm"=>$data['xpm'], "game_id"=>$data['game_id'], "team"=>$data['team'] ),$table_name="game_id");
    }

}

?>
<?php

require 'scraperwiki/simple_html_dom.php'; 
$html_content = scraperwiki::scrape("http://dota2.com/international/prelims/schedule/sunday/");
$html = str_get_html($html_content);
$data['id']=0;

foreach ($html->find("div.sgrMatch a") as $el) {           
    $html_orig = "http://dota2.com/international/gamesummary/" . substr($el->href,-3) . "?l=english"; 
    $game_id = substr($el->href,-3);
    $html_content = scraperwiki::scrape($html_orig);
    $html_final = str_get_html($html_content);
    
/*
    foreach ($html_final->find("div.pn") as $eli) {
        $data['name'] =  $eli->plaintext;
        print $data['name']. "\n";}
*/
    for ($i=0; $i<=9; $i++) {
        $data['id']++;
        $data['name'] = $html_final->find("div.pn",$i)->plaintext;
        $data['hero'] = $html_final->find("div.pcc",$i)->plaintext;
        $data['kda'] = $html_final->find("div.pkda",$i)->plaintext;
        preg_match_all('/\d+/', $data['kda'], $kda);
        $data['kills'] = (int) $kda[0][0];
        $data['deaths'] = (int) $kda[0][1];
        $data['assists'] = (int) $kda[0][2];
        $data['gpm'] = (int) $html_final->find("div.pgm",$i)->plaintext;
        $data['xpm'] = (int) $html_final->find("div.pxm",$i)->plaintext;
        $data['game_id'] = $game_id;
        if ($i<=4) {$data['team'] = $html_final->find("div.tn",0)->plaintext;} else {$data['team'] = $html_final->find("div.tn",1)->plaintext;}
        scraperwiki::save_sqlite(array("id"), array("id"=>$data['id'], "name"=>$data['name'], "hero"=>$data['hero'], "kills"=>$data['kills'], "deaths"=>$data['deaths'], "assists"=>$data['assists'], "gpm"=>$data['gpm'], "xpm"=>$data['xpm'], "game_id"=>$data['game_id'], "team"=>$data['team'] ),$table_name="game_id");
    }

}

?>
