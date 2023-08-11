import time
import urllib.parse
import requests
import os
import pytumblr
import creds

# Variables

client = pytumblr.TumblrRestClient(
  creds.consumer_key,
  creds.consumer_secret,
  creds.access_token,
  creds.access_secret
)
posturl = '&zoom=20&maptype=satellite&size=640x640&key='
baseurl = 'https://maps.googleapis.com/maps/api/staticmap?center='
usedfile = 'used.txt'

# Check if used works

if not os.path.exists(usedfile):
    print('Creating Used File')
    with open(usedfile, 'w') as g:
        g.write('0')


# Establishing lists

# List of all coordinates

with open('shufflecoords.csv', newline='')as f:
    coordrows = f.readlines()
    coordlinesx = [coordrow.rstrip() for coordrow in coordrows]

# index of last used coordinates

with open(usedfile, 'r') as fd:
    usedrows = int(fd.readline())

# Removing used from all coords

print('Removing used')

coordlines = coordlinesx[usedrows::]

print(f'Untweeted: {len(coordlines)}')

# Start of actual tweeting function

print('Beginning')

for coord in coordlines:

    print(f'Posting {str(coord)}')

    # Update used

    usedrows = int(usedrows) + 1

    with open(usedfile, 'w') as out:
        out.write(str(usedrows))
    print('Used file updated')


    # Generate Content
    try:
        text = coord.split(',')
        lat = str(text[0])
        lon = str(text[1])
        locate = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lon}&result_type=locality|administrative_area_level_2&key={creds.maps_api}')
        locatejson = locate.json()
        if locatejson['results'][0]['address_components'][0]['types'][0] == 'locality':
            location = locatejson['results'][0]['address_components'][0]['long_name'] + ', ' + locatejson['results'][1]['formatted_address']
        else:
            location = locatejson['results'][0]['formatted_address']
        url = (baseurl + urllib.parse.quote_plus((str(coord))) + posturl + creds.maps_api)
        response = requests.get(url)
        imagesave = f'tempscreenshot{len(coordlines)}.png'
        with open(f'{imagesave}', 'wb') as image:
            image.write(response.content)
        print('Image saved')

        # Twitter... I mean Tumblr API stuff

        image_path = f'tempscreenshot{len(coordlines)}.png'
        text = f'{location}\n{lat}, {lon}'
        client.create_photo('culdesacbot1', state="published", tags=["culdesac"],
                    caption=text,
                    data=image_path)
        print('Tumblr post made')

        # Delete and sleep

        os.remove(f'tempscreenshot{len(coordlines)}.png')
        print('Image deleted')

        print('Sleeping')

        time.sleep(14400)

    except Exception as e:
        print(e)
        time.sleep(1800)
        pass
