<?php
scraperwiki::attach("pcusa_church_data");
$Data = scraperwiki::select("* from pcusa");
$synData = scraperwiki::select("* from synods");
print "<h1>Presbyterian Church USA Statistics</h1>\n\r";
print("<table border=1>\n\r");
// PCUSA data
print("<tr style=\"font-weight:bold;\"><td>Synod</td><td>Pbys</td><td>Churches</td><td>Mbr 2000</td><td>Mbr 2010</td><td>Wor 2000</td><td>Wor 2010</td><td>Cont 2000</td><td>Cont 2010</td><td>Mem=0</td><td>1&gt;Mem&lt;99</td><td>100&gt;=Mem&lt;=250</td><td>250&gt;=Mem&lt;=500</td><td>Mem&gt;500</td></tr>\n\r");
  print "<tr><td><span style=\"font-weight:bold;\">PCUSA Syn:" . number_format($Data[0]["synods"]) . "</span></td>";
  print "<td>" . number_format($Data[0]["presbyteries"]) . "</td>";
  print "<td>" . number_format($Data[0]["churches"]) . "</td>";

  print "<td>" . number_format($Data[0]["m2000"]) . "</td>";
  print "<td>" . number_format($Data[0]["m2010"]) . "</td>";
  print "<td>" . number_format($Data[0]["w2000"]) . "</td>";
  print "<td>" . number_format($Data[0]["w2010"]) . "</td>";
  print "<td>$" . number_format($Data[0]["c2000"]) . "</td>";
  print "<td>$" . number_format($Data[0]["c2010"]) . "</td>";

// show church cnt and %total
  $diff = ($Data[0]["zero"] / $Data[0]["churches"]) * 100;
  print "<td>" . number_format($Data[0]["zero"]) . "(" . number_format($diff, 1) . "%)</td>";
  $diff = ($Data[0]["m100"] / $Data[0]["churches"]) * 100;
  print "<td>" . number_format($Data[0]["m100"]) . "(" . number_format($diff, 1) . "%)</td>";
  $diff = ($Data[0]["m250"] / $Data[0]["churches"]) * 100;
  print "<td>" . number_format($Data[0]["m250"]) . "(" . number_format($diff, 1) . "%)</td>";
  $diff = ($Data[0]["m500"] / $Data[0]["churches"]) * 100;
  print "<td>" . number_format($Data[0]["m500"]) . "(" . number_format($diff, 1) . "%)</td>";
  $diff = ($Data[0]["mbig"] / $Data[0]["churches"]) * 100;
  print "<td>" . number_format($Data[0]["mbig"]) . "(" . number_format($diff, 1) . "%)</td></tr>\n\r";

// show change %
  print "<tr><td>Change % / #Mbrs/size</td><td>&nbsp;</td><td>&nbsp;</td>";
  $diff = (($Data[0]["m2010"] - $Data[0]["m2000"]) / $Data[0]["m2000"]) * 100;
  print "<td>&nbsp;</td><td>" . number_format($diff, 1) . "%</td>";

  $diff = (($Data[0]["w2010"] - $Data[0]["w2000"]) / $Data[0]["w2000"]) * 100;
  print "<td>&nbsp;</td><td>" . number_format($diff, 1) . "%</td>";

  $diff = (($Data[0]["c2010"] - $Data[0]["c2000"]) / $Data[0]["c2000"]) * 100;
  print "<td>&nbsp;</td><td>" . number_format($diff, 1) . "%</td>";

// show #members in each size church
  print "<td>&nbsp;</td>";    // 0 cnt = 0%

  $diff = ($Data[0]["t100"] / $Data[0]["m2010"]) * 100;
  print "<td>" . number_format($Data[0]["t100"], 0). "(" . number_format($diff, 1) . "%)</td>";

  $diff = ($Data[0]["t250"] / $Data[0]["m2010"]) * 100;
  print "<td>" . number_format($Data[0]["t250"], 0). "(" . number_format($diff, 1) . "%)</td>";

  $diff = ($Data[0]["t500"] / $Data[0]["m2010"]) * 100;
  print "<td>" . number_format($Data[0]["t500"], 0). "(" . number_format($diff, 1) . "%)</td>";

  $diff = ($Data[0]["tbig"] / $Data[0]["m2010"]) * 100;
  print "<td>" . number_format($Data[0]["tbig"], 0) . "(" . number_format($diff, 1) . "%)</td>";
  print "</tr>\n\r";

// each synod data
$first = 1;
foreach($synData as $s){
  if ($first == 0)
    print("<tr style=\"font-weight:bold;\"><td>Synod</td><td>Pbys</td><td>Churches</td><td>Mbr 2000</td><td>Mbr 2010</td><td>Wor 2000</td><td>Wor 2010</td><td>Cont 2000</td><td>Cont 2010</td><td>Mem=0</td><td>1&gt;Mem&lt;99</td><td>100&gt;=Mem&lt;=250</td><td>250&gt;=Mem&lt;=500</td><td>Mem&gt;500</td></tr>\n\r");
  $first = 0;
  print "<tr><td><a href=\"" . $s["url"] . "\">" . $s["name"] . "</a>(". $s["syn_id"] . ")</td>\n";
  print "<td>" . number_format($s["pbys"]) . "</td>";
  print "<td>" . number_format($s["churches"]) . "</td>";

  print "<td>" . number_format($s["m2000"]) . "</td>";
  print "<td>" . number_format($s["m2010"]) . "</td>";

  print "<td>" . number_format($s["w2000"]) . "</td>";
  print "<td>" . number_format($s["w2010"]) . "</td>";

  print "<td>$" . number_format($s["c2000"]) . "</td>";
  print "<td>$" . number_format($s["c2010"]) . "</td>";

  print "<td>" . number_format($s["zero"]) . "</td>";
  print "<td>" . number_format($s["m100"]) . "</td>";
  print "<td>" . number_format($s["m250"]) . "</td>";
  print "<td>" . number_format($s["m500"]) . "</td>";
  print "<td>" . number_format($s["mbig"]) . "</td></tr>\n\r";
    $pbyData = scraperwiki::select("* from presbyteries where syn_id=" . $s["syn_id"]);
    foreach($pbyData as $pby)
    {
    print "<tr><td> </td><td><a href=\"" . $pby["URL"] . "\">" . $pby["name"] . "</a> (". $pby["pby_id"] . ")</td>";
    print "<td>" . number_format($pby["churches"]) . "</td>";

    print "<td>" . number_format($pby["m2000"]) . "</td>";
    print "<td>" . number_format($pby["m2010"]) . "</td>";
    print "<td>" . number_format($pby["w2000"]) . "</td>";
    print "<td>" . number_format($pby["w2010"]) . "</td>";
    print "<td>$" . number_format($pby["c2000"]) . "</td>";
    print "<td>$" . number_format($pby["c2010"]) . "</td>";

    print "<td>" . number_format($pby["zero"]) . "</td>";
    print "<td>" . number_format($pby["m100"]) . "</td>";
    print "<td>" . number_format($pby["m250"]) . "</td>";
    print "<td>" . number_format($pby["m500"]) . "</td>";
    print "<td>" . number_format($pby["mbig"]) . "</td></tr>\n\r";
    }
}
print "</table>\n\r";

?>
