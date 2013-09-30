<?php

require 'scraperwiki/simple_html_dom.php';

$x = 1;
$arr = array(); 

//last: n=761
while($x<=10)
   {

$url = "http://www.puzzledragonx.com/en/monster.asp?n=".$x;

$html_content = scraperwiki::scrape($url);


$html = str_get_html($html_content);

$num = $html->find("td.title",0)->plaintext;
$mname = $html->find("td.value-end",1)->plaintext; 
$jname = $html->find("td.value-end",2)->plaintext;
$type = $html->find("td.value-end",3)->plaintext; 
$element = $html->find("td.value-end",4)->plaintext; 
$stars = $html->find("td.value-end",5)->plaintext; 
$cost = $html->find("td.value-end",6)->plaintext; 

$exp = $html->find("td.title",15)->plaintext;

//sometimes off
//$min = $html->find("td.value-end",9); 
//print $min->plaintext . "\n";

//$max = $html->find("td.value-end",10); 
//print $max->plaintext . "\n";

//$growth = $html->find("td.value-end",25); 
//print $growth->plaintext . "\n";


//$skill =  $html->find("span.blue",0); 
//print $skill->plaintext . "\n";

//$skilldesc = $html->find("td.nc",1); 
//print $skilldesc->plaintext . "\n";

//$effects =  $html->find("td.nc",0); 
//print $effects->plaintext . "\n";

//$cooldown =  $html->find("td.value-end",31); 
//print $cooldown->plaintext . "\n";

//$lskill =  $html->find("span.green",0); 
//print $lskill->plaintext . "\n";

//$ldesc =  $html->find("td.nc",3); 
//print $ldesc->plaintext . "\n";

//$leffects =  $html->find("td.nc",2); 
//print $leffects->plaintext . "\n";

//array_push($arr, $num,$mname,$jname,$stars,$element,$type,$cost,$exp);
$records = scraperwiki::save_sqlite(array("num","mname","jname","stars","element","type","cost","exp"), array("num"=>$num, "mname"=>$mname, "jname"=>$jname, "stars"=>$stars, "element"=>$element, "type"=>$type, "cost"=>$cost, "exp"=>$exp));


$x++;

}

?>
<?php

require 'scraperwiki/simple_html_dom.php';

$x = 1;
$arr = array(); 

//last: n=761
while($x<=10)
   {

$url = "http://www.puzzledragonx.com/en/monster.asp?n=".$x;

$html_content = scraperwiki::scrape($url);


$html = str_get_html($html_content);

$num = $html->find("td.title",0)->plaintext;
$mname = $html->find("td.value-end",1)->plaintext; 
$jname = $html->find("td.value-end",2)->plaintext;
$type = $html->find("td.value-end",3)->plaintext; 
$element = $html->find("td.value-end",4)->plaintext; 
$stars = $html->find("td.value-end",5)->plaintext; 
$cost = $html->find("td.value-end",6)->plaintext; 

$exp = $html->find("td.title",15)->plaintext;

//sometimes off
//$min = $html->find("td.value-end",9); 
//print $min->plaintext . "\n";

//$max = $html->find("td.value-end",10); 
//print $max->plaintext . "\n";

//$growth = $html->find("td.value-end",25); 
//print $growth->plaintext . "\n";


//$skill =  $html->find("span.blue",0); 
//print $skill->plaintext . "\n";

//$skilldesc = $html->find("td.nc",1); 
//print $skilldesc->plaintext . "\n";

//$effects =  $html->find("td.nc",0); 
//print $effects->plaintext . "\n";

//$cooldown =  $html->find("td.value-end",31); 
//print $cooldown->plaintext . "\n";

//$lskill =  $html->find("span.green",0); 
//print $lskill->plaintext . "\n";

//$ldesc =  $html->find("td.nc",3); 
//print $ldesc->plaintext . "\n";

//$leffects =  $html->find("td.nc",2); 
//print $leffects->plaintext . "\n";

//array_push($arr, $num,$mname,$jname,$stars,$element,$type,$cost,$exp);
$records = scraperwiki::save_sqlite(array("num","mname","jname","stars","element","type","cost","exp"), array("num"=>$num, "mname"=>$mname, "jname"=>$jname, "stars"=>$stars, "element"=>$element, "type"=>$type, "cost"=>$cost, "exp"=>$exp));


$x++;

}

?>
<?php

require 'scraperwiki/simple_html_dom.php';

$x = 1;
$arr = array(); 

//last: n=761
while($x<=10)
   {

$url = "http://www.puzzledragonx.com/en/monster.asp?n=".$x;

$html_content = scraperwiki::scrape($url);


$html = str_get_html($html_content);

$num = $html->find("td.title",0)->plaintext;
$mname = $html->find("td.value-end",1)->plaintext; 
$jname = $html->find("td.value-end",2)->plaintext;
$type = $html->find("td.value-end",3)->plaintext; 
$element = $html->find("td.value-end",4)->plaintext; 
$stars = $html->find("td.value-end",5)->plaintext; 
$cost = $html->find("td.value-end",6)->plaintext; 

$exp = $html->find("td.title",15)->plaintext;

//sometimes off
//$min = $html->find("td.value-end",9); 
//print $min->plaintext . "\n";

//$max = $html->find("td.value-end",10); 
//print $max->plaintext . "\n";

//$growth = $html->find("td.value-end",25); 
//print $growth->plaintext . "\n";


//$skill =  $html->find("span.blue",0); 
//print $skill->plaintext . "\n";

//$skilldesc = $html->find("td.nc",1); 
//print $skilldesc->plaintext . "\n";

//$effects =  $html->find("td.nc",0); 
//print $effects->plaintext . "\n";

//$cooldown =  $html->find("td.value-end",31); 
//print $cooldown->plaintext . "\n";

//$lskill =  $html->find("span.green",0); 
//print $lskill->plaintext . "\n";

//$ldesc =  $html->find("td.nc",3); 
//print $ldesc->plaintext . "\n";

//$leffects =  $html->find("td.nc",2); 
//print $leffects->plaintext . "\n";

//array_push($arr, $num,$mname,$jname,$stars,$element,$type,$cost,$exp);
$records = scraperwiki::save_sqlite(array("num","mname","jname","stars","element","type","cost","exp"), array("num"=>$num, "mname"=>$mname, "jname"=>$jname, "stars"=>$stars, "element"=>$element, "type"=>$type, "cost"=>$cost, "exp"=>$exp));


$x++;

}

?>
<?php

require 'scraperwiki/simple_html_dom.php';

$x = 1;
$arr = array(); 

//last: n=761
while($x<=10)
   {

$url = "http://www.puzzledragonx.com/en/monster.asp?n=".$x;

$html_content = scraperwiki::scrape($url);


$html = str_get_html($html_content);

$num = $html->find("td.title",0)->plaintext;
$mname = $html->find("td.value-end",1)->plaintext; 
$jname = $html->find("td.value-end",2)->plaintext;
$type = $html->find("td.value-end",3)->plaintext; 
$element = $html->find("td.value-end",4)->plaintext; 
$stars = $html->find("td.value-end",5)->plaintext; 
$cost = $html->find("td.value-end",6)->plaintext; 

$exp = $html->find("td.title",15)->plaintext;

//sometimes off
//$min = $html->find("td.value-end",9); 
//print $min->plaintext . "\n";

//$max = $html->find("td.value-end",10); 
//print $max->plaintext . "\n";

//$growth = $html->find("td.value-end",25); 
//print $growth->plaintext . "\n";


//$skill =  $html->find("span.blue",0); 
//print $skill->plaintext . "\n";

//$skilldesc = $html->find("td.nc",1); 
//print $skilldesc->plaintext . "\n";

//$effects =  $html->find("td.nc",0); 
//print $effects->plaintext . "\n";

//$cooldown =  $html->find("td.value-end",31); 
//print $cooldown->plaintext . "\n";

//$lskill =  $html->find("span.green",0); 
//print $lskill->plaintext . "\n";

//$ldesc =  $html->find("td.nc",3); 
//print $ldesc->plaintext . "\n";

//$leffects =  $html->find("td.nc",2); 
//print $leffects->plaintext . "\n";

//array_push($arr, $num,$mname,$jname,$stars,$element,$type,$cost,$exp);
$records = scraperwiki::save_sqlite(array("num","mname","jname","stars","element","type","cost","exp"), array("num"=>$num, "mname"=>$mname, "jname"=>$jname, "stars"=>$stars, "element"=>$element, "type"=>$type, "cost"=>$cost, "exp"=>$exp));


$x++;

}

?>
