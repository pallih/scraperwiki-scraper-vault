<?php
require 'scraperwiki/simple_html_dom.php';
$council = "Clare County Council";
$uri = "http://www.clarecoco.ie/your-council/contact-the-council/councillors/";
# eg http://www.clarecoco.ie/your-council/contact-the-council/councillors/ennis-west/
$subpages = array(
"ennis-east",
"ennis-west",
"ennistymon",
"killaloe",
"kilrush",
"shannon"
    );
function trim_value(&$value) 
{ 
    $value = trim($value); 
}
foreach($subpages as $subpage) {
    $dom = new simple_html_dom();
    $html = scraperwiki::scrape($uri . $subpage . "/");
    $dom->load($html);

    $rows=$dom->find("ul[class=azDetails] li");

foreach($rows as $row) {
    $nameparty = $row->find("h2",0);
    $nameparty = explode("-",$nameparty);
    $name = trim(strip_tags(str_replace("Councillor","",$nameparty[0])));
    $party = trim(strip_tags($nameparty[1]));
//$party = html_entity_decode($party);
//htmlspecialchars_decode($party);
//iconv("ISO-8859-1", "UTF-8", $party); //iso-8859-1
//$party = str_replace("FÃ¡il","Fail",$party);
print $party; // can't find right way to convert FÃ¡il
//utf8_decode($party);
//$party = uchiberno($party);
$party = preg_replace( '`&([a-z]+)(acute|uml|circ|grave|ring|cedil|slash|tilde|caron|lig);`i',"\\1", $party );
    $alldetails = explode("<br/>",$row);

    $detailslength = count($alldetails);
$emailcell = $row->find("a",0);

    $imagecell = $row->find("img",0);
    $image = "http://www.clarecoco.ie" .$imagecell->src;

    $phonecell = $alldetails[$detailslength-5];
    $mobilecell = $alldetails[$detailslength-4];
//    $emailcell = $alldetails[$detailslength-3];

   if($detailslength === 12) {
   
        $addresscell = $alldetails[1] . $alldetails[2] . $alldetails[3] . $alldetails[4] . $alldetails[5];    
}
    elseif($detailslength === 11) {

        $addresscell = $alldetails[1] . $alldetails[2] . $alldetails[3] . $alldetails[4];  
    }
    elseif($detailslength === 10) {

        $addresscell = $alldetails[1] . $alldetails[2] . $alldetails[3];   
    }
    elseif($detailslength === 9) 
    {
        $addresscell = $alldetails[1] . $alldetails[2];   
    }
    else 
    {

        $phonecell = $alldetails[4];
        $mobilecell = $alldetails[5];
  //      $emailcell = "";
        $addresscell = $alldetails[1] . $alldetails[2] . $alldetails[3];      
}

    $address = str_replace(",",", ",$addresscell);

    $phone = trim(str_replace("("," ",str_replace(")"," ",str_replace("Telephone:","",$phonecell))));

    $mobile = trim(str_replace("("," ",str_replace(")"," ",str_replace("Mobile:","",$mobilecell))));

    $email = trim(str_replace("Email:","",strip_tags($emailcell))); #->src;

    $lea = ucfirst(str_replace("-"," ",$subpage));


        $councillors["$name"] = array(
            "LEA"     => $lea,
            "Party"   => $party,
            "Email"   => $email,
            "Phone"   => $phone,
            "Mobile"  => $mobile,
            "Image"   => $image,
            "Address" => $address
        );
    }
}
scraperwiki::sqliteexecute("create table if not exists councillors (`auth` string, `lea` string, `name` string, `party` string, `email` string, `phone` text, `mobile` text, `image` string,  `address` string)");
scraperwiki::sqliteexecute("delete from councillors");
foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:auth, :lea, :name, :party, :email, :phone, :mobile, :image, :address)", 
            array(  "auth"    => "Clare County Council", 
                    "lea"     => $values["LEA"],
                    "name"    => $name,
                    "party"   => $values["Party"],
                    "email"   => $values["Email"],
                    "phone"   => $values["Phone"],
                    "mobile"  => $values["Mobile"],
                    "image"   => $values["Image"],
                    "address" => $values["Address"],
            )
    );
}


function uchiberno($str)
{
    $strUPPER = strtolower($str);
    $str = ucwords($strUPPER);

    // Not perfect dyer85 http://php.net/manual/en/function.ucwords.php
    return preg_replace(
        '/
            (?: ^ | \\b )         # assertion: beginning of string or a word boundary
            ( O\' | Ma?c | Fitz)  # attempt to match Irish surnames
            ( [^\W\d_] )          # match next char; we exclude digits and _ from \w
        /xe',
        "'\$1' . strtoupper('\$2')",
        $str);
}


scraperwiki::sqlitecommit();
?><?php
require 'scraperwiki/simple_html_dom.php';
$council = "Clare County Council";
$uri = "http://www.clarecoco.ie/your-council/contact-the-council/councillors/";
# eg http://www.clarecoco.ie/your-council/contact-the-council/councillors/ennis-west/
$subpages = array(
"ennis-east",
"ennis-west",
"ennistymon",
"killaloe",
"kilrush",
"shannon"
    );
function trim_value(&$value) 
{ 
    $value = trim($value); 
}
foreach($subpages as $subpage) {
    $dom = new simple_html_dom();
    $html = scraperwiki::scrape($uri . $subpage . "/");
    $dom->load($html);

    $rows=$dom->find("ul[class=azDetails] li");

foreach($rows as $row) {
    $nameparty = $row->find("h2",0);
    $nameparty = explode("-",$nameparty);
    $name = trim(strip_tags(str_replace("Councillor","",$nameparty[0])));
    $party = trim(strip_tags($nameparty[1]));
//$party = html_entity_decode($party);
//htmlspecialchars_decode($party);
//iconv("ISO-8859-1", "UTF-8", $party); //iso-8859-1
//$party = str_replace("FÃ¡il","Fail",$party);
print $party; // can't find right way to convert FÃ¡il
//utf8_decode($party);
//$party = uchiberno($party);
$party = preg_replace( '`&([a-z]+)(acute|uml|circ|grave|ring|cedil|slash|tilde|caron|lig);`i',"\\1", $party );
    $alldetails = explode("<br/>",$row);

    $detailslength = count($alldetails);
$emailcell = $row->find("a",0);

    $imagecell = $row->find("img",0);
    $image = "http://www.clarecoco.ie" .$imagecell->src;

    $phonecell = $alldetails[$detailslength-5];
    $mobilecell = $alldetails[$detailslength-4];
//    $emailcell = $alldetails[$detailslength-3];

   if($detailslength === 12) {
   
        $addresscell = $alldetails[1] . $alldetails[2] . $alldetails[3] . $alldetails[4] . $alldetails[5];    
}
    elseif($detailslength === 11) {

        $addresscell = $alldetails[1] . $alldetails[2] . $alldetails[3] . $alldetails[4];  
    }
    elseif($detailslength === 10) {

        $addresscell = $alldetails[1] . $alldetails[2] . $alldetails[3];   
    }
    elseif($detailslength === 9) 
    {
        $addresscell = $alldetails[1] . $alldetails[2];   
    }
    else 
    {

        $phonecell = $alldetails[4];
        $mobilecell = $alldetails[5];
  //      $emailcell = "";
        $addresscell = $alldetails[1] . $alldetails[2] . $alldetails[3];      
}

    $address = str_replace(",",", ",$addresscell);

    $phone = trim(str_replace("("," ",str_replace(")"," ",str_replace("Telephone:","",$phonecell))));

    $mobile = trim(str_replace("("," ",str_replace(")"," ",str_replace("Mobile:","",$mobilecell))));

    $email = trim(str_replace("Email:","",strip_tags($emailcell))); #->src;

    $lea = ucfirst(str_replace("-"," ",$subpage));


        $councillors["$name"] = array(
            "LEA"     => $lea,
            "Party"   => $party,
            "Email"   => $email,
            "Phone"   => $phone,
            "Mobile"  => $mobile,
            "Image"   => $image,
            "Address" => $address
        );
    }
}
scraperwiki::sqliteexecute("create table if not exists councillors (`auth` string, `lea` string, `name` string, `party` string, `email` string, `phone` text, `mobile` text, `image` string,  `address` string)");
scraperwiki::sqliteexecute("delete from councillors");
foreach ($councillors as $name => $values) {
    scraperwiki::sqliteexecute("insert or replace into councillors values (:auth, :lea, :name, :party, :email, :phone, :mobile, :image, :address)", 
            array(  "auth"    => "Clare County Council", 
                    "lea"     => $values["LEA"],
                    "name"    => $name,
                    "party"   => $values["Party"],
                    "email"   => $values["Email"],
                    "phone"   => $values["Phone"],
                    "mobile"  => $values["Mobile"],
                    "image"   => $values["Image"],
                    "address" => $values["Address"],
            )
    );
}


function uchiberno($str)
{
    $strUPPER = strtolower($str);
    $str = ucwords($strUPPER);

    // Not perfect dyer85 http://php.net/manual/en/function.ucwords.php
    return preg_replace(
        '/
            (?: ^ | \\b )         # assertion: beginning of string or a word boundary
            ( O\' | Ma?c | Fitz)  # attempt to match Irish surnames
            ( [^\W\d_] )          # match next char; we exclude digits and _ from \w
        /xe',
        "'\$1' . strtoupper('\$2')",
        $str);
}


scraperwiki::sqlitecommit();
?>