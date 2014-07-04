# Pinterest HTML resolver
-------------------------

This python (2.7) script will create a GeoJSON file from the HTML sourcefiles of boards on Pinterest with _pins_ as instances. This allows the pins to be viewable on a map. It uses the JSON in the HTML. 

## Pin properties

The following properties will be added to the GeoJSON file:

* description
* longitude
* latitude
* description
* user_name
* user_full_name
* user_id
* city_name
* country_name
* foursquare_category
* repin_count
* is_repin
* board_url
* pin_url
* date
* file_name
* board_description
* board_follower_count
* pin_language

## How to use

Make sure that the script is in the same folder as a `html_sources` containing raw html source from a pinterest board. Then the script can be ran using python 2.7. Run `python pinterest_html_resolver -k` to additionally export the locations to Google Earths KMZ fileformat.


## Required python modules:

* simplekml
* guess_language

Both can be installed using `pip install <module name >`.

*This script was not tested on windows (and likely will not work due to the path seperator)*