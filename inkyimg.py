
from inky.auto import auto
from font_fredoka_one import FredokaOne
from font_source_sans_pro import SourceSansPro
from PIL import Image, ImageFont, ImageDraw
import sys
import re

SPACEFACTOR = 0.35
LINEFACTOR = 0.75

def split_string(text, font, inky_display):
	if text == '':
		return []
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
			a.append('')
			i = i - 1
		i = i + 1
	return a

def add_line(text, y, h, font, inky_display, draw, max=3):
	space = h*SPACEFACTOR
	if text == []:
		return y
	x = inky_display.WIDTH / 2

	for i in range(max):
		if y+(h*LINEFACTOR) >= inky_display.HEIGHT:
			return y + space
		draw.text((x, y), text[i], inky_display.RED, font)
		y = y+(h*LINEFACTOR)
		if len(text) == 1+i:
			break
	return y + space

def display_song(cover, title1, title2, title3):
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
	t2 = split_string(title2, font, inky_display)
	t3 = split_string(title3, font, inky_display)

	print(t1, t2, t3)

	w, h = font.getsize(title1+title2+title3)

	max = 3
	if (len(t1)+len(t2)+len(t3))*(h*LINEFACTOR)+2*(h*SPACEFACTOR) <= inky_display.HEIGHT:
		max = 10

	row = add_line(t1, 0, h, font, inky_display, draw, max)
	row = add_line(t2, row, h, font, inky_display, draw, max)
	row = add_line(t3, row, h, font, inky_display, draw, max)

	inky_display.set_image(img)
	inky_display.show()
