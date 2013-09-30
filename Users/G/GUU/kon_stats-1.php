<?php
$short_name = 'kon_members-1';

ScraperWiki::attach($short_name, 'src');
$keys = ScraperWiki::sqliteexecute("select * from swdata limit 0")->keys;
$data = ScraperWiki::select("* from swdata");


$class = array(
    "captain" => 0, 
    "lore-master" => 0,
    "rune-keeper" => 0,
    "guardian" => 0, 
    "minstrel" => 0, 
    "hunter" => 0, 
    "burglar" => 0, 
    "champion" => 0,
    "warden" => 0
 );
$level = array( '0-9' =>0, '10-19' =>0, '20-29' =>0, '30-39' =>0, '40-49' =>0,'50-59' =>0,'60-65' =>0);
$race = array( 'elf' => 0, 'race of man' => 0, 'hobbit' => 0, 'dwarf' => 0 );
$rank = array( 'leader' => 0, 'officer' => 0, 'member' => 0);
$members = array();

foreach( $data as $i => $member )
{
    $class[strtolower($member->class)]++;
    $race[strtolower($member->race)]++;
    $rank[strtolower($member->rank)]++;
    $lvl = intval($member->level);
    $range = $lvl - ( $lvl % 10 );
    if( $lvl <= 10 ) { $st = 0; $en = 10; }
    elseif( $lvl >= 60 ) { $st = 60; $en = 66; }
    else { $st = $range; $en = $range+10; }

    $lb = "$st-".($en-1);
    $level[$lb]++;
    if( !isset($date) ) $date = $data[$i]->date_scraped;
    unset ( $data[$i]->date_scraped);
}
ksort($level);

$stats = array ( 'class' => $class, 'rank' => $rank,  'race' => $race, 'level' => $level );
$meta = array ( 'class' => count($class), 'rank' => count($rank),  'race' => count($race), 'level' => count($level) );

/* <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"> */
?>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
 "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    <link rel="stylesheet" href="http://yui.yahooapis.com/2.8.0r4/build/reset-fonts-grids/reset-fonts-grids.css" type="text/css">
    <script type="text/javascript" src="http://content.level3.turbine.com/sites/lorebook.lotro.com/js/onering.js"></script>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
        var char_size = {'width':500, 'height':350};
        String.prototype.capitalize = function(){ return this.replace( /(^|\s)([a-z])/g , function(m,p1,p2){ return p1+p2.toUpperCase(); } ); };
      var KoN_stats =<?=json_encode($stats)?>;
      var KoN_meta =<?=json_encode($meta)?>;
      var KoN_list =<?=json_encode($data)?>;
      google.load("visualization", "1", {packages:["table", "corechart"]});
      function drawChart(label, obj, dest) {
        var data = new google.visualization.DataTable(), i=0, prefix='';
        data.addColumn('string', label);
        data.addColumn('number', 'Total');
        data.addRows(KoN_meta[obj]);
        if( obj ===  'level' ) prefix = 'Level ';
        
        for( cl in KoN_stats[obj] ) 
        {
            data.setValue(i, 0, prefix+ cl.capitalize());
            data.setValue(i, 1, KoN_stats[obj][cl]);
            i++;
        }
        var chart = new google.visualization.PieChart(document.getElementById(dest));
        chart.draw(data, {width: char_size.width, height: char_size.height, title: label,  is3D: true});
      }
      google.setOnLoadCallback(function() { drawChart('Classes', 'class', 'class_div'); });
      google.setOnLoadCallback(function() { drawChart('Levels', 'level', 'level_div'); });
      google.setOnLoadCallback(function() { drawChart('Races', 'race', 'race_div'); });

        google.setOnLoadCallback(drawRoster);
        function drawRoster() {
          var data = new google.visualization.DataTable();
          data.addColumn('string', 'Name');
          data.addColumn('string', 'Race');
          data.addColumn('string', 'Class');
          data.addColumn('number', 'Level');
//          data.addColumn('string', 'Rank');
          data.addRows(KoN_list.length);

          for (var i=0; i<KoN_list.length;i++ ) 
          {
              var member = KoN_list[i];
              data.setCell(i, 0, member['name'].capitalize());
              data.setCell(i, 1, member['race'].capitalize());
              data.setCell(i, 2, member['class'].replace("-", "_")); // .capitalize());
              data.setCell(i, 3, parseInt(member['level']));
          }        
          // Create and draw the visualization.
          var table = new google.visualization.Table(document.getElementById('roster'));
          var options =[];
          options['allowHtml'] =  true;
          options['alternatingRowStyle'] = true;
          options['sortColumn'] = 0;
          options['sort'] = 'disable';
          options['page'] = 'enable';
          options['pageSize'] = 15;
          //options['width'] = 500;
          //options['height'] = 400;
          //options['pagingSymbols'] = {prev: 'prev', next: 'next'};
          //options['pagingButtonsConfiguration'] = 'auto';
          var class_formatter = new google.visualization.PatternFormat('<img src="http://content.turbine.com/sites/my.lotro.com/themes/default/media/common/class_icon_small/{0}.png" title="{0}"/>');
          class_formatter.format(data, [2]);
          var class_formatter = new google.visualization.PatternFormat('<a target="_new" href="http://my.lotro.com/character/riddermark/{0}/">{0}</a>');
          class_formatter.format(data, [0]);

            var lvl_formatter = new google.visualization.BarFormat({width: 100});
            lvl_formatter.format(data, 3);

          data.sort(0);
          table.draw(data, options);  
        }
        google.setOnLoadCallback(function() {document.getElementById('scraperwikipane').innerHTML ='';});
    </script>
  </head>

  <body>

    <div id="doc2" class="yui-t7">
        <div id="hd" role="contentinfo"><h1>Kings of Numenor on Riddermark</h1></div>
        
        <div id="bd" role="main">
            <div class="yui-ge">
                <div class="yui-u first">
                    <div id="roster"></div>
                </div>
                <div class="yui-u">
                    <div id="class_div"></div><div id="level_div"></div><div id="race_div"></div>
                </div>
            </div>
        </div>
        <div id="ft" role="contentinfo"><p>Last update on <?=$date?></p></div>
    </div>
  </body>
</html><?php
$short_name = 'kon_members-1';

ScraperWiki::attach($short_name, 'src');
$keys = ScraperWiki::sqliteexecute("select * from swdata limit 0")->keys;
$data = ScraperWiki::select("* from swdata");


$class = array(
    "captain" => 0, 
    "lore-master" => 0,
    "rune-keeper" => 0,
    "guardian" => 0, 
    "minstrel" => 0, 
    "hunter" => 0, 
    "burglar" => 0, 
    "champion" => 0,
    "warden" => 0
 );
$level = array( '0-9' =>0, '10-19' =>0, '20-29' =>0, '30-39' =>0, '40-49' =>0,'50-59' =>0,'60-65' =>0);
$race = array( 'elf' => 0, 'race of man' => 0, 'hobbit' => 0, 'dwarf' => 0 );
$rank = array( 'leader' => 0, 'officer' => 0, 'member' => 0);
$members = array();

foreach( $data as $i => $member )
{
    $class[strtolower($member->class)]++;
    $race[strtolower($member->race)]++;
    $rank[strtolower($member->rank)]++;
    $lvl = intval($member->level);
    $range = $lvl - ( $lvl % 10 );
    if( $lvl <= 10 ) { $st = 0; $en = 10; }
    elseif( $lvl >= 60 ) { $st = 60; $en = 66; }
    else { $st = $range; $en = $range+10; }

    $lb = "$st-".($en-1);
    $level[$lb]++;
    if( !isset($date) ) $date = $data[$i]->date_scraped;
    unset ( $data[$i]->date_scraped);
}
ksort($level);

$stats = array ( 'class' => $class, 'rank' => $rank,  'race' => $race, 'level' => $level );
$meta = array ( 'class' => count($class), 'rank' => count($rank),  'race' => count($race), 'level' => count($level) );

/* <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"> */
?>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
 "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    <link rel="stylesheet" href="http://yui.yahooapis.com/2.8.0r4/build/reset-fonts-grids/reset-fonts-grids.css" type="text/css">
    <script type="text/javascript" src="http://content.level3.turbine.com/sites/lorebook.lotro.com/js/onering.js"></script>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
        var char_size = {'width':500, 'height':350};
        String.prototype.capitalize = function(){ return this.replace( /(^|\s)([a-z])/g , function(m,p1,p2){ return p1+p2.toUpperCase(); } ); };
      var KoN_stats =<?=json_encode($stats)?>;
      var KoN_meta =<?=json_encode($meta)?>;
      var KoN_list =<?=json_encode($data)?>;
      google.load("visualization", "1", {packages:["table", "corechart"]});
      function drawChart(label, obj, dest) {
        var data = new google.visualization.DataTable(), i=0, prefix='';
        data.addColumn('string', label);
        data.addColumn('number', 'Total');
        data.addRows(KoN_meta[obj]);
        if( obj ===  'level' ) prefix = 'Level ';
        
        for( cl in KoN_stats[obj] ) 
        {
            data.setValue(i, 0, prefix+ cl.capitalize());
            data.setValue(i, 1, KoN_stats[obj][cl]);
            i++;
        }
        var chart = new google.visualization.PieChart(document.getElementById(dest));
        chart.draw(data, {width: char_size.width, height: char_size.height, title: label,  is3D: true});
      }
      google.setOnLoadCallback(function() { drawChart('Classes', 'class', 'class_div'); });
      google.setOnLoadCallback(function() { drawChart('Levels', 'level', 'level_div'); });
      google.setOnLoadCallback(function() { drawChart('Races', 'race', 'race_div'); });

        google.setOnLoadCallback(drawRoster);
        function drawRoster() {
          var data = new google.visualization.DataTable();
          data.addColumn('string', 'Name');
          data.addColumn('string', 'Race');
          data.addColumn('string', 'Class');
          data.addColumn('number', 'Level');
//          data.addColumn('string', 'Rank');
          data.addRows(KoN_list.length);

          for (var i=0; i<KoN_list.length;i++ ) 
          {
              var member = KoN_list[i];
              data.setCell(i, 0, member['name'].capitalize());
              data.setCell(i, 1, member['race'].capitalize());
              data.setCell(i, 2, member['class'].replace("-", "_")); // .capitalize());
              data.setCell(i, 3, parseInt(member['level']));
          }        
          // Create and draw the visualization.
          var table = new google.visualization.Table(document.getElementById('roster'));
          var options =[];
          options['allowHtml'] =  true;
          options['alternatingRowStyle'] = true;
          options['sortColumn'] = 0;
          options['sort'] = 'disable';
          options['page'] = 'enable';
          options['pageSize'] = 15;
          //options['width'] = 500;
          //options['height'] = 400;
          //options['pagingSymbols'] = {prev: 'prev', next: 'next'};
          //options['pagingButtonsConfiguration'] = 'auto';
          var class_formatter = new google.visualization.PatternFormat('<img src="http://content.turbine.com/sites/my.lotro.com/themes/default/media/common/class_icon_small/{0}.png" title="{0}"/>');
          class_formatter.format(data, [2]);
          var class_formatter = new google.visualization.PatternFormat('<a target="_new" href="http://my.lotro.com/character/riddermark/{0}/">{0}</a>');
          class_formatter.format(data, [0]);

            var lvl_formatter = new google.visualization.BarFormat({width: 100});
            lvl_formatter.format(data, 3);

          data.sort(0);
          table.draw(data, options);  
        }
        google.setOnLoadCallback(function() {document.getElementById('scraperwikipane').innerHTML ='';});
    </script>
  </head>

  <body>

    <div id="doc2" class="yui-t7">
        <div id="hd" role="contentinfo"><h1>Kings of Numenor on Riddermark</h1></div>
        
        <div id="bd" role="main">
            <div class="yui-ge">
                <div class="yui-u first">
                    <div id="roster"></div>
                </div>
                <div class="yui-u">
                    <div id="class_div"></div><div id="level_div"></div><div id="race_div"></div>
                </div>
            </div>
        </div>
        <div id="ft" role="contentinfo"><p>Last update on <?=$date?></p></div>
    </div>
  </body>
</html>