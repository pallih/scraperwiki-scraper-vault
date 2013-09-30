<?php

// retrieval for https://scraperwiki.com/scrapers/es_congreso_voting_records_downloader

//temp
//first voting records are from 2012
//scraperwiki::save_var('last_date','2012-01-01');

$last_date = scraperwiki::get_var('last_date');

scraperwiki::attach("es_congreso_voting_records_downloader", "src");
$rows = scraperwiki::select("date,number from src.division WHERE date>='{$last_date}' ORDER BY date, number");

foreach ($rows as $row) {
  $item0 = scraperwiki::select("* from src.division WHERE date='{$row['date']}' AND number='{$row['number']}'");
  $item = $item0[0];
  $xml = simplexml_load_string($item['xml']);

  $info = $xml->Informacion;
  $total = $xml->Totales;

  $division = array(
    'session' => (string)$info->Sesion,
    'number_in_session' => (string)$info->NumeroVotacion[0],
    'date' => $item['date'],
    'name' => (string)$info->Titulo,
    'description' => (string)$info->TextoExpendiente,
    'subname' => (string)$info->TituloSubGrupo,
    'subdescription' => (string)$info->TextoSubGrupo,
    'passed' => (string)$total->Asentimiento,
    'present' => (string)$total->Presentes,
    'for' => (string)$total->AFavor,
    'against' => (string)$total->EnContra,
    'abstain' => (string)$total->Abstenciones,
    'not_voted' => (string)$total->NoVotan,
    'division_id' => str_replace('-','',$division['date']) . n3($division['number_in_session']),
  );

  $votes = array();
  foreach ($xml->Votaciones->Votacion as $row) {
    $votes[] = array(
        'seat' => (string)$row->Asiento,
        'mp_name' => (string)$row->Diputado,
        'vote' => (string)$row->Voto,
        'division_id' => str_replace('-','',$division['date']) . n3($division['number_in_session']),
    );
  }

    scraperwiki::save_sqlite(array('date','number_in_session'),$division,'division');
    scraperwiki::save_sqlite(array('seat','division_id'),$votes,'mp_vote');
    scraperwiki::save_var('last_date',$division['date']);
  

}

function n3($n) {
  if ($n >= 100) return $n;
  if ($n >= 10) return '0' . $n;
  return '00' . $n;
}


?>
<?php

// retrieval for https://scraperwiki.com/scrapers/es_congreso_voting_records_downloader

//temp
//first voting records are from 2012
//scraperwiki::save_var('last_date','2012-01-01');

$last_date = scraperwiki::get_var('last_date');

scraperwiki::attach("es_congreso_voting_records_downloader", "src");
$rows = scraperwiki::select("date,number from src.division WHERE date>='{$last_date}' ORDER BY date, number");

foreach ($rows as $row) {
  $item0 = scraperwiki::select("* from src.division WHERE date='{$row['date']}' AND number='{$row['number']}'");
  $item = $item0[0];
  $xml = simplexml_load_string($item['xml']);

  $info = $xml->Informacion;
  $total = $xml->Totales;

  $division = array(
    'session' => (string)$info->Sesion,
    'number_in_session' => (string)$info->NumeroVotacion[0],
    'date' => $item['date'],
    'name' => (string)$info->Titulo,
    'description' => (string)$info->TextoExpendiente,
    'subname' => (string)$info->TituloSubGrupo,
    'subdescription' => (string)$info->TextoSubGrupo,
    'passed' => (string)$total->Asentimiento,
    'present' => (string)$total->Presentes,
    'for' => (string)$total->AFavor,
    'against' => (string)$total->EnContra,
    'abstain' => (string)$total->Abstenciones,
    'not_voted' => (string)$total->NoVotan,
    'division_id' => str_replace('-','',$division['date']) . n3($division['number_in_session']),
  );

  $votes = array();
  foreach ($xml->Votaciones->Votacion as $row) {
    $votes[] = array(
        'seat' => (string)$row->Asiento,
        'mp_name' => (string)$row->Diputado,
        'vote' => (string)$row->Voto,
        'division_id' => str_replace('-','',$division['date']) . n3($division['number_in_session']),
    );
  }

    scraperwiki::save_sqlite(array('date','number_in_session'),$division,'division');
    scraperwiki::save_sqlite(array('seat','division_id'),$votes,'mp_vote');
    scraperwiki::save_var('last_date',$division['date']);
  

}

function n3($n) {
  if ($n >= 100) return $n;
  if ($n >= 10) return '0' . $n;
  return '00' . $n;
}


?>
<?php

// retrieval for https://scraperwiki.com/scrapers/es_congreso_voting_records_downloader

//temp
//first voting records are from 2012
//scraperwiki::save_var('last_date','2012-01-01');

$last_date = scraperwiki::get_var('last_date');

scraperwiki::attach("es_congreso_voting_records_downloader", "src");
$rows = scraperwiki::select("date,number from src.division WHERE date>='{$last_date}' ORDER BY date, number");

foreach ($rows as $row) {
  $item0 = scraperwiki::select("* from src.division WHERE date='{$row['date']}' AND number='{$row['number']}'");
  $item = $item0[0];
  $xml = simplexml_load_string($item['xml']);

  $info = $xml->Informacion;
  $total = $xml->Totales;

  $division = array(
    'session' => (string)$info->Sesion,
    'number_in_session' => (string)$info->NumeroVotacion[0],
    'date' => $item['date'],
    'name' => (string)$info->Titulo,
    'description' => (string)$info->TextoExpendiente,
    'subname' => (string)$info->TituloSubGrupo,
    'subdescription' => (string)$info->TextoSubGrupo,
    'passed' => (string)$total->Asentimiento,
    'present' => (string)$total->Presentes,
    'for' => (string)$total->AFavor,
    'against' => (string)$total->EnContra,
    'abstain' => (string)$total->Abstenciones,
    'not_voted' => (string)$total->NoVotan,
    'division_id' => str_replace('-','',$division['date']) . n3($division['number_in_session']),
  );

  $votes = array();
  foreach ($xml->Votaciones->Votacion as $row) {
    $votes[] = array(
        'seat' => (string)$row->Asiento,
        'mp_name' => (string)$row->Diputado,
        'vote' => (string)$row->Voto,
        'division_id' => str_replace('-','',$division['date']) . n3($division['number_in_session']),
    );
  }

    scraperwiki::save_sqlite(array('date','number_in_session'),$division,'division');
    scraperwiki::save_sqlite(array('seat','division_id'),$votes,'mp_vote');
    scraperwiki::save_var('last_date',$division['date']);
  

}

function n3($n) {
  if ($n >= 100) return $n;
  if ($n >= 10) return '0' . $n;
  return '00' . $n;
}


?>
<?php

// retrieval for https://scraperwiki.com/scrapers/es_congreso_voting_records_downloader

//temp
//first voting records are from 2012
//scraperwiki::save_var('last_date','2012-01-01');

$last_date = scraperwiki::get_var('last_date');

scraperwiki::attach("es_congreso_voting_records_downloader", "src");
$rows = scraperwiki::select("date,number from src.division WHERE date>='{$last_date}' ORDER BY date, number");

foreach ($rows as $row) {
  $item0 = scraperwiki::select("* from src.division WHERE date='{$row['date']}' AND number='{$row['number']}'");
  $item = $item0[0];
  $xml = simplexml_load_string($item['xml']);

  $info = $xml->Informacion;
  $total = $xml->Totales;

  $division = array(
    'session' => (string)$info->Sesion,
    'number_in_session' => (string)$info->NumeroVotacion[0],
    'date' => $item['date'],
    'name' => (string)$info->Titulo,
    'description' => (string)$info->TextoExpendiente,
    'subname' => (string)$info->TituloSubGrupo,
    'subdescription' => (string)$info->TextoSubGrupo,
    'passed' => (string)$total->Asentimiento,
    'present' => (string)$total->Presentes,
    'for' => (string)$total->AFavor,
    'against' => (string)$total->EnContra,
    'abstain' => (string)$total->Abstenciones,
    'not_voted' => (string)$total->NoVotan,
    'division_id' => str_replace('-','',$division['date']) . n3($division['number_in_session']),
  );

  $votes = array();
  foreach ($xml->Votaciones->Votacion as $row) {
    $votes[] = array(
        'seat' => (string)$row->Asiento,
        'mp_name' => (string)$row->Diputado,
        'vote' => (string)$row->Voto,
        'division_id' => str_replace('-','',$division['date']) . n3($division['number_in_session']),
    );
  }

    scraperwiki::save_sqlite(array('date','number_in_session'),$division,'division');
    scraperwiki::save_sqlite(array('seat','division_id'),$votes,'mp_vote');
    scraperwiki::save_var('last_date',$division['date']);
  

}

function n3($n) {
  if ($n >= 100) return $n;
  if ($n >= 10) return '0' . $n;
  return '00' . $n;
}


?>
