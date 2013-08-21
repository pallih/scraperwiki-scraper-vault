<?php
        function alphabetCombos($length,$prefix = '') {
            for($j = 97; $j < 123; $j++) {
                if ($length > 1) {
                    alphabetCombos($length-1,$prefix . chr($j));
                } else {
                    echo $prefix . chr($j) . ' ';
                }
            }
        }

        alphabetCombos(2);

?>
