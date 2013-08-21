<?php
$scp[0] = "ASbX:IND";
$scp[1] = "WBcI:IND";
$scp[2] = "BEL2b0:IND";
$scp[3] = "BIRS:IND";
$scp[4] = "BGSMDC:IND";
$scp[5] = "SOFIX:IND";
$scp[6] = "CRO:IND";
$scp[7] = "CYSMMAPA:IND";
$scp[8] = "PX:IND";
$scp[9] = "KAX:IND";
$scp[10] = "TALSE:IND";
$scp[11] = "HEX:IND";
$scp[12] = "ASE:IND";
$scp[13] = "BUX:IND";
$scp[14] = "ICEXI:IND";
$scp[15] = "ISEQ:IND";
$scp[16] = "ITLMS:IND";
$scp[17] = "KZKAK:IND";
$scp[18] = "RIGSE:IND";
$scp[19] = "VILSE:IND";
$scp[20] = "LUXXX:IND";
$scp[21] = "MBIDM:IND";
$scp[22] = "MALTEX:IND";
$scp[23] = "SEMDEX:IND";
$scp[24] = "MONEX20:IND";
$scp[25] = "MOSENEW:IND";
$scp[26] = "AEX:IND";
$scp[27] = "OSEAX:IND";
$scp[28] = "WIG20:IND";
$scp[29] = "BVLX:IND";
$scp[30] = "BET:IND";
$scp[31] = "INDEXCF:IND";
$scp[32] = "BELEX15:IND";
$scp[33] = "SKSM:IND";
$scp[34] = "SBITOP:IND";
$scp[35] = "JALSH:IND";
$scp[36] = "OMX:IND";
$scp[37] = "SMI:IND";
$scp[38] = "UX:IND";
$scp[39] = "MEXBOL:IND";
$scp[40] = "IBG:IND";
$scp[41] = "BSX:IND";
$scp[42] = "IBOV:IND";
$scp[43] = "IGBC:IND";
$scp[44] = "IGPA:IND";
$scp[45] = "CRSMBCT:IND";
$scp[46] = "JMSMX:IND";
$scp[47] = "BVPSBVPS:IND";
$scp[48] = "IGBVL:IND";
$scp[49] = "IBVC:IND";
$scp[50] = "JCI:IND";
$scp[51] = "DHAKA:IND";
$scp[52] = "LSXC:IND";
$scp[53] = "FBMEMAS:IND";
$scp[54] = "MSETOP:IND";
$scp[55] = "KSE:IND";
$scp[56] = "PCOMP:IND";
$scp[57] = "FSTAS:IND";
$scp[58] = "CSEALL:IND";
$scp[59] = "KOSPI2:IND";
$scp[60] = "SET:IND";
$scp[61] = "VNINDEX:IND";
$scp[62] = "BHSEASI:IND";
$scp[63] = "CASE:IND";
$scp[64] = "TA-100:IND";
$scp[65] = "JOSMGNFF:IND";
$scp[66] = "SECTMIND:IND";
$scp[67] = "MSM30:IND";
$scp[68] = "PASISI:IND";
$scp[69] = "DSM:IND";
$scp[70] = "SASEIDX:IND";
$scp[71] = "XU100:IND";
$scp[72] = "DFMGI:IND";
$scp[73] = "ADSMI:IND";
$scp[74] = "NZSE:IND";
$scp[75] = "WIAUT:IND";
$scp[76] = "BEL20:IND";
$scp[77] = "CAC:IND";
$scp[78] = "ASX:IND";
$scp[79] = "DAX:IND";
$scp[80] = "NIFTY:IND";

for ($i = 2; $i <= 79; $i++ ) {
$url = "http://www.bloomberg.com/quote/".$scp[$i];
$jkl = file_get_contents($url);

$jkl = explode('span class="ticker_data">', $jkl );

$jkll = explode('</span>', $jkl[1] );
$stream = $jkll[0];


$message = scraperwiki::save_sqlite(array("a"), array("a"=>$scp[$i].":".$stream));
print_r($message); 



if ($i == 79) { $i = 3;}

}
?>
