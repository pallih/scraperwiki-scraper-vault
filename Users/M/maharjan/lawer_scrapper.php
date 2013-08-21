<?php

$curlData = '<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><FindAttorneys xmlns="FCWSite.FCWSite.DlaPiperWS"><scFirstName></scFirstName><scLastName></scLastName><scKeyword></scKeyword><scOfficesGUID></scOfficesGUID><scSpokenLanguagesGUID></scSpokenLanguagesGUID><scServicesGUID></scServicesGUID><scRegionGUID>dc16cc3b-d65f-4cfe-b0c6-619bdf58325d</scRegionGUID><scSchoolGUID></scSchoolGUID><scAdmissionGUID></scAdmissionGUID><scLevelGUID></scLevelGUID><strLanguageGUID>7483b893-e478-44a4-8fed-f49aa917d8cf</strLanguageGUID><strCountry>us</strCountry><returnUntranslated>true</returnUntranslated><sortBy>name</sortBy><page>1</page></FindAttorneys></soap:Body></soap:Envelope>';
$url='http://www.dlapiper.com/FCWSite/DlaPiperWS/Attorneys.asmx?op=FindAttorneys';
$curl = curl_init();

curl_setopt ($curl, CURLOPT_URL, $url);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($curl,CURLOPT_TIMEOUT,120);
curl_setopt($curl,CURLOPT_ENCODING,'gzip');

curl_setopt($curl,CURLOPT_HTTPHEADER,array (
   
    'Content-Type: text/xml; charset=utf-8',
));

curl_setopt ($curl, CURLOPT_POST, 1);
curl_setopt ($curl, CURLOPT_POSTFIELDS, $curlData);

$result = curl_exec($curl);
curl_close ($curl);
echo $result;
?>
