import urllib.parse
import requests
import os
import credsbsky
from atproto import Client

handle = credsbsky.BLUESKY_HANDLE
password = credsbsky.BLUESKY_PASSWORD


endpoint = "https://bsky.social"
posturl = '&zoom=20&maptype=satellite&size=640x640&key='
baseurl = 'https://maps.googleapis.com/maps/api/staticmap?center='
nextfile = 'next.txt'

if not os.path.exists(nextfile):
    print('Creating Used File')
    with open(nextfile, 'w') as g:
        g.write('0')

with open('shufflecoords.csv', newline='')as f:
    coordrows = f.readlines()
    coordlinesx = [coordrow.rstrip() for coordrow in coordrows]

with open(nextfile, 'r') as fd:
    nextindex = int(fd.readline())

coord = coordrows[nextindex].rstrip()

print(f'Posting {str(coord)} at index {nextindex}')

next = int(nextindex) + 1

with open(nextfile, 'w') as out:
    out.write(str(next))

print('Used file updated')

try:
    # Parsing
    text = coord.split(',')
    lat = str(text[0])
    lon = str(text[1])

    # GCP
    locate = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lon}&result_type=locality|administrative_area_level_2&key={credsbsky.MAPS_API}')
    locatejson = locate.json()
    if locatejson['results'][0]['address_components'][0]['types'][0] == 'locality':
        location = locatejson['results'][0]['address_components'][0]['long_name'] + ', ' + locatejson['results'][1]['formatted_address']
    else:
        location = locatejson['results'][0]['formatted_address']
    url = (baseurl + urllib.parse.quote_plus((str(coord))) + posturl + credsbsky.MAPS_API)
    response = requests.get(url)
    image_bytes = response.content

    # Metadata parsing
    text = f'{location}\n{lat}, {lon}'
    alt=f"Cul-de-sac located in {location}"

    # BlueSky
    client = Client(endpoint)
    client.login(handle, password)
    upload_response = client.upload_blob(image_bytes)
    client.send_image(text=text, image=image_bytes, image_alt=alt)
    print(f'BlueSkeet made')

except Exception as e:
    print(e)
