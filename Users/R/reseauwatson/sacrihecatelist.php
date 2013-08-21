<?php

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, 'http://www.dofus.com/api/dofus/ladder.json');
curl_setopt($ch, CURLOPT_HEADER, 0);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, "{\"id\":320,\"method\":\"Ranking\",\"params\":{\"sOrder\":\"3D\",\"iBreed\":\"11\",\"iServer\":\"5\",\"sName\":\" Nom du personnage\",\"sLang\":\"fr\"}}");

$json = curl_exec($ch);
curl_close($ch);
$j = json_decode($json, true);
//var_dump($j);
//var_dump($j["result"]["ranking"][0]);
//echo $j->success->ranking[0];

foreach($j["result"]["ranking"] as $data){

        $record = array(
            'id' => $data["id"], 
            'kills' => intval($data["ki"]),
            'level' => intval($data["le"]),
            'xp' => $data["xp"],
            'name' => $data["na"],
            'server' => $data["hs"]
        );
        //print json_encode($record) . "\n";
        scraperwiki::save(array('id'), $record);
}

?>
