<?php

function lbl_recyclebins_kml() {
    scraperwiki::sqliteexecute("drop table if exists r_kml");
    scraperwiki::sqlitecommit(); 
    scraperwiki::sqliteexecute("create table r_kml('kml' string)");
    scraperwiki::sqlitecommit();
    $data = scraperwiki::sqliteexecute("select * from r_locs");
    $keys = $data ->keys;
    $iaddress = array_search('address', $keys);
    $idesc = array_search('types', $keys);
    $ilatitude = array_search('latitude', $keys);
    $ilongitude = array_search('longitude', $keys);
    $kml = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>";
    $kml .= '<kml xmlns="http://www.opengis.net/kml/2.2">
      <Document>
        <name>Lambeth On-street Recycling Banks</name>
        <description><![CDATA[Information about recycling points available in Lambeth.]]></description>';
    foreach ($data ->data as $k => $row) {
        $kml.=  "
          <Placemark>
            <name>$row[$iaddress]</name>
            <description>$row[$idesc]</description>
            <Point>
              <coordinates>$row[$ilongitude],$row[$ilatitude],0</coordinates>
            </Point>
          </Placemark>";
    }
    $kml.=  '</Document>';
    $kml.=  '</kml>';
    scraperwiki::sqliteexecute("insert into r_kml values (:kml)", array($kml));
    scraperwiki::sqlitecommit(); 
    print_r($kml);
    return;
}

function lbl_recyclebins_types() {
    $descs = scraperwiki::sqliteexecute("select * from r_types");
    $keys = $descs->keys;
    $ikey = array_search('key', $keys);
    $idesc = array_search('desc', $keys);
    foreach ($descs->data as $k => $desc) {
        $result[$desc[$ikey]] = $desc[$idesc];
    }
    return $result;
}

function lbl_recyclebins_locs($dom) {
    scraperwiki::sqliteexecute("drop table if exists r_locs");
    scraperwiki::sqlitecommit(); 
    scraperwiki::sqliteexecute("create table r_locs ('address' string, 'types' string, 'latitude' string, 'longitude' string)");
    scraperwiki::sqlitecommit();
    $descs = lbl_recyclebins_types();
    foreach($dom->find("tr") as $id =>  $data){
        $tds = $data->find("td");    
        if (count($tds)) {
            $add = $tds[0]->plaintext;
            $tmp = explode(', ', $tds[1]->plaintext);
            $types = '';
            foreach ($tmp as $k => $v) {
                $types .= trim($descs[$v]) . "; ";
            }
            $lat = '';
            $lon = '';
            if ($i = preg_match('/([\w]{2}[\d]+\s\d[\w]{2})/', $add, $matches)) {
                if ($pcode = $matches[0]) {
                    try {
                        $geo = scraperwiki::gb_postcode_to_latlng($pcode);
                        $lat = $geo[0];
                        $lon = $geo[1];
                    } catch (Exception $e) {
                        print_r($e->getMessage());
                        $lat = '';
                        $lon = '';
                    }
                }
            }            
            scraperwiki::sqliteexecute("insert into r_locs values (:address,:types,:latitude,:longitude)", array($add, $types, $lat, $lon));
            scraperwiki::sqlitecommit();
        }
    }        
}

function lbl_recyclebins_refs($dom) {
    scraperwiki::sqliteexecute("drop table if exists r_types");
    $tmp = $dom->find("span#titlebox");
    if ($tmp) {
        $tmp = $tmp[0];
        print $tmp->innertext . "\n";
        $div = $tmp->parent()->parent();
        $tmp->__destruct();
        $uls = $div ->find("ul");
        $div->__destruct();
        $tmp = array();
        foreach ($uls[1]->children() as $k => $li) {
            $tmp = explode(" = ", $li->innertext);        
            if (!empty($tmp[0])) {
                $types[$k]['key'] = trim($tmp[0]);
                $types[$k]['desc'] = trim($tmp[1]);
            }
        }
        scraperwiki::save_sqlite(array('key', 'desc'), $types, "r_types", 2);
    }        
}

/*$html = scraperwiki::scrape('http://www.lambeth.gov.uk/Services/Environment/RubbishWasteRecycling/Recycling/LocalRecyclingPoints.htm');
require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);*/

//print_r(scraperwiki::show_tables());
//lbl_recyclebins_refs($dom);
//lbl_recyclebins_locs($dom);
//print_r(scraperwiki::sqliteexecute("select * from r_locs"));
//lbl_recyclebins_kml();

?>
<?php

function lbl_recyclebins_kml() {
    scraperwiki::sqliteexecute("drop table if exists r_kml");
    scraperwiki::sqlitecommit(); 
    scraperwiki::sqliteexecute("create table r_kml('kml' string)");
    scraperwiki::sqlitecommit();
    $data = scraperwiki::sqliteexecute("select * from r_locs");
    $keys = $data ->keys;
    $iaddress = array_search('address', $keys);
    $idesc = array_search('types', $keys);
    $ilatitude = array_search('latitude', $keys);
    $ilongitude = array_search('longitude', $keys);
    $kml = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>";
    $kml .= '<kml xmlns="http://www.opengis.net/kml/2.2">
      <Document>
        <name>Lambeth On-street Recycling Banks</name>
        <description><![CDATA[Information about recycling points available in Lambeth.]]></description>';
    foreach ($data ->data as $k => $row) {
        $kml.=  "
          <Placemark>
            <name>$row[$iaddress]</name>
            <description>$row[$idesc]</description>
            <Point>
              <coordinates>$row[$ilongitude],$row[$ilatitude],0</coordinates>
            </Point>
          </Placemark>";
    }
    $kml.=  '</Document>';
    $kml.=  '</kml>';
    scraperwiki::sqliteexecute("insert into r_kml values (:kml)", array($kml));
    scraperwiki::sqlitecommit(); 
    print_r($kml);
    return;
}

function lbl_recyclebins_types() {
    $descs = scraperwiki::sqliteexecute("select * from r_types");
    $keys = $descs->keys;
    $ikey = array_search('key', $keys);
    $idesc = array_search('desc', $keys);
    foreach ($descs->data as $k => $desc) {
        $result[$desc[$ikey]] = $desc[$idesc];
    }
    return $result;
}

function lbl_recyclebins_locs($dom) {
    scraperwiki::sqliteexecute("drop table if exists r_locs");
    scraperwiki::sqlitecommit(); 
    scraperwiki::sqliteexecute("create table r_locs ('address' string, 'types' string, 'latitude' string, 'longitude' string)");
    scraperwiki::sqlitecommit();
    $descs = lbl_recyclebins_types();
    foreach($dom->find("tr") as $id =>  $data){
        $tds = $data->find("td");    
        if (count($tds)) {
            $add = $tds[0]->plaintext;
            $tmp = explode(', ', $tds[1]->plaintext);
            $types = '';
            foreach ($tmp as $k => $v) {
                $types .= trim($descs[$v]) . "; ";
            }
            $lat = '';
            $lon = '';
            if ($i = preg_match('/([\w]{2}[\d]+\s\d[\w]{2})/', $add, $matches)) {
                if ($pcode = $matches[0]) {
                    try {
                        $geo = scraperwiki::gb_postcode_to_latlng($pcode);
                        $lat = $geo[0];
                        $lon = $geo[1];
                    } catch (Exception $e) {
                        print_r($e->getMessage());
                        $lat = '';
                        $lon = '';
                    }
                }
            }            
            scraperwiki::sqliteexecute("insert into r_locs values (:address,:types,:latitude,:longitude)", array($add, $types, $lat, $lon));
            scraperwiki::sqlitecommit();
        }
    }        
}

function lbl_recyclebins_refs($dom) {
    scraperwiki::sqliteexecute("drop table if exists r_types");
    $tmp = $dom->find("span#titlebox");
    if ($tmp) {
        $tmp = $tmp[0];
        print $tmp->innertext . "\n";
        $div = $tmp->parent()->parent();
        $tmp->__destruct();
        $uls = $div ->find("ul");
        $div->__destruct();
        $tmp = array();
        foreach ($uls[1]->children() as $k => $li) {
            $tmp = explode(" = ", $li->innertext);        
            if (!empty($tmp[0])) {
                $types[$k]['key'] = trim($tmp[0]);
                $types[$k]['desc'] = trim($tmp[1]);
            }
        }
        scraperwiki::save_sqlite(array('key', 'desc'), $types, "r_types", 2);
    }        
}

/*$html = scraperwiki::scrape('http://www.lambeth.gov.uk/Services/Environment/RubbishWasteRecycling/Recycling/LocalRecyclingPoints.htm');
require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);*/

//print_r(scraperwiki::show_tables());
//lbl_recyclebins_refs($dom);
//lbl_recyclebins_locs($dom);
//print_r(scraperwiki::sqliteexecute("select * from r_locs"));
//lbl_recyclebins_kml();

?>
