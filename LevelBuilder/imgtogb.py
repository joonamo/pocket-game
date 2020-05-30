# Many functions in this file has been copied over from SimonLarsen's pyimgtogb
# You can find the original repo at https://github.com/SimonLarsen/pyimgtogb

import png
import numpy as np
import itertools

def convert_tile(data, x, y):
  px, py = x*8, y*8
  td = data[px:px+8, py:py+8]

  out = []
  for iy in range(8):
    b0, b1 = 0, 0
    for ix in range(8):
      v = td[ix, iy]

      b0 |= (v & 1) << (7 - ix)
      b1 |= ((v & 2) >> 1) << (7 - ix)

    out.append(b0)
    out.append(b1)
  return tuple(out)

def read_palette_image(path, colors):
  source = png.Reader(path)
  width, height, data_map, meta = source.read()
  palette_map = []

  if width != 4:
    raise ValueError("Palette image must be 4 pixels wide.")
  if "palette" not in meta:
    raise ValueError("Palette image must be indexed.")

  data = np.array(list(data_map)).transpose()

  # remap colors
  color_map = {}
  for i in range(len(meta["palette"])):
    c = meta["palette"][i]
    if c in colors:
      color_map[i] = colors.index(c)
    else:
      color_map[i] = len(colors)
      colors.append(c)

  for iy in range(height):
    x = list(color_map[i] for i in data[:,iy])
    palette_map.append(x)

  return colors, palette_map

def make_color_palettes(data, colors, palette_map, tiles_x, tiles_y):
	palettes = []
	for y in range(tiles_y):
		for x in range(tiles_x):
			px, py = x*8, y*8
			td = data[px:px+8, py:py+8]
			values = np.unique(td)
			if len(values) > 4:
				raise ValueError("Tile ({},{}) contains more than 4 different colors.".format(x, y))

			index = -1
			for i in range(len(palette_map)):
				noverlap = sum(v in palette_map[i] for v in values)
				if len(palette_map[i]) + len(values) - noverlap <= 4:
					index = i
					break

			if index == -1:
				index = len(palette_map)
				palette_map.append([])

			for v in values:
				if v not in palette_map[index]:
					palette_map[index].append(v)

			palettes.append(index)

	return palettes, palette_map

def rgb_to_5bit(r, g, b):
  r = round(r  / 255 * 31)
  g = round(g  / 255 * 31)
  b = round(b  / 255 * 31)
  return r + (g << 5) + (b << 10)

def convert_tile_color(data, palette, x, y):
	m = {}
	for i in range(len(palette)):
		m[palette[i]] = i

	px, py = x*8, y*8
	td = data[px:px+8, py:py+8]

	out = []
	for iy in range(8):
		b0, b1 = 0, 0
		for ix in range(8):
			v = m[td[ix, iy]]

			b0 |= (v & 1) << (7 - ix)
			b1 |= ((v & 2) >> 1) << (7 - ix)

		out.append(b0)
		out.append(b1)
	return tuple(out)

def read_png(path, s8x16 = False, color = False, include_palette = False):
  palette_offset = 0
  source = png.Reader(path)
  width, height, data_map, meta = source.read()

  data = np.array(list(data_map)).transpose()
  colors = meta["palette"]

  tiles_x = width // 8
  tiles_y = height // 8

  palettes, palette_data = None, None

  if s8x16:
    tileorder = [(x // 2, y + x % 2) for y in range(0, tiles_y, 2) for x in range(tiles_x*2)]
  else:
    tileorder = [(x, y) for y in range(tiles_y) for x in range(tiles_x)]

  if color:
    palette_map = []
    if include_palette:
      colors, palette_map = read_palette_image(include_palette, colors)

    palettes, palette_map = make_color_palettes(data, colors, palette_map, tiles_x, tiles_y)
    tile_data = [convert_tile_color(data, palette_map[palettes[t[0]+t[1]*tiles_x]], t[0], t[1]) for t in tileorder]
    tile_data_length = len(tile_data)
    palette_data = []
    for m in palette_map:
      for i in range(4):
        if i < len(m):
          palette_data.append(rgb_to_5bit(*colors[m[i]]))
        else:
          palette_data.append(0)

  else:
    tile_data = [convert_tile(data, t[0], t[1]) for t in tileorder]
    tile_data_length = len(tile_data)

    # if args.dx:
    #   source_dx = png.Reader(args.dx)
    #   width_dx, height_dx, data_map_dx, meta_dx = source_dx.read()

    #   if width_dx != width or height_dx != height:
    #     raise ValueError("Dimension of DX reference image does not match input.")
    #   if "palette" not in meta_dx:
    #     raise ValueError("DX reference PNG image is not indexed.")

    #   data_dx = np.array(list(data_map_dx)).transpose()

    #   palettes, palette_data = make_dx_palettes(data, data_dx, meta_dx["palette"], tiles_x, tiles_y)

  if palettes != None:
    palettes = [i + palette_offset for i in palettes]

  tile_data = np.fromiter(itertools.chain.from_iterable(tile_data), np.uint8)
  return (tile_data, palettes)

    # if args.correct_lcd:
    #   lcd_map = lcd.build_lcd_map()
    #   palette_data = [lcd.find_best(c, lcd_map) for c in palette_data]

# Licence
# MIT License

# Copyright (c) 2018 Simon Larsen

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.