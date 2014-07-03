<?php

$outputFile = "locationsFound.csv";
$locationFile = "allCountries.txt";
$filter = "PCLI"; // PCLI = independent political entity, i.e. countries. You can find other geocodes on http://www.geonames.org/export/codes.html

$file = file('allCountries.txt');

$csv = fopen($filename, "w");
foreach ($file as $f) {
	if ( $filter && !strstr($f, $filter))
		continue;

        $e = explode("\t", $f);
        $oname = strtolower($e[1]);
        $asciiname = strtolower($e[2]);
        $alternatenames = explode(",", strtolower($e[3]));
        $countrycode = $e[8];

        fputs($csv, "$oname\t$oname\n");
        fputs($csv, "$asciiname\t$oname\n");
        foreach ($alternatenames as $name)
            fputs($csv, "$name\t$oname\n");
}
fclose($csv);
?>

