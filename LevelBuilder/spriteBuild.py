from imgtogb import read_png
from sourceGenerator import write_tiledata

import argparse

def main():
  parser = argparse.ArgumentParser(description="Compiles tiled to gb")
  parser.add_argument("infile", help="level file", type=str)
  parser.add_argument("outfile", help="Output file", type=str)
  parser.add_argument("-b", "--bank", help="bank", type=str, default="3")
  parser.add_argument("-pr", "--palette_reference", help="Palette reference file", type=str, default=None)

  args = parser.parse_args()
  infile = args.infile
  outfile = args.outfile
  bank = args.bank
  palette_reference = args.palette_reference
  sprite_name = args.infile.split("/")[-1].split(".")[0]

  (tile_data, palettes, palette_data) = read_png(
    infile,
    False,
    True,
    palette_reference)
  
  tiles_data = []
  for idx, palette in enumerate(palettes):
    start_offset = idx * 16
    data = tile_data[start_offset : (start_offset + 16)]
    tiles_data.append({
      "name": sprite_name + "@" + str(idx),
      "hexdata": [hex(v).rjust(4, " ") for v in tile_data],
      "palette_idx": palette
    })

  write_tiledata(outfile, bank, tiles_data, sprite_name)

if __name__ == "__main__":
  main()