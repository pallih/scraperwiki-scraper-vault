<?php
    scraperwiki::attach("game_score_of_saitama_seibu_lions");
    $teams = scraperwiki::select("* FROM game_score_of_saitama_seibu_lions.teams ORDER BY id ASC");
?>
<style type="text/css">
    table {
        border-collapse: collapse;
    }
    td, th {
        border: 1px solid #000033;
        font-size: 14px;
        padding: 5px;
    }
    th {
        background-color: #000033;
        color: #ffffff;
    }
</style>
<table>
    <thead>
        <tr>
            <th>Team</th>
            <th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th><th>7</th><th>8</th><th>9</th><th>10</th><th>11</th><th>12</th>
            <th>R</th><th>H</th><th>E</th>
        </tr>
    </thead>
    <tbody>
    <?php
        foreach($teams as $team){
            $team_id = $team["id"];
    ?>
        <tr>
            <th><?= $team["name"] ?></th>
    <?php
            $innings = scraperwiki::select("* FROM game_score_of_saitama_seibu_lions.innings WHERE team = ? ORDER BY inning ASC", array($team_id));
            foreach($innings as $inning) {
    ?>
            <td><?= $inning["runs"] ?></td>
    <?php
            }
    ?>
            <td><?= $team["runs"] ?></td>
            <td><?= $team["hits"] ?></td>
            <td><?= $team["errors"] ?></td>
        </tr>
    <?php
        }
    ?>
    </tbody>
</table>