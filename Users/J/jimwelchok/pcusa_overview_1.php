<?php
# Blank PHP
$sourcescraper = '';
scraperwiki::attach("pcusa_church_data");
$Data = scraperwiki::select("* from pcusa");
$synData = scraperwiki::select("* from synods");
print("<ul id=\"pcusatree\">\n\r");
  print "<li><table border=1>\n\r<tr>";
  print "<td width=150>" . number_format($Data[0]["synods"]). "</td>";
  print "<td width=150>" . number_format($Data[0]["presbyteries"]). "</td>";
  print "<td width=100>" . number_format($Data[0]["churches"]). "</td>";
  print "<td width=100>" . number_format($Data[0]["members"]). "</td>";
  print "<td width=100>" . number_format($Data[0]["contribution"]). "</td>\n\r";
  print "<td width=100>" . number_format($Data[0]["zero"]). "</td>";
  print "<td width=100>" . number_format($Data[0]["m100"]). "</td>";
  print "<td width=100>" . number_format($Data[0]["m500"]). "</td>";
  print "<td width=100>" . number_format($Data[0]["mbig"]) . "</td>";
  print "</tr></table></li>\n\r";

foreach($synData as $s){
  print "<li><table border=1\n\r>";
  print "<tr><td width=100>Synod</td><td width=100>Presbytery</td><td width=100>Churches</td><td width=100>Members</td><td width=100>Contribution</td>";
  print "<td width=100>Mbr=0</td><td width=100>Mbr&lt;100</td><td width=100>Mbr&lt;500</td><td width=100>Mbr&gt;500</td></tr>\n\r";
  print "<td width=150><a href=\"" . $s["url"] . "\">" . $s["name"] . "</a></td>\n\r";
  print "<td width=150>" . number_format($synData[0]["pbys"]). "</td>";
  print "<td width=100>" . number_format($synData[0]["churches"]). "</td>";
  print "<td width=100>" . number_format($synData[0]["members"]). "</td>";
  print "<td width=100>" . number_format($synData[0]["contribution"]). "</td>\n\r";
  print "<td width=100>" . number_format($synData[0]["zero"]). "</td>";
  print "<td width=100>" . number_format($synData[0]["m100"]). "</td>";
  print "<td width=100>" . number_format($synData[0]["m500"]). "</td>";
  print "<td width=100>" . number_format($synData[0]["mbig"]) . "</td>";
  print "</tr></table></li>\n\r";
  print("<ul id=\"pcusatree\">\n\r");
    $pbyData = scraperwiki::select("* from presbyteries where syn_id=" . $s["syn_id"]);
    foreach($pbyData as $pby)
    {
    print "<li><table border=1>\n\r<tr>";
    print "<td width=150>&nbsp;</td>";
    print "<td width=150><a href=\"" . $pby["URL"] . "\">" . $pby["name"] . "</a></td>\n\r";
    print "<td width=100>" . number_format($pby["churches"]) . "</td>";
    print "<td width=100>" . number_format($pby["members"]) . "</td>";
    print "<td width=100>" . number_format($pby["contribution"]) . "</td>\n\r";
    print "<td width=100>" . number_format($pby["zero"]) . "</td>";
    print "<td width=100>" . number_format($pby["m100"]) . "</td>";
    print "<td width=100>" . number_format($pby["m500"]) . "</td>";
    print "<td width=100>" . number_format($pby["mbig"]) . "</td>";
    print "</tr></table></li>\n\r";
    }
  print("</ul>\n\r");
}
print("</ul>\n\r");

?>
