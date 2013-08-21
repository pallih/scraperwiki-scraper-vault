<?php
$url = 'http://query.yahooapis.com/v1/public/yql?q=select%20content'.
'%20from%20search.termextract%20where%20context%20in'.
'%20(select%20content%20from%20html%20where%20url%3D%22'.
'http%3A%2F%2Fnews.bbc.co.uk%22%20and%20xpath%3D%22%2F%2F'.
'table%5B%40width%3D800%5D%2F%2Fa%22)&format=json';
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
$output = curl_exec($ch);
curl_close($ch);
$data = json_decode($output);
echo $data;
?>