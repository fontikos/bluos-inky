#!/usr/bin/env python3
# Modified from https://github.com/RubenLagrouw/inkyconv
from os import remove
from PIL import Image
import subprocess

def convert(imgpath, outpath, example='InkypHAT-212x104.png', dimensions=(122, 122)):
    subprocess.run(
         'convert {in_file} -auto-orient -geometry {x}x{y}^ -gravity center -crop {x}x{y}+0+0 -strip -type Palette -remap {ex} -dither FloydSteinberg temp.png'
        .format(in_file=imgpath, x=dimensions[0], y=dimensions[1], ex=example), shell=True)

    img = Image.open("temp.png")
    cR = [255, 0, 0]
    cB = [0, 0, 0]
    cW = [255, 255, 255]

    new_pixdata = []
    old_pixdata = img.getdata()
    palette_old = img.getpalette()

    if palette_old == None: # Grayscale Image

      for pix in old_pixdata:
        if pix == 0:
          new_pixdata.append(0)
        else:
          new_pixdata.append(1)
      img = Image.new("P", dimensions)

      #img.putdata(newpix)
      #img.putpalette(cW + cB + cR)
      #img.save('converted.png')
      #return -1

    else: # Coloured Image

        p_conv = {0: palette_old[0:3],
                1: palette_old[3:6],
                2: palette_old[6:9]}

        # p_target = {0: cW,
        #             1: cB,
        #             2: cR}

        for pix in old_pixdata:
            if pix not in p_conv:
                print('Pixel out of range: {}'.format(pix))
                new_pixdata.append(0)
            elif p_conv[pix] == cW:
                new_pixdata.append(0)
            elif p_conv[pix] == cB:
                new_pixdata.append(1)
            elif p_conv[pix] == cR:
                new_pixdata.append(2)

    img.putdata(new_pixdata)
    img.putpalette(cW + cB + cR)  # Goal palette

    remove('temp.png')
    if not outpath.lower().endswith('.png'):
        outpath += '.png'
    img.save(outpath)
    return 0

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print('Improper amount of arguments')
        sys.exit(-1)
    convert(sys.argv[1], sys.argv[2])
