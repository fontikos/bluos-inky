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

def clean_title(title):
	if title == None: title = ''
	title = re.sub(r'\(.*?Remaster.*?\)','', title)
	title = re.sub(r'\[.*?Remaster.*?\]','', title)
	title = re.sub(r'\(.*?Mix.*?\)','', title)
	title = re.sub(r'\(.*?Edition.*?\)','', title)
	title = re.sub(r'\(.*?Live.*?\)','', title)
	title = re.sub(r'\(.*?Bonus.*?\)','', title)
	title = title.strip()
	return title

BLUOS_STATUS_URL = 'http://%s:%d/Status' % (myconfig.BLUOS_IP, myconfig.BLUOS_PORT)

song = {}
song['etag'] = ''
song['timeout'] = 300
old = ''

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

		song['title1'] = ''
		if root.find('title1') != None:
			song['title1'] = root.find('title1').text
		song['title2'] = ''
		if root.find('title2') != None:
			song['title2'] = root.find('title2').text
		song['title3'] = ''
		if root.find('title3') != None:
			song['title3'] = root.find('title3').text

		#if ',' in song['title2']:
		#	song['title2'] = song['title2'].split(',')[0]

		song['title1'] = clean_title(song['title1'])
		song['title2'] = clean_title(song['title2'])
		song['title3'] = clean_title(song['title3'])

		song['state'] = root.find('state').text
		song['secs'] = int(root.find('secs').text)
		song['serviceName'] = song['service']
		if root.find('serviceName') != None:
			song['serviceName'] = root.find('serviceName').text
		song['image'] = root.find('image').text
	except AttributeError as error:
		print(type(error).__name__, error)
		#print(r.text)
		continue

	with open('state', 'w') as f:
		f.write(song['state'] + '\n')

	if song['state'] in ['play', 'stream']:

		if song['service'] == 'TuneIn':
			song['title1'] = ''

		if song['image'].startswith('http'):
			url = song['image']
		else:
			url = 'http://%s:%d%s' % (myconfig.BLUOS_IP, myconfig.BLUOS_PORT, song['image'])
		res = requests.get(url, stream = True)
		#print(url)

		if res.status_code == 200:
			with open('cover.jpg','wb') as f:
				shutil.copyfileobj(res.raw, f)
			if inkyconvert.convert('cover.jpg','converted.png') == 0:
				imgpath = 'converted.png'
			else:
				imgpath = None
		else:
			print('Image could not be retrieved: $s' % url)

		if url + song['title1'] + song['title2'] + song['title3'] != old:
			old = url + song['title1'] + song['title2'] + song['title3']
			print(song)
			inkyimg.display_song('converted.png', song['title1'], song['title2'], song['title3'])
			time.sleep(10)
