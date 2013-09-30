<html>
<head>
  <title>Drupal Stock Suggestor by Viet Coop</title>
  <style>
    table {
      width: 55%;
      margin: 0 auto;
    }
    
    thead {
      background: #000;
      color: #fff;
    }
    
    tbody tr {
      border-bottom: 1px #333 solid;
    }
  </style>
</head>
<body>
<?php

scraperwiki::attach("drupy-stock");

if (!empty($_GET['cash']) && is_numeric($_GET['cash'])) {
  function fetch($cash) {
    $data  = "*,";
    $data .= " (share_value - change) as old_value,";
    $data .= " ({$cash} / (share_value - change)) as can,";
    $data .= " ({$cash} / share_value) * change as growth";
    $data .= " from 'drupy-stock'.swdata";
    $data .= " where share_value < {$cash} and can <= 100 AND old_value > 0";
    $data .= " order by growth desc limit 100";
    $data = scraperwiki::select($data);
    return $data;
  }

  function get($real_cash, $cash) {
    $projects = array();
    foreach (fetch($cash) as $project) {
      $pay = $project['old_value'] * $project['can'];

      if ($real_cash < $pay) {
        break;
      }

      if ($real_cash >= $pay) {
        $projects[] = $project;
        $cash -= $real_cash;
      }
    }
    return $projects;
  }
  
  function table($real_cash, $cash) {
    print '<table>';
    print '<thead><tr><th>Project</th><th>Change</th><th>Old Value</th><th>New Value</th><th>Can buy</th><th>Growth</th></tr></thead>';
    print '<tbody>';
    
    $total = 0;

    foreach (get($real_cash, $cash) as $project) {
        print '  <td><a href="http://drupal.webstocks.ws/project/'. $project['name'] .'">' . $project['label'] . '</a></td>';
        print '  <td>'. $project['change'] .'</td>';
        print '  <td>'. $project['old_value'] .'</td>';
        print '  <td>'. $project['share_value'] .'</td>';
        print '  <td>'. $project['can'] .'</td>';
        print '  <td>'. $project['growth'] .'</td>';
        print '</tr>';
        
        $total += $project['growth'];
    }

    print '</tbody>';
    print '<tfoot><th><tr><td colspan="5" style="text-align: right;">Total:</td><td>'. $total .'</td></tr></th></tfoot>';
    print '</table>';
  }

  for ($try = 1; $try <= 10; $try++) {
    $cash = floor($_GET['cash'] / $try);
    table($_GET['cash'], $cash);
  }
}
else {
  $data  = "* from 'drupy-stock'.swdata";
  if (isset($_GET['max']) && is_numeric($_GET['max'])) {
    $data .= " where share_value < {$_GET['max']}";
  }
  $data .= " order by change desc";
  $data .= " limit 100";
  $data = scraperwiki::select($data);
  print '<table>';
  print '<thead><tr><th>Project</th><th>Change</th><th>Share Value</th></tr></thead>';
  print '<tbody>';

  foreach ($data as $project) {
    print '<tr>';
    print '  <td><a href="http://drupal.webstocks.ws/project/'. $project['name'] .'">' . $project['label'] . '</a></td>';
    print '  <td>'. $project['change'] .'</td>';
    print '  <td>'. $project['share_value'] .'</td>';
    print '</tr>';
  }
  
  print '</tbody></table>';
}
?></body></html><html>
<head>
  <title>Drupal Stock Suggestor by Viet Coop</title>
  <style>
    table {
      width: 55%;
      margin: 0 auto;
    }
    
    thead {
      background: #000;
      color: #fff;
    }
    
    tbody tr {
      border-bottom: 1px #333 solid;
    }
  </style>
</head>
<body>
<?php

scraperwiki::attach("drupy-stock");

if (!empty($_GET['cash']) && is_numeric($_GET['cash'])) {
  function fetch($cash) {
    $data  = "*,";
    $data .= " (share_value - change) as old_value,";
    $data .= " ({$cash} / (share_value - change)) as can,";
    $data .= " ({$cash} / share_value) * change as growth";
    $data .= " from 'drupy-stock'.swdata";
    $data .= " where share_value < {$cash} and can <= 100 AND old_value > 0";
    $data .= " order by growth desc limit 100";
    $data = scraperwiki::select($data);
    return $data;
  }

  function get($real_cash, $cash) {
    $projects = array();
    foreach (fetch($cash) as $project) {
      $pay = $project['old_value'] * $project['can'];

      if ($real_cash < $pay) {
        break;
      }

      if ($real_cash >= $pay) {
        $projects[] = $project;
        $cash -= $real_cash;
      }
    }
    return $projects;
  }
  
  function table($real_cash, $cash) {
    print '<table>';
    print '<thead><tr><th>Project</th><th>Change</th><th>Old Value</th><th>New Value</th><th>Can buy</th><th>Growth</th></tr></thead>';
    print '<tbody>';
    
    $total = 0;

    foreach (get($real_cash, $cash) as $project) {
        print '  <td><a href="http://drupal.webstocks.ws/project/'. $project['name'] .'">' . $project['label'] . '</a></td>';
        print '  <td>'. $project['change'] .'</td>';
        print '  <td>'. $project['old_value'] .'</td>';
        print '  <td>'. $project['share_value'] .'</td>';
        print '  <td>'. $project['can'] .'</td>';
        print '  <td>'. $project['growth'] .'</td>';
        print '</tr>';
        
        $total += $project['growth'];
    }

    print '</tbody>';
    print '<tfoot><th><tr><td colspan="5" style="text-align: right;">Total:</td><td>'. $total .'</td></tr></th></tfoot>';
    print '</table>';
  }

  for ($try = 1; $try <= 10; $try++) {
    $cash = floor($_GET['cash'] / $try);
    table($_GET['cash'], $cash);
  }
}
else {
  $data  = "* from 'drupy-stock'.swdata";
  if (isset($_GET['max']) && is_numeric($_GET['max'])) {
    $data .= " where share_value < {$_GET['max']}";
  }
  $data .= " order by change desc";
  $data .= " limit 100";
  $data = scraperwiki::select($data);
  print '<table>';
  print '<thead><tr><th>Project</th><th>Change</th><th>Share Value</th></tr></thead>';
  print '<tbody>';

  foreach ($data as $project) {
    print '<tr>';
    print '  <td><a href="http://drupal.webstocks.ws/project/'. $project['name'] .'">' . $project['label'] . '</a></td>';
    print '  <td>'. $project['change'] .'</td>';
    print '  <td>'. $project['share_value'] .'</td>';
    print '</tr>';
  }
  
  print '</tbody></table>';
}
?></body></html>