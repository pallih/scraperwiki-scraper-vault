<?php
# Blank PHP
scraperwiki::attach("lxml_jo_tut");
$lastdate = scraperwiki::select( "strftime('%d',Dateformat) FROM lxml_jo_tut.swdata WHERE rowid = (SELECT MAX(rowid) FROM lxml_jo_tut.swdata)" );
//print_r ($lastdate);
$nap = 1;
$nap_query = scraperwiki::select( "strftime('%d',Dateformat), strftime('%m',Dateformat), date(Dateformat),Datum, Dateformat,Nev,Text FROM lxml_jo_tut.swdata WHERE date(Dateformat) = (SELECT date(Dateformat,'-".$nap." day') FROM lxml_jo_tut.swdata WHERE rowid = (SELECT MAX(rowid) FROM lxml_jo_tut.swdata))" );
//print_r ($tegnap);



//$lastdate = scraperwiki::select( "Datum FROM lxml_jo_tut.swdata WHERE id = (SELECT MAX(id) FROM lxml_jo_tut.swdata)" );
//print ($nap_query["0"]["date(Dateformat)"]);

for ($nap = 0; $nap < 7; $nap++) {
    $results = scraperwiki::select( "Nev, count(Nev),date(Dateformat),Datum from lxml_jo_tut.swdata WHERE date(Dateformat) = (SELECT date(Dateformat,'-".$nap." day') FROM lxml_jo_tut.swdata WHERE rowid = (SELECT MAX(rowid) FROM lxml_jo_tut.swdata)) GROUP BY Nev ORDER BY Nev ASC" );
    $baseapi = "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=htmltable&name=lxml_jo_tut&query=select%20Datum%2CNev%2CText%20FROM%20%27swdata%27";
    $nevapi = "%20WHERE%20Nev%20LIKE%20%27";
    $datumapi = "%27%20AND%20date(Dateformat)%20%3D%20(SELECT%20date(Dateformat%2C%27-";
    $apiend = "%20day%27)%20FROM%20%27swdata%27%20WHERE%20rowid%20%3D%20(SELECT%20MAX(rowid)%20FROM%20%27swdata%27))";
    print "<table style=display:inline-table;>";
    print "<caption><a href=".$baseapi."".$nevapi."%".$datumapi."".$nap."" .$apiend.">".$results["0"]["date(Dateformat)"]."</a></caption>";
    print "<tr><th>Név</th><th>Poszt</th>";
    foreach($results as $d){
        print "<tr>";
        print "<td>" . $d["Nev"] . "</td>";
        print "<td><a href=".$baseapi."".$nevapi."".$d["Nev"]."".$datumapi."".$nap."" .$apiend. ">" . $d["count(Nev)"] . "</a></td>";
        print "</tr>"; }
    print "</table>";
}

/*
<a href="http://www.w3schools.com">Visit W3Schools</a>
https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=lxml_jo_tut&query=select%20Datum%2CNev%2CText%20from%20%60swdata%60%20

select Datum,Nev,Text from `swdata` WHERE Datum LIKE "01/07%" AND Nev="sorted"
https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=htmltable&name=lxml_jo_tut&query=select%20Datum%2CNev%2CText%20from%20%60swdata%60%20WHERE%20Datum%20LIKE%20%2201%2F07%25%22%20AND%20Nev%3D%22sorted%22%0A
*/

?><?php
# Blank PHP
scraperwiki::attach("lxml_jo_tut");
$lastdate = scraperwiki::select( "strftime('%d',Dateformat) FROM lxml_jo_tut.swdata WHERE rowid = (SELECT MAX(rowid) FROM lxml_jo_tut.swdata)" );
//print_r ($lastdate);
$nap = 1;
$nap_query = scraperwiki::select( "strftime('%d',Dateformat), strftime('%m',Dateformat), date(Dateformat),Datum, Dateformat,Nev,Text FROM lxml_jo_tut.swdata WHERE date(Dateformat) = (SELECT date(Dateformat,'-".$nap." day') FROM lxml_jo_tut.swdata WHERE rowid = (SELECT MAX(rowid) FROM lxml_jo_tut.swdata))" );
//print_r ($tegnap);



//$lastdate = scraperwiki::select( "Datum FROM lxml_jo_tut.swdata WHERE id = (SELECT MAX(id) FROM lxml_jo_tut.swdata)" );
//print ($nap_query["0"]["date(Dateformat)"]);

for ($nap = 0; $nap < 7; $nap++) {
    $results = scraperwiki::select( "Nev, count(Nev),date(Dateformat),Datum from lxml_jo_tut.swdata WHERE date(Dateformat) = (SELECT date(Dateformat,'-".$nap." day') FROM lxml_jo_tut.swdata WHERE rowid = (SELECT MAX(rowid) FROM lxml_jo_tut.swdata)) GROUP BY Nev ORDER BY Nev ASC" );
    $baseapi = "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=htmltable&name=lxml_jo_tut&query=select%20Datum%2CNev%2CText%20FROM%20%27swdata%27";
    $nevapi = "%20WHERE%20Nev%20LIKE%20%27";
    $datumapi = "%27%20AND%20date(Dateformat)%20%3D%20(SELECT%20date(Dateformat%2C%27-";
    $apiend = "%20day%27)%20FROM%20%27swdata%27%20WHERE%20rowid%20%3D%20(SELECT%20MAX(rowid)%20FROM%20%27swdata%27))";
    print "<table style=display:inline-table;>";
    print "<caption><a href=".$baseapi."".$nevapi."%".$datumapi."".$nap."" .$apiend.">".$results["0"]["date(Dateformat)"]."</a></caption>";
    print "<tr><th>Név</th><th>Poszt</th>";
    foreach($results as $d){
        print "<tr>";
        print "<td>" . $d["Nev"] . "</td>";
        print "<td><a href=".$baseapi."".$nevapi."".$d["Nev"]."".$datumapi."".$nap."" .$apiend. ">" . $d["count(Nev)"] . "</a></td>";
        print "</tr>"; }
    print "</table>";
}

/*
<a href="http://www.w3schools.com">Visit W3Schools</a>
https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=lxml_jo_tut&query=select%20Datum%2CNev%2CText%20from%20%60swdata%60%20

select Datum,Nev,Text from `swdata` WHERE Datum LIKE "01/07%" AND Nev="sorted"
https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=htmltable&name=lxml_jo_tut&query=select%20Datum%2CNev%2CText%20from%20%60swdata%60%20WHERE%20Datum%20LIKE%20%2201%2F07%25%22%20AND%20Nev%3D%22sorted%22%0A
*/

?>