<?php
function scrape($year, $code, $court_act) {
    $ch = curl_init();
    curl_setopt_array($ch, array(
        CURLOPT_URL => 'http://www.hcbombayatgoa.nic.in/actqry.asp',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POSTFIELDS => http_build_query(array(
            'warn' => '',
            'txtact' => $code,
            'txtyear' => $year
        )),
        CURLOPT_USERAGENT => 'User-Agent: Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.56 Safari/537.17',
        CURLOPT_CONNECTTIMEOUT => 0,
        CURLOPT_TIMEOUT => 1000,
    ));

    echo "Loading data (Court Act: $code-$court_act; Year: $year) ...\n";
    $dom = new DOMDocument();
    @$dom->loadHTML(curl_exec($ch));
    $xpath = new DOMXPath($dom);
    $dom = null;
    unset($dom);
    $query = $xpath->query('//select[@id="txtlist"]/option');
    $xpath = null;
    unset($xpath);
    $n = $query->length;

    echo "Parsing Results ...\n";
    $results = array();
    for ($i = 0; $i < $n; $i++) {
        $option = preg_split('/\r\n/', $query->item($i)->nodeValue);
        $party_role = 'Unknown';
        if (stripos($option[5], 'Pet') !== false) $party_role = 'Petitioner / Plaintiff';
        if (stripos($option[4], 'Res') !== false) $party_role = 'Respondent / Defendant';
        @$result = array(
            'unique_id' => trim($query->item($i)->getAttribute('value') .'-'. substr($party_role, 0, 3)),
            'case_number' => trim(preg_replace('/\xC2\xA0/', '', $option[1])),
            'path' => $query->item($i)->getAttribute('value'),
            'party_name' => trim($option[2]),
            'party_role' => $party_role,
            'filing_year' => $year,
            'court_act' => $court_act
        );
        array_push($results, $result);
        //Clean loop variables
        $option = null;
        $result = null;
        unset($option);
        unset($result);
        if ($i % 100 === 0 && count($results) > 1) { //If $results gets above 100 during the loop, then save and clear
            scraperwiki::save_sqlite(array('unique_id'), $results);
            $results = array();
        }
    }
    
    //Clean up
    $query = null;
    $xpath = null;
    $ch = null;
    unset($query);
    unset($xpath);
    unset($ch);

    //Final save to database
    scraperwiki::save_sqlite(array('unique_id'), $results);
    $results = null;
    unset($results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
}

$court_act_codes = array(
    396 => 'Absorbed Employees Act, 1965',
    53 => 'Adovcates Act 1961',
    68 => 'Ancient Monuments & Archeological Sites & Remains Act,1958',
    90 => 'Andhra Pradesh (Agricultural Produce & Livestock)Markets Act, 1966',
    376 => 'Apprentices Act, 1961',
    80 => 'Arbitration Act',
    82 => 'ARBITRATION AND CONCILIATION ACT, 1996',
    15 => 'B.T. & A.L. Act',
    402 => 'Bank & Financial Institution Act, 1993',
    39 => 'Banking Regulation Act',
    400 => 'C.C.S (Classification,Control & Appeal) Rules,1965',
    398 => 'C.C.S(C.C.A.) Rules,1965.',
    1 => 'C.P.C.',
    399 => 'Cental Civil Services (Conduct) Rules, 1964',
    67 => 'Central Civil Services (Revised Pay) Rules, 1997',
    34 => 'Central Excise & Salt Act',
    85 => 'Central Excise act 1944 under rule 59Q',
    401 => 'Central Industrial Tribunals Act',
    18 => 'City & Industrial Development Act',
    312 => 'Code of Communidade',
    73 => 'Commission of Inquiry Act, 1952',
    355 => 'Company Act, 1956',
    79 => 'Company Laws',
    54 => 'Constitution of India',
    360 => 'Consumer Protection Act',
    369 => 'Contempt of Court Act',
    27 => 'Contract Labour (Reg. & Abolition) Act',
    356 => 'Court Fees Act, 1870',
    201 => 'Criminal Procedure Code',
    35 => 'Customs Act, 1962',
    392 => 'Customs Tariff Act 1975',
    302 => 'Devasthan Regulation (Regu. de Mazanias)',
    51 => 'Displace Persons (C&R) Act 1954',
    319 => 'Divorce case under the Local Law',
    72 => 'Dock Workers (Regulation of Employment) Act, 1948',
    30 => 'Employees State Insurance Act, 1948',
    28 => 'Employment Provident Fund & Misc. P. Act',
    57 => 'Essential Commodities Act, 1955',
    71 => 'Evidence Act',
    26 => 'Factories Act',
    84 => 'FAMILY ACT CODE',
    365 => 'Foreign Exchange Managment Act, 1999',
    388 => 'Forest (Conservation) Act 1980',
    359 => 'Forest Act, 1927',
    351 => 'G.D.D. Agricultural Produce Marketing (Regulation) Rules, 1969',
    350 => 'G.D.D. Medical Education Service Rules, 1979',
    340 => 'G.D.D. Tourist Trade Act',
    322 => 'G.D.D.Abolition of Proprietorship of Lands in Diu Act,1971',
    323 => 'G.D.D.Abolition of Proprietorship of Lands in Diu(D.C.O.R.)Rules,1972',
    324 => 'G.D.D.Absorbed Employees Conditions of Service(Amendment)Rules,1976',
    336 => 'G.D.D.Agricultural Tenancy Act and Rules with Amendments upto 1992',
    326 => 'G.D.D.Civil Service (Judicial Branch) Rules-Amendment',
    327 => 'G.D.D.Entertainment Tax Act, 196',
    352 => 'G.D.D.Industrial Development Act,1965',
    329 => 'G.D.D.Irrigation Act, 1973',
    330 => 'G.D.D.Land Revenue Code, 1968 Vol.I',
    331 => 'G.D.D.Mundkar Act and Rules',
    332 => 'G.D.D.Municipalities (Amendment) Act, 1978',
    328 => 'G.D.D.Public Gambling Act, 1976',
    333 => 'G.D.D.Village Panchayats, Regulation and Rules',
    88 => 'Gazetted Posts Recruitment Rules, 1998',
    354 => 'Goa Childrens Act, 2003. U/s 6',
    383 => 'Goa Civil Court Act, 1965',
    346 => 'Goa Civil Services (Retirement) Rules, 2000',
    307 => 'Goa D.D Excise Duty Act 1964',
    306 => 'Goa D.D Housing Boards Act 1968',
    320 => 'Goa D.D Land Revenue Code 1966',
    305 => 'Goa D.D Lease Rent & Evic Cont. Act 1968',
    303 => 'Goa D.D Mundkars(Pro. from Evic.)Act1975',
    309 => 'Goa D.D Municipalities Act 1968',
    315 => 'Goa D.D Regist.of Tourism Trd.Act 1982',
    308 => 'Goa D.D Sales Tax Act 1964',
    317 => 'Goa D.D School Education Act 1984',
    313 => 'Goa D.D Shops & Establishment Act 1973',
    304 => 'Goa D.D Town & Country Planning Act 1974',
    301 => 'Goa D.D. Adminstrative Tribunal act 1965',
    310 => 'Goa Daman Diu Panchayat Act 1993',
    335 => 'Goa Govt.Seniority Rules, 1967',
    366 => 'Goa maintenance of public order & safety act 1988',
    343 => 'Goa Police Subordinate Services(Discipline & Appeal)Rules, 1975',
    377 => 'Goa Public Health Act',
    349 => 'Goa Right to Information Act, 1997',
    373 => 'Goa Rural Improvement and Welfare Cess Act',
    334 => 'Goa Sales Tax Act, with Amendment upto 1993',
    394 => 'Goa School Education Act',
    342 => 'Goa State Reorganization Act, 1987',
    385 => 'Goa Tax on Entry of Goods Act, 2000',
    314 => 'Goa Tax on Luxuries(Hotel &Lodg)Act 1988',
    348 => 'Goa Tourist Places (Protection & Maintenance) Act, 2001',
    347 => 'Goa University Act, 1994',
    364 => 'Goa Vexatious Litigation (Prevention) Act., 2007',
    321 => 'Goa. D.D Agricultural Tenancy Act 1964',
    316 => 'Grant-in-Aid Code of Sec.School.Coll.etc',
    6 => 'Guardian and Wards Act',
    8 => 'Hindu Marriage Act',
    380 => 'IMMORAL TRAFFIC (PREVENTION) ACT (ITPA), 1956',
    406 => 'Import and Export (Control) Act, 1947',
    32 => 'Income Tax Act, 1961',
    5 => 'Indian Arbitration Act',
    11 => 'Indian Citizenship Act',
    74 => 'Indian Constitution Act',
    75 => 'Indian Contract Act',
    9 => 'Indian Divorce Act',
    362 => 'Indian Easements Act',
    59 => 'Indian Electricity Act',
    83 => 'INDIAN LIMITATION ACT OF 1963',
    46 => 'Indian Medical Council Act- 1956',
    202 => 'Indian Penal Code',
    3 => 'Indian Railways Act,1890',
    81 => 'Indian Registration Act, 1908',
    7 => 'Indian Succession Act',
    404 => 'Indian Telegraph Act, 1885',
    20 => 'Industrial Dispute Act, 1947.',
    31 => 'Industrial Employment (Standing O.) Act',
    318 => 'Inventory Matters',
    13 => 'Land Acquisition Act',
    397 => 'Limitation Act',
    44 => 'M.R.T.U. & P.U.L.P. Act',
    311 => 'Mah. Co-op. Societies Act to Goa D.D',
    86 => 'Maharashtra Co-op. Soc. Act',
    371 => 'Maharashtra Co-operative Societies Act 1960',
    38 => 'Major Port Trusts Act',
    358 => 'Mamlatdar\'s Courts Act, 1906',
    70 => 'Merchant Shipping Act, 1958',
    16 => 'Mines & Minerals (Reg. & Devolp) Act',
    21 => 'Minimum Wages Act, 1948.',
    36 => 'Motor Vehicle Act',
    4 => 'Motor Vehicles Act,1939',
    370 => 'Multi State Co-Operative Socities Act 2002',
    203 => 'N.D.P.S. Act,1985',
    40 => 'Negotiable Instruments Act',
    0 => 'Unknown',
    405 => 'Patents Act, 1970',
    25 => 'Payment of Wages Act',
    353 => 'PORTUGUESE CIVIL CODE',
    43 => 'Presidency Small Causes Court Act',
    375 => 'Prevention of Food Adulteration Act, 1954',
    372 => 'Protection of Women from Domestic Violence Act, 05',
    409 => 'Provision of the Families Laws of Goa',
    17 => 'Public Premises (Eviction) Act',
    37 => 'Railways Act',
    52 => 'Rent Act',
    391 => 'Representation of the People Act, 1951',
    10 => 'Reqn.& Acqn.of Immoveable Property Act',
    367 => 'Right to Information Act',
    337 => 'Rules of P&C of Business of Goa State L.Assembly(Second Edition)1967',
    47 => 'S.C. & S.T. Orders (Amendment) Act.',
    19 => 'Secondary School Code',
    386 => 'Securitisation & Reconstruction of Financial Assests & Enforcements of Securities Interests Act 2002',
    87 => 'Service Matter',
    41 => 'Sick Textile Undertakings Act',
    381 => 'SLUM AREAS (IMPROVEMENT & CLEARANCE) ACT, 1956',
    407 => 'Special Economic Zone Act, 2005',
    42 => 'Specific Relief Act',
    50 => 'Standards of Weights & Measures Act-1976',
    357 => 'Suits Valuation Act, 1887',
    78 => 'The Air Pollution Control Act, 1981',
    63 => 'The Central Excise Act, 1944',
    64 => 'The Central Excise Rules, 1944',
    403 => 'The Cinematograph Act, 1952',
    387 => 'The City of Panaji Corporation Act, 2002',
    77 => 'The Contempt of Courts Act, 1971',
    12 => 'The Copy Right Act',
    393 => 'The Dock Workers (Regulation of Employment) (inapplicability to Major Ports) Act, 1997',
    65 => 'The Drugs & Cosmetics Act, 1940',
    66 => 'The Drugs & Cosmetics Rules, 1945',
    58 => 'The Environment Protectin Act, 1986',
    379 => 'THE GOA ANIMAL PRESERVATION ACT, 1995',
    378 => 'The Goa Cess on Fluid Milk (Control) Act, 2000',
    408 => 'The Goa Co-operative Societies Act, 2001',
    345 => 'The Goa Panchayat Raj Act, 1993',
    339 => 'The Goa Panchayat Raj Act, 1994',
    341 => 'The Goa Preservation of Trees Act, 1984',
    344 => 'The Goa Public Men\'s Corruption(Investigation & Inquiries)Act,1988',
    395 => 'The Goa Tax on Infrastructure Act, 2009',
    338 => 'The Goa University Act, 1984',
    374 => 'The Goa, Daman & Diu Fire Force Act, 1986',
    368 => 'The Human Right Act, 1993',
    390 => 'The Indian Fisheries Act,1897 and The Goa Fisheries Rules,1981',
    76 => 'The Inland Vessels Act, 1917',
    89 => 'The Maharashtra Agricultural Produce Marketing(Regulation)Act,1963',
    361 => 'The Marine Insurance Act',
    62 => 'The Medical & Toilet Preparations (Excise Duties) Rules, 1956',
    61 => 'The Medical & Toilet Preparations(Excise Duties) Act, 1955',
    22 => 'The Payment of Bonus Act, 1965.',
    23 => 'The Payment of Gratuity Act',
    60 => 'The Ports Act, 1908',
    363 => 'The Prevention of Corruption Act',
    411 => 'THE PROBATION OF OFFENDERS ACT',
    325 => 'The State Agricultural Credit Corporations Act, 1968',
    382 => 'The State Financial Corporation Act, 1951',
    56 => 'The University Grants Commission Act, 1956',
    389 => 'The Wakf Act, 1995',
    29 => 'Trade Unions Act, 1926',
    45 => 'Transfer of Property Act',
    55 => 'Unlawful Activities (prevention) Act, 1967',
    14 => 'Urban & Agricultural Land Ceiling Act',
    49 => 'Urban Land CC & RD Act 1976',
    69 => 'Water(Prevention & Control of Pollution) Act, 1974',
    33 => 'Wealth Tax Act, 1957',
    384 => 'Wild Life Protection Act, 1972',
    24 => 'Workmen\'s Compensation Act'
);

for ($year = date("Y"); $year < (date("Y")+1); $year++) { 
    foreach ($court_act_codes as $code => $court_act) {
        scrape($year, $code, $court_act);
    }
}
?>