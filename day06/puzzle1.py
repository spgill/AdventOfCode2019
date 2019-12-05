#!/usr/bin/env python3
import requests, time, urllib

url = "https://print.spgill.me:9500"
img_url = "https://i.redd.it/255iuxdit0g21.jpg"
img = urllib.urlopen(img_url)


while 1:
    x = requests.post(url, files=img)
    time.sleep(3)
