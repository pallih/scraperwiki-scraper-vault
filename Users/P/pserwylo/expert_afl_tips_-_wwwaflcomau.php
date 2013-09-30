<?php
require 'scraperwiki/simple_html_dom.php'; 

define( "SOURCE", "www.afl.com.au" );
define( "YEAR", date( 'Y' ) );
define( "GAMES_PER_ROUND", 9 );

// TODO: Does this URL change each week?
$html = scraperwiki::scrape( "http://www.afl.com.au/Tipping/AFLExpertTipsters/tabid/13842/Default.aspx" );
$dom = new simple_html_dom();
$dom->load( $html );

// This is here because if I call get_var without calling set_var first, then it busts,
// so the first time I run this I'll need to uncomment this line, then recomment for 
// further runs...
// scraperwiki::save_var( SOURCE . "-" . YEAR . "-lastRound", 0 );

// Find out which round we are tipping for currently...
$title = $dom->find( "table.teamTabular thead th h4" );
$round = 0;
if ( is_array( $title ) && count( $title ) > 0 ) {
  $titleText = strtolower( trim( $title[0]->plaintext ) );
  $i = strpos( $titleText, "round " );
  $round = (int)substr( $titleText, $i + 6 /* 6 == strlen( "round " ) */ );
}

// If we can't find out the round number, then 
if ( $round <= 0 ) {
  echo "Cannot find round number, bailing...\n";
  exit;
} else if ( $round == scraperwiki::get_var( SOURCE . "-" . YEAR . "-lastRound" ) ) {
  echo "Already have data for this round, bailing...\n";
  exit;
}

echo "Round: " . $round . "\n";

// REMOVED: Just save them all in a big flat table...
// echo "Saving round " . $round . " from " . SOURCE . "\n";
// $roundData = array( 'round' => $round, 'source' => SOURCE, 'year' => YEAR );
// scraperwiki::save_sqlite( array( "source", "round" ), $roundData, "round" );

// Find each expert and their respective tips...
foreach( $dom->find( "table.teamTabular tbody tr" ) as $tr ) {
  $i = 0;

  $cells = $tr->find( 'td' );
  if ( count( $cells ) < 11 /* 11 = Tipper + Score + 9 * Tips */ ) {
    echo "Skipping row, not enough cells.\n";
    continue;
  }

  $expertName = "";
  foreach( $cells as $td )
  {
    if ( $i == 0 ) {

      // Expert name and picture...
      $expertName = trim( $td->plaintext );
      echo "Expert: " . $expertName . "\n";

    } else if ( $i == 1 ) { 

      // This holds the current score of the tipster...
      $correct = (int)trim( $td->plaintext );      
      $total = ( $round - 1 ) * GAMES_PER_ROUND;
      $score = $correct / $total * 100;
      $scoreRow = array( 
        'expert' => $expertName,
        'round' => $round,
        'year' => YEAR,
        'source' => SOURCE,
        'correct' => $correct,
        'score' => $score,
        'total' => $total,
      );
      echo "Saving current results for " . $expertName . " - " . $correct . "\n";
      scraperwiki::save_sqlite( array( "expert", "round", "year", "source" ), $scoreRow, "results" );

    } else {

      // Tip for a particular round.
      // Need to get the team from the image name, because AFL sucks at accessability and websites in general...
      $img = $td->find( "img" );
      if ( is_array( $img ) && count( $img ) > 0 ) {
        // Example src: http://www.afl.com.au/portals/0/2012/FLAGS2011/hawthornhawks.gif
        $src = $img[0]->src;
        $lastSlash = strrpos( $src, "/" );
        $lastDot = strrpos( $src, "." );
        $team = substr( $src, $lastSlash + 1, -( strlen( $src ) - $lastDot ) );
        $gameNum = $i - 1;        

        echo " - " . $team . "\n";
        $tipRow = array(
          "expert" => $expertName,
          "round" => $round,
          "year" => YEAR,
          "gameNum" => $gameNum ++,
          "tip" => $team,
          "source" => SOURCE
        );
        scraperwiki::save_sqlite( array( "expert", "round", "source", "year", "gameNum" ), $tipRow, "tips" );


      }

    }
    $i ++;
  }
}

scraperwiki::save_var( SOURCE . "-" . YEAR . "-lastRound", $round );
<?php
require 'scraperwiki/simple_html_dom.php'; 

define( "SOURCE", "www.afl.com.au" );
define( "YEAR", date( 'Y' ) );
define( "GAMES_PER_ROUND", 9 );

// TODO: Does this URL change each week?
$html = scraperwiki::scrape( "http://www.afl.com.au/Tipping/AFLExpertTipsters/tabid/13842/Default.aspx" );
$dom = new simple_html_dom();
$dom->load( $html );

// This is here because if I call get_var without calling set_var first, then it busts,
// so the first time I run this I'll need to uncomment this line, then recomment for 
// further runs...
// scraperwiki::save_var( SOURCE . "-" . YEAR . "-lastRound", 0 );

// Find out which round we are tipping for currently...
$title = $dom->find( "table.teamTabular thead th h4" );
$round = 0;
if ( is_array( $title ) && count( $title ) > 0 ) {
  $titleText = strtolower( trim( $title[0]->plaintext ) );
  $i = strpos( $titleText, "round " );
  $round = (int)substr( $titleText, $i + 6 /* 6 == strlen( "round " ) */ );
}

// If we can't find out the round number, then 
if ( $round <= 0 ) {
  echo "Cannot find round number, bailing...\n";
  exit;
} else if ( $round == scraperwiki::get_var( SOURCE . "-" . YEAR . "-lastRound" ) ) {
  echo "Already have data for this round, bailing...\n";
  exit;
}

echo "Round: " . $round . "\n";

// REMOVED: Just save them all in a big flat table...
// echo "Saving round " . $round . " from " . SOURCE . "\n";
// $roundData = array( 'round' => $round, 'source' => SOURCE, 'year' => YEAR );
// scraperwiki::save_sqlite( array( "source", "round" ), $roundData, "round" );

// Find each expert and their respective tips...
foreach( $dom->find( "table.teamTabular tbody tr" ) as $tr ) {
  $i = 0;

  $cells = $tr->find( 'td' );
  if ( count( $cells ) < 11 /* 11 = Tipper + Score + 9 * Tips */ ) {
    echo "Skipping row, not enough cells.\n";
    continue;
  }

  $expertName = "";
  foreach( $cells as $td )
  {
    if ( $i == 0 ) {

      // Expert name and picture...
      $expertName = trim( $td->plaintext );
      echo "Expert: " . $expertName . "\n";

    } else if ( $i == 1 ) { 

      // This holds the current score of the tipster...
      $correct = (int)trim( $td->plaintext );      
      $total = ( $round - 1 ) * GAMES_PER_ROUND;
      $score = $correct / $total * 100;
      $scoreRow = array( 
        'expert' => $expertName,
        'round' => $round,
        'year' => YEAR,
        'source' => SOURCE,
        'correct' => $correct,
        'score' => $score,
        'total' => $total,
      );
      echo "Saving current results for " . $expertName . " - " . $correct . "\n";
      scraperwiki::save_sqlite( array( "expert", "round", "year", "source" ), $scoreRow, "results" );

    } else {

      // Tip for a particular round.
      // Need to get the team from the image name, because AFL sucks at accessability and websites in general...
      $img = $td->find( "img" );
      if ( is_array( $img ) && count( $img ) > 0 ) {
        // Example src: http://www.afl.com.au/portals/0/2012/FLAGS2011/hawthornhawks.gif
        $src = $img[0]->src;
        $lastSlash = strrpos( $src, "/" );
        $lastDot = strrpos( $src, "." );
        $team = substr( $src, $lastSlash + 1, -( strlen( $src ) - $lastDot ) );
        $gameNum = $i - 1;        

        echo " - " . $team . "\n";
        $tipRow = array(
          "expert" => $expertName,
          "round" => $round,
          "year" => YEAR,
          "gameNum" => $gameNum ++,
          "tip" => $team,
          "source" => SOURCE
        );
        scraperwiki::save_sqlite( array( "expert", "round", "source", "year", "gameNum" ), $tipRow, "tips" );


      }

    }
    $i ++;
  }
}

scraperwiki::save_var( SOURCE . "-" . YEAR . "-lastRound", $round );
