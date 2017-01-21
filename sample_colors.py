# -*- coding: utf-8 -*-

# Lightpad - sample_colors.py
# Created by Vinyl Darkscratch, Light Apacha, and WhoovesPON3, ©2017 Nightwave Studios.
# Additional assistance by Eric Busch (Origami1105).

from PIL import Image

output = "\n\nwxColor velocitycolors[] = {\n\t"

def do_it(img):
	o = []
	for y in range(36, img.height, 74):
		for x in range(36, img.width, 74):
			o.append("wxColor(%d, %d, %d)" %img.getpixel((x, y)))
	return o

output += ",\n\t".join(
	do_it(Image.open('references/rgbcolors1.png').convert('RGB')) +
	do_it(Image.open('references/rgbcolors2.png').convert('RGB'))
) + "\n};\n"

cpp_file = open("Colors.cpp", "w")
cpp_tmpl = open("Colors_template.cpp", "r")

for line in cpp_tmpl:
	if line.strip() == "!XXX!":
		cpp_file.write(output)
	else:
		cpp_file.write(line)

cpp_file.close()
cpp_tmpl.close()