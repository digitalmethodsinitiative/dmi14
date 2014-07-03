Detect geo names in tweets
==========================

* Get locations from http://download.geonames.org/export/dump/allCountries.zip (and unzip it and put the resulting file in this directory).
* Edit and run geoParser.php to retrieve a filtered list of geonames and their alternate spellings.
* Retrieve a list of words via dmi-tcat > word frequency and save that to this dir.
* Run 'perl transform.pl GEO_FILE.txt WORD_FREQUENCY.txt > detected_names.txt'
* The first colummn of detected_names.org will contain the alternate name detected, the second will contain the canonical name, the third column will again contain the alternate name detected, the fourth column will contain the frequency from WORD_FREQUENCY.txt.
