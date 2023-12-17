# BluOS Scrobbler
# BluOS API: https://bluos.net/wp-content/uploads/2020/06/Custom-Integration-API-v1.0.pdf

import requests
import xml.etree.cElementTree as et
import datetime
import time
import myconfig
import re
import sys
import inkyimg
import inkyconvert
import shutil

BLUOS_STATUS_URL = 'http://%s:%d/Status' % (myconfig.BLUOS_IP, myconfig.BLUOS_PORT)

song = {}
song['etag'] = ''
song['timeout'] = 300

while True:
	try:
		if song['etag'] == '':
			r = requests.get(BLUOS_STATUS_URL)
		else:
			r = requests.get('%s?timeout=%d&etag=%s' % (BLUOS_STATUS_URL, song['timeout'], song['etag']))
	except:
		time.sleep(10)
		continue
	#print(r.text)
	root=et.fromstring(r.text)

	try:
		song['etag'] = root.attrib['etag']
		song['service'] = root.find('service').text

		song['title1'] = root.find('title1').text
		song['title2'] = root.find('title2').text
		song['title3'] = root.find('title3').text

		if ',' in song['title2']:
			song['title2'] = song['title2'].split(',')[0]

		song['title1'] = re.sub(r'\(.*?Remaster.*?\)','', song['title1'])
		song['title1'] = song['title1'].strip()

		song['title2'] = re.sub(r'\(.*?Remaster.*?\)','', song['title2'])
		song['title2'] = song['title2'].strip()

		song['title3'] = re.sub(r'\(.*?Remaster.*?\)','', song['title3'])
		song['title3'] = song['title3'].strip()

		song['state'] = root.find('state').text
		song['secs'] = int(root.find('secs').text)
		song['service'] = root.find('serviceName').text
		song['image'] = root.find('image').text
	except AttributeError:
		#print(r.text)
		continue

	with open('state', 'w') as f:
		f.write(song['state'] + '\n')

	if song['state'] in ['play', 'stream']:
		print(song)

		if song['service'] == 'TuneIn':
			song['title1'] = ''

		if song['image'].startswith('http'):
			url = song['image']
		else:
			url = 'http://%s:%d%s' % (myconfig.BLUOS_IP, myconfig.BLUOS_PORT, song['image'])
		print(url)
		res = requests.get(url, stream = True)

		if res.status_code == 200:
			with open('cover.jpg','wb') as f:
				shutil.copyfileobj(res.raw, f)
			inkyconvert.convert('cover.jpg','converted.png')
		else:
			print('Image could not be retrieved: $s' % url)

		inkyimg.display_song('converted.png', song['title1'], song['title2'], song['title3'])
		time.sleep(30)

