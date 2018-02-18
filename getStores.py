#!/usr/bin/python3

import requests, json, sys
from optparse import OptionParser
#  curl 'https://www.mcdonalds.de/search' -H 'Host: www.mcdonalds.de' -H 'User-Agent: Test/Test' -H 
# 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Accept-Language: en-US,en;q=0.5' 
# --compressed -H 'Referer: https://www.mcdonalds.de/restaurant-suche' -H 'Content-Type: 
# application/x-www-form-urlencoded; charset=UTF-8' -H 'X-Requested-With: XMLHttpRequest' -H  -H 
# 'Connection: keep-alive' --data 'longitude=10.26517&latitude=51.9482&radius=10000000000000'

from helpers import convertOpeningHours

searchUrl = 'https://www.mcdonalds.de/search'

headers = {
  'Host' : 'www.mcdonalds.de',
  'User-Agent' : 'restaurantSearch.py/1.0',
  'Accept' : 'application/json, text/javascript, */*; q=0.01',
  'Referer' : 'https://www.mcdonalds.de/restaurant-suche',
  'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
  'X-Requested-With' : 'XMLHttpRequest',
  'Connection' : 'close'
}

payload = {
  # see https://de.wikipedia.org/wiki/Mittelpunkt_Deutschlands#Mittelpunkt_eines_von_Breiten-_und_L%C3%A4ngengraden_begrenzten_Gebietes
  'latitude' : '51.9482',
  'longitude' : '10.26517',
  'radius' : 100000000
}

parser = OptionParser()
parser.add_option("-p", "--no-properties",
                  help="Don't add properties to the output", action="store_true",
                  dest="removeProperties", default=False)
parser.add_option("-q", "--quiet",
                  action="store_false", dest="verbose", default=True,
                  help="don't print status messages to stdout")

(options, args) = parser.parse_args()

request = requests.post(searchUrl, data=payload, headers=headers)
if request.status_code != requests.codes.ok:
  sys.exit('Error fetching data');

data = json.loads(request.text)
geojson = {
  'type' : 'FeatureCollection',
  'features' : []
}

blacklist = [ 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',
  'latitude', 'longitude', 'city', 'postalCode', 'street', 'name1', 'name2' ]

for restaurantObj in data['restaurantList']:
  restaurant = restaurantObj['restaurant']
  geojsonobj = {
    'type' : 'Feature',
    'geometry' : {
      'type' : 'point',
      'coordinates' : [restaurant['latitude'], restaurant['longitude']],
    },
    'properties': {}
  }

  if not options.removeProperties:
    geojsonobj['properties'].update({
      'opening_hours' : convertOpeningHours(restaurant),
      'addr:city' : restaurant['city'],
      'addr:postcode' : restaurant['postalCode'],
      # todo separate street and housenumber somehow
      'addr:full' : restaurant['street'],
      'addr:country' : 'DE',
      'name' : restaurant['name1'],
      'operator' : restaurant['name2']
    })
    for key,value in restaurant.items():
      if key not in blacklist:
        geojsonobj['properties'][key] = value

  geojson['features'].append(geojsonobj)

print(json.dumps(geojson))
