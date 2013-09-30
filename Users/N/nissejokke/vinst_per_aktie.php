<!doctype html>
<!-- paulirish.com/2008/conditional-stylesheets-vs-css-hacks-answer-neither/ -->
<!--[if lt IE 7]> <html class="no-js lt-ie9 lt-ie8 lt-ie7" lang="en"> <![endif]-->
<!--[if IE 7]>    <html class="no-js lt-ie9 lt-ie8" lang="en"> <![endif]-->
<!--[if IE 8]>    <html class="no-js lt-ie9" lang="en"> <![endif]-->
<!-- Consider adding a manifest.appcache: h5bp.com/d/Offline -->
<!--[if gt IE 8]><!--> <html class="no-js" lang="en"> <!--<![endif]-->
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">

  <title></title>
  <meta name="description" content="">

  <!-- Mobile viewport optimized: h5bp.com/viewport -->
  <meta name="viewport" content="width=device-width">

    <link rel="stylesheet" href="http://tablesorter.com/themes/blue/style.css" />

    <style type="text/css">

        table.tablesorter { width: auto; }
        table.tablesorter tbody td { min-width:150px; }

    </style>

  <link rel="stylesheet" href="css/style.css" />
    <script src="http://code.jquery.com/jquery-1.7.2.min.js"></script>
    <script src="http://tablesorter.com/__jquery.tablesorter.min.js"></script>


<script>

    $(document).ready(function() {
        $("table.tablesorter").tablesorter();
    });

</script>

</head>
<body>
  <header>

  </header>
  <div role="main">



<?php
# Blank PHP
$sourcescraper = 'bolagsinfo';

scraperwiki::attach($sourcescraper);           

$data = scraperwiki::select(           
    "vinst_per_aktie, rantabilitet_totalt_kapital, nettomarginal, omsattningstillvaxt, bolag, ar  
from `swdata` 
order by bolag asc, ar desc"
);
//print_r($data);

$lastbolag = "";

print("<table class=\"tablesorter\">
        <thead>
            <tr>
                <th>Bolag</th>
                <th>VPA tillväxt per år</th>
                <th>Räntabilitet totalt kapital</th>
                <th title=\"senaste året\">Nettomarginal</th>
                <th>Omsättningstillväxt</th>
            <tr>
        <thead>
        <tbody>
");
foreach($data as $d){

  $bolag = $d["bolag"];
  if ($lastbolag == $bolag)
    continue;
  $lastbolag = $bolag;

  $barr = getItemsForCompany($data, $bolag);

  print "<tr>";
  print "<td>" . $bolag. "</td>";
  print "<td>" . getVinstOkning($barr, $bolag) . "</td>";
  print "<td>" . $d["rantabilitet_totalt_kapital"] . "</td>";
  print "<td>" . $d["nettomarginal"] . "</td>";
  print "<td>" . $d["omsattningstillvaxt"] . "</td>";
  print "</tr>\n";
}
print("</tbody></table>");

function getItemsForCompany($data, $bolag)
{
    $arr = array();
    $foundbolag = false;
    foreach($data as $d){
        if ($d["bolag"] == $bolag)
        {
            array_push($arr, $d);
            $foundbolag = true;
            
        }
        else if ($foundbolag == true)
            break;
    }

    return $arr;
}

function getVinstOkning($data, $bolag)
{
    $last = 0;
    $first = 0;
    $lastyear = 0;
    $firstyear = 0;
    $foundlatest = false;
    foreach($data as $d){

            if (!is_null($d["vinst_per_aktie"]) && $d["vinst_per_aktie"] != 0)
            {
                if (!$foundlatest)
                {
                    $last = $d["vinst_per_aktie"];
                    $lastyear = $d["ar"];
                    $foundlatest = true;
                }

                $first = $d["vinst_per_aktie"];
                $firstyear = $d["ar"];
            }
            
        

    }

//print($first . " " . $last);

    if ($first == 0 || $lastyear - $firstyear == 0)
        return "";
    //print($first . " * x^" . ($lastyear - $firstyear) . " = $last ");
    $v = xroot($last / $first, $lastyear - $firstyear) - 1;
    if (is_nan($v))
        return "";
    return round((float)$v * 100 ) . '%';
}

function xroot($value, $base)
{
    return pow($value, 1.0/$base);
}

?>

</div>
  <footer>

  </footer>


</body>
</html><!doctype html>
<!-- paulirish.com/2008/conditional-stylesheets-vs-css-hacks-answer-neither/ -->
<!--[if lt IE 7]> <html class="no-js lt-ie9 lt-ie8 lt-ie7" lang="en"> <![endif]-->
<!--[if IE 7]>    <html class="no-js lt-ie9 lt-ie8" lang="en"> <![endif]-->
<!--[if IE 8]>    <html class="no-js lt-ie9" lang="en"> <![endif]-->
<!-- Consider adding a manifest.appcache: h5bp.com/d/Offline -->
<!--[if gt IE 8]><!--> <html class="no-js" lang="en"> <!--<![endif]-->
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">

  <title></title>
  <meta name="description" content="">

  <!-- Mobile viewport optimized: h5bp.com/viewport -->
  <meta name="viewport" content="width=device-width">

    <link rel="stylesheet" href="http://tablesorter.com/themes/blue/style.css" />

    <style type="text/css">

        table.tablesorter { width: auto; }
        table.tablesorter tbody td { min-width:150px; }

    </style>

  <link rel="stylesheet" href="css/style.css" />
    <script src="http://code.jquery.com/jquery-1.7.2.min.js"></script>
    <script src="http://tablesorter.com/__jquery.tablesorter.min.js"></script>


<script>

    $(document).ready(function() {
        $("table.tablesorter").tablesorter();
    });

</script>

</head>
<body>
  <header>

  </header>
  <div role="main">



<?php
# Blank PHP
$sourcescraper = 'bolagsinfo';

scraperwiki::attach($sourcescraper);           

$data = scraperwiki::select(           
    "vinst_per_aktie, rantabilitet_totalt_kapital, nettomarginal, omsattningstillvaxt, bolag, ar  
from `swdata` 
order by bolag asc, ar desc"
);
//print_r($data);

$lastbolag = "";

print("<table class=\"tablesorter\">
        <thead>
            <tr>
                <th>Bolag</th>
                <th>VPA tillväxt per år</th>
                <th>Räntabilitet totalt kapital</th>
                <th title=\"senaste året\">Nettomarginal</th>
                <th>Omsättningstillväxt</th>
            <tr>
        <thead>
        <tbody>
");
foreach($data as $d){

  $bolag = $d["bolag"];
  if ($lastbolag == $bolag)
    continue;
  $lastbolag = $bolag;

  $barr = getItemsForCompany($data, $bolag);

  print "<tr>";
  print "<td>" . $bolag. "</td>";
  print "<td>" . getVinstOkning($barr, $bolag) . "</td>";
  print "<td>" . $d["rantabilitet_totalt_kapital"] . "</td>";
  print "<td>" . $d["nettomarginal"] . "</td>";
  print "<td>" . $d["omsattningstillvaxt"] . "</td>";
  print "</tr>\n";
}
print("</tbody></table>");

function getItemsForCompany($data, $bolag)
{
    $arr = array();
    $foundbolag = false;
    foreach($data as $d){
        if ($d["bolag"] == $bolag)
        {
            array_push($arr, $d);
            $foundbolag = true;
            
        }
        else if ($foundbolag == true)
            break;
    }

    return $arr;
}

function getVinstOkning($data, $bolag)
{
    $last = 0;
    $first = 0;
    $lastyear = 0;
    $firstyear = 0;
    $foundlatest = false;
    foreach($data as $d){

            if (!is_null($d["vinst_per_aktie"]) && $d["vinst_per_aktie"] != 0)
            {
                if (!$foundlatest)
                {
                    $last = $d["vinst_per_aktie"];
                    $lastyear = $d["ar"];
                    $foundlatest = true;
                }

                $first = $d["vinst_per_aktie"];
                $firstyear = $d["ar"];
            }
            
        

    }

//print($first . " " . $last);

    if ($first == 0 || $lastyear - $firstyear == 0)
        return "";
    //print($first . " * x^" . ($lastyear - $firstyear) . " = $last ");
    $v = xroot($last / $first, $lastyear - $firstyear) - 1;
    if (is_nan($v))
        return "";
    return round((float)$v * 100 ) . '%';
}

function xroot($value, $base)
{
    return pow($value, 1.0/$base);
}

?>

</div>
  <footer>

  </footer>


</body>
</html>