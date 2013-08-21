<?php
$sourcescraper = '';
scraperwiki::attach("pcusa_church_data");
//$Data = scraperwiki::select("* from pcusa");
$pby_id = 420548;
$pbyData = scraperwiki::select("* from presbyteries where pby_id=" . $pby_id);
print "<h1>Presbyterian Church USA Statistics</h1>";
print "<table border=1>\n\r";
foreach($pbyData as $pby){
    $synData = scraperwiki::select("* from synods where syn_id=" . $pby['syn_id']);
    print "<h2>Presbytery: <a href=\"" . $pby["URL"] . "\">" . $pby["name"] . "</a></h2>\n";
    print "<h2>Synod " . $synData[0]["syn_id"] . ": <a href=\"" . $synData[0]["url"] . "\">" . $synData[0]["name"] . "</a>". "</h2>\n";
    print("<tr><td>ID</td><td>Church</td><td>City, State</td><td>Zip</td><td>Mbr 2000</td><td>Mbr 2010</td><td>Cont2000</td><td>Cont2010</td><td>Wor2000</td><td>Wor2010</td></tr>\n\r");
    print "<tr>";
    print "<td>" . $pby["pby_id"] . "</td>";
    print "<td><b>Presbytery Totals</b></td>";
    print"<td>&nbsp;</td><td>&nbsp;</td>";
    print "<td>" . number_format($pby["m2000"]) . "</td>";
    print "<td>" . number_format($pby["m2010"]) . "</td>";
    print "<td>" . number_format($pby["c2000"]) . "</td>";
    print "<td>" . number_format($pby["c2010"]) . "</td>";
    print "<td>" . number_format($pby["w2000"]) . "</td>";
    print "<td>" . number_format($pby["w2010"]) . "</td>";
    print "</tr>\n\r";

    $chData = scraperwiki::select("* from churches where pby_id=" . $pby_id);
    foreach($chData as $church)
    {
    print "<tr>";
    print "<td>" . $church["church_id"] . "</td>";
    print "<td><a href=\"" . $church["url"] . "\">" . $church["name"] . "</a></td>";
    print "<td>" . $church["city"] . "," . $church["state"] . "</td>";
    print "<td>" . $church["zip_blob"] . "</td>";
    print "<td>" . number_format($church["m2000"]) . "</td>";
    print "<td>" . number_format($church["m2010"]) . "</td>";
    print "<td>" . number_format($church["c2000"]) . "</td>";
    print "<td>" . number_format($church["c2010"]) . "</td>";
    print "<td>" . number_format($church["w2000"]) . "</td>";
    print "<td>" . number_format($church["w2010"]) . "</td>";
    print "</tr>\n\r";
    }
}
print "</table>\n\r";

?>
