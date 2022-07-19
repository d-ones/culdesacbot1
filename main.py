import random
import time
import urllib.parse

prefix = 'https://www.google.com/maps/@?api=1&map_action=map&center='
suffix = '&zoom=20&basemap=satellite'

with open('culdesaccoords2021.csv', newline='')as f:
    lines = f.readlines()

for line in lines:
            print(str(659799 - len(lines)) + ' of 659798')
            coord = random.choice(lines)
            print(prefix + urllib.parse.quote_plus((str(coord))) + suffix)
            lines.remove(coord)
            time.sleep(5)