<?php
$db = "DATABASE NAME";
$admin = "MYSQL USER NAME";
$adpass = "MYSQL PASSWORD";
$mysql_link = mysql_connect("localhost", $admin, $adpass);
mysql_select_db($db, $mysql_link);

$query = "SELECT * FROM avg_tally ORDER BY average DESC";
$result = mysql_query($query, $mysql_link);
if(mysql_num_rows($result)) {
  $rank = 1;
  while($row = mysql_fetch_row($result)) 
  {
    print("</tr><tr>");
    if($color == "#D8DBFE") {
     $color = "#A6ACFD";
    } else {
      $color = "#D8DBFE";
    }
   print("<td width=\"6%\" bgcolor=\"$color\"><center><small>");
   print("<font face=\"Verdana\">$rank</font></small></center></td>");
   print("<td width=\"7%\" bgcolor=\"$color\"><center><small>");
   print("<font face=\"Verdana\"><strong>$row[1]</strong></font></small></center></td>");
   print("<td width=\"11%\" bgcolor=\"$color\"><center><small>");
   $url = $row[2] . ".php3";
     if(!file_exists($url)) { $url = $row[2] . ".html"; }
   print("<font face=\"Verdana\"><a href=\"$url\">$row[2]</a></font></small></center></td>");
   print("<td width=\"76%\" bgcolor=\"$color\"><left><small>");
   print("<font face=\"Verdana\">$row[3]</font></small></left></td>");
      $rank++;
?>