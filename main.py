import time
import urllib.parse
import requests
import os
import tweepy
import creds

# Variables

auth = tweepy.OAuthHandler(creds.consumer_key, creds.consumer_secret)
auth.set_access_token(creds.access_token, creds.access_secret)
posturl = '&zoom=20&maptype=satellite&size=640x640&key='
baseurl = 'https://maps.googleapis.com/maps/api/staticmap?center='
api = tweepy.API(auth)
usedfile = 'used2.txt'

sess = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries=20)
sess.mount('http://', adapter)

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

    print(f'Tweeting {str(coord)}')

    # Update used

    usedrows = int(usedrows) + 1

    with open(usedfile, 'w') as out:
        out.write(str(usedrows))
    print('Used file updated')


    # Generate Content
    try:
        text = coord.split(',')
        lat = (text[0])
        lon = str(text[1])
        nom = f'https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&zoom=11&format=json'
        locate = sess.get(nom)
        json = locate.json()
        location = json['display_name']
        url = (baseurl + urllib.parse.quote_plus((str(coord))) + posturl + creds.maps_api)
        response = requests.get(url)
        imagesave = f'tempscreenshot{len(coordlines)}.png'
        with open(f'{imagesave}', 'wb') as image:
            image.write(response.content)
        print('Image saved')

        # Twitter API stuff

        image_path = f'tempscreenshot{len(coordlines)}.png'
        tweet_text = f'{location}\n{lat}, {lon}'
        api.update_status_with_media(tweet_text, image_path)
        print('Tweet posted')

        # Delete and sleep

        os.remove(f'tempscreenshot{len(coordlines)}.png')
        print('Image deleted')

        # Don't delete this :-) !

        print('Sleeping')

        time.sleep(14400)

    except Exception as e:
        print(e.message, e.args)
        time.sleep(1200)
        pass
