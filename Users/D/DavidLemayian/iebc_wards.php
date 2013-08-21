<?php

$ward_data = array();

for ($i = 0; $i < 1451; $i++){
    
    $ward_raw = file_get_contents('http://api.iebc.or.ke/geojson/ward_'.$i.'.geojson');

    $ward_json = json_decode($ward_raw);

    $ward_data[$i] = array(
                        'ID' => $i,
                        'OBJECTID_1' => $ward_json->{'features'}[0]->{'properties'}->{'OBJECTID_1'},
                        'OBJECTID' => $ward_json->{'features'}[0]->{'properties'}->{'OBJECTID'},
                        'COUNTY_NAM' => $ward_json->{'features'}[0]->{'properties'}->{'COUNTY_NAM'},
                        'CONST_CODE' => $ward_json->{'features'}[0]->{'properties'}->{'CONST_CODE'},
                        'CONSTITUEN' => $ward_json->{'features'}[0]->{'properties'}->{'CONSTITUEN'},
                        'COUNTY_ASS' => $ward_json->{'features'}[0]->{'properties'}->{'COUNTY_ASS'},
                        'COUNTY_A_1' => $ward_json->{'features'}[0]->{'properties'}->{'COUNTY_A_1'},
                        'COUNTY_COD' => $ward_json->{'features'}[0]->{'properties'}->{'COUNTY_COD'},
                        'Shape_Leng' => $ward_json->{'features'}[0]->{'properties'}->{'Shape_Leng'},
                        'Shape_Le_1' => $ward_json->{'features'}[0]->{'properties'}->{'Shape_Le_1'},
                        'Shape_Area' => $ward_json->{'features'}[0]->{'properties'}->{'Shape_Area'},
                        'Geo_Type' => $ward_json->{'features'}[0]->{'geometry'}->{'type'},
                        'Raw_Data' => $ward_raw
                     );

}

scraperwiki::save(array('ID'), $ward_data);

?>
