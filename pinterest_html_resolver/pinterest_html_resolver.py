import csv
import glob
import json
import sys
import argparse

import simplekml
import guess_language

# import chronium_compact_language_detector

__author__ = 'Alexander van Someren'

#######################  Helper methods for json conversion  #########################################

def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv


def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv

######################################################################################################


def filter_geo_location(picture_data):
    file_name = picture_data['file_name']
    picture = picture_data['picture']
    location = None
    # If it contains geo-location
    if 'place' in picture['data']:
        if picture['data']['place'] is not None:
            # topLanguageName, topLanguageCode, isReliable, textBytesFound, details = chronium_compact_language_detector.detect(picture['data']['description'])
            pin_language = guess_language.guessLanguageName(picture_data['board_description'])
            if pin_language == "Afrikaans" or pin_language == "Latin" or pin_language == "Catalan":
                pin_language = "UNKNOWN"
            # extract features we want:
            location = {'longitude': picture['data']['place']['longitude'],
                        'latitude': picture['data']['place']['latitude'],
                        'description': picture['data']['description'],
                        'user_name': picture['data']['pinner']['username'],
                        'user_full_name': picture['data']['pinner']['username'],
                        'user_id': picture['data']['pinner']['id'],
                        'city_name': picture['data']['place']['locality'],
                        'country_name': picture['data']['place']['country'],
                        'foursquare_category': picture['data']['place']['category'],
                        'repin_count': picture['data']['repin_count'],
                        'is_repin': picture['data']['is_repin'],
                        'board_url': picture['data']['board']['url'],
                        'pin_url': picture['data']['link'],
                        'date': picture['data']['created_at'],
                        'board_follower_count': picture_data['board_follower_count'],
                        'board_description': picture_data['board_description'],
                        'file_name': file_name,
                        'pin_language': pin_language

            }
    return location


def get_pictures(json_data, file_name):

    pictures = []
    if len(json_data['tree']['children'][3]['children']) > 3:  # if there are pictures
        for picture in json_data['tree']['children'][3]['children'][3]['children'][0]['children']:
            board_description = json_data['tree']['data']['description']
            board_follower_count = json_data['tree']['data']['follower_count']
            pictures.append({'picture': picture, 'file_name': file_name, 'board_description': board_description,
                             'board_follower_count': board_follower_count})
    # else:  # this debug code could be turned on when something goes wrong with reading pages.
    #     sys.stdout.flush()
    #     print "Hmmm.. iets gaat een beetje raar met de json van " + file_name
    return pictures


def export_kmz(geo_tagged_pictures):
    kml = simplekml.Kml()
    for gtp in geo_tagged_pictures:
        kml.newpoint(name=gtp['description'], coords=[
            (float(gtp['longitude']), float(gtp['latitude']))])
    kml.save("testLocation.kmz")


def export_geojson(geo_tagged_pictures):
    features = []
    for gtp in geo_tagged_pictures:  # loop over geo tagged pictures
        feature = {"type": "Feature",
                   "geometry": {"type": "Point", "coordinates": [gtp['longitude'], gtp['latitude']]},
                   "properties": dict((k, gtp[k]) for k in (
                       'description',
                       'longitude',
                       'latitude',
                       'description',
                       'user_name',
                       'user_full_name',
                       'user_id',
                       'city_name',
                       'country_name',
                       'foursquare_category',
                       'repin_count',
                       'is_repin',
                       'board_url',
                       'pin_url',
                       'date',
                       'file_name',
                       'board_description',
                       'board_follower_count',
                       'pin_language'
                   ))
        }
        features.append(feature)
    json_dict = {"type": "FeatureCollection", "features": features}
    with open('json_data_pinterest.txt', 'w') as outfile:
        json.dump(json_dict, outfile)

# Main function
if __name__ == '__main__':

    # Parse the arguments
    parser = argparse.ArgumentParser(description='This pinterest scraper exports GeoJSON  from the html of a board. ')
    parser.add_argument("-k", "--kmz",
                        action="store_true", dest="kmz", default=False,
                        help="Also export pin coordinates to the google KMZ format (for viewing in Google Earth.")
    args = parser.parse_args()

    files_names = glob.glob(
        'html_sources/*.html')  # select board html files (now all html files that are present in current folder)

    print "Starting to extract json from html..."

    files_processed = 0  # For process printing only
    geo_tagged_pictures = []  # initialize data set
    for file_name in files_names:
        with open(file_name, "r") as myfile:  # open the file
            html_file = myfile.read()
        start_json = html_file.index('"gaAccountNumbers": [') - 1  # define the starting point of relevant json
        end_json = html_file.index('"canDebug": false}') + 18  # define the end point of relevant json

        json_html = html_file[start_json:end_json]  # strip json from html

        json_data = json.loads(json_html,
                               object_hook=_decode_dict)  # convert json to dictionary/list structure in python

        pictures = get_pictures(json_data, file_name)

        geo_count = 0
        for picture in pictures:  # loop over all pictures from current board
            geo_tagged_picture = filter_geo_location(picture)  # try to get a geo tagged picture
            if geo_tagged_picture is not None:  # if the picture has geo coords
                geo_count += 1
                geo_tagged_pictures.append(geo_tagged_picture)  # add it to the list with geotagged pictures

    ##### Only for progress printing #######
        files_processed += 1
        if files_processed % 10 == 0:
            sys.stdout.flush()
            sys.stdout.write("\r" + str(round(float(files_processed) / float(len(files_names)) * 100, 1)) + "%")
    sys.stdout.flush()
    sys.stdout.write("100% \n")
    ########################################
    print "Done."
    print "Starting to extract geodata..."

    if args.kmz:
        print "Exporting KMZ..."
        export_kmz(geo_tagged_pictures)
    print "Done."

    print "Creating geoJson..."
    export_geojson(geo_tagged_pictures)

    print "All Done!"