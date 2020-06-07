from imgtogb import generate_palette_from_reference_strip
from sourceGenerator import write_palette_data

import argparse

def main():
  parser = argparse.ArgumentParser(description="Compiles tiled to gb")
  parser.add_argument("infile", help="level file", type=str)
  parser.add_argument("outfile", help="Output file", type=str)
  parser.add_argument("-b", "--bank", help="bank", type=str, default="3")

  args = parser.parse_args()
  infile = args.infile
  outfile = args.outfile
  bank = args.bank
  palette_name = args.infile.split("/")[-1].split(".")[0]

  palettes = generate_palette_from_reference_strip(infile)
  write_palette_data(outfile, bank, palette_name, palettes)

if __name__ == "__main__":
    main()
