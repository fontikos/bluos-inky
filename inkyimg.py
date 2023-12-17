
from inky.auto import auto
from font_fredoka_one import FredokaOne
from font_source_sans_pro import SourceSansPro
from PIL import Image, ImageFont, ImageDraw
import sys
import re

def split_string(text, font, inky_display):
	a = ['']
	aidx = 0
	split = text.split()
	i = 0
	while i < len(split):
		word = split[i]
		if a[aidx] == '' and font.getsize(word)[0] > inky_display.WIDTH / 2:
			j=len(word)
			while font.getsize(word[:j-1] + '.')[0] > inky_display.WIDTH / 2:
				j = j - 1
			a[aidx] = a[aidx] + word[:j] + '.'
		elif a[aidx] == '' and font.getsize(a[aidx] + word)[0] <= inky_display.WIDTH / 2:
			a[aidx] = a[aidx] + word
		elif a[aidx] != '' and font.getsize(a[aidx] + ' ' + word)[0] <= inky_display.WIDTH / 2:
			a[aidx] = a[aidx] + ' ' + word
		else:
			aidx = aidx + 1
			if aidx >= 3:
				break
			a.append('')
			i = i - 1
		i = i + 1
	return a

def add_line(text, row, h, font, inky_display, draw):
	x = inky_display.WIDTH / 2

	y = (row) * (inky_display.HEIGHT / 8) - (h / 2)
	draw.text((x, y), text[0], inky_display.RED, font)
	if len(text) == 1 or row == 7: return row+1

	y = (row+1) * (inky_display.HEIGHT / 8) - (h / 2)
	draw.text((x, y), text[1], inky_display.RED, font)
	if len(text) == 2 or row == 6: return row+2

	y = (row+2) * (inky_display.HEIGHT / 8) - (h / 2)
	draw.text((x, y), text[2], inky_display.RED, font)
	return row+3

def display_song(cover, title1, title2, title3):

	#print('to display', title1, title2, title3)
	inky_display = auto()
	inky_display.set_border(inky_display.WHITE)
	inky_display.h_flip = True
	inky_display.v_flip = True

	img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
	left = Image.open(cover)
	img.paste(left)
	draw = ImageDraw.Draw(img)

	font = ImageFont.truetype(FredokaOne, 18)
	if re.findall(r"[α-ωΑ-Ω]", title1+title2+title3) != []:
		font = ImageFont.truetype(SourceSansPro, 14)

	t1 = split_string(title1, font, inky_display)
	print(t1)

	t2 = split_string(title2, font, inky_display)
	print(t2)

	t3 = split_string(title3, font, inky_display)
	print(t3)

	w, h = font.getsize(title1+title2+title3)

	row = add_line(t1, 1, h, font, inky_display, draw)
	row = add_line(t2, row + 1, h, font, inky_display, draw)
	row = add_line(t3, row + 1, h, font, inky_display, draw)

	inky_display.set_image(img)
	inky_display.show()
