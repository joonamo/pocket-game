from imgtogb import read_png
from sourceGenerator import write_tiledata, write_mapdata, write_palette_data

import argparse
import xml.etree.ElementTree as XET
from pathlib import Path

def main():
  parser = argparse.ArgumentParser(description="Compiles tiled to gb")
  parser.add_argument("infile", help="level file", type=str)
  parser.add_argument("outfile", help="Output file", type=str)
  parser.add_argument("-b", "--bank", help="bank", type=str, default="3")

  args = parser.parse_args()
  infile = args.infile
  outfile = args.outfile
  bank = args.bank

  root = XET.parse(infile).getroot()
  layer = root.find("layer")
  map_width = layer.attrib['width']
  map_height = layer.attrib['height']
  level_data = [int(v) for v in layer.find('data').text.replace("\n", "").split(",")]
  level_gids = set(level_data)

  tileset_gid_map = dict()
  seen_tiles_id = 0
  tiles_data = []
  unique_palettes = []
  collision_tiles = []
  collision_down_tiles = []

  tilemap_dir = Path(infile).parent
  for tilemap in root.findall("tileset"):
    tilemap_gid = int(tilemap.attrib["firstgid"])
    tilemap_path = tilemap_dir.joinpath(tilemap.attrib["source"])
    print("processing tileset", tilemap_path)
    tileroot = XET.parse(tilemap_path).getroot()
    root_image = tileroot.find("image")
    if root_image is not None:
      # This is single-image tiled map
      root_name = root_image.attrib["source"]
      (root_tile_data, root_palettes, root_palette_data) = read_png(
        str(tilemap_path.parent.joinpath(root_name)),
        False,
        True)
    for tile in tileroot.findall("tile"):
      tile_id = int(tile.attrib["id"])
      tile_gid = tilemap_gid + tile_id
      if not tile_gid in level_gids:
        continue
      tileset_gid_map[tile_gid] = seen_tiles_id
      if tile.find("properties/property[@name='collision'][@value='true']") is not None:
        collision_tiles.append(seen_tiles_id)
      elif tile.find("properties/property[@name='collision_down'][@value='true']") is not None:
        collision_down_tiles.append(seen_tiles_id)
      if (root_image is None):
        image = tile.find("image")
        name = image.attrib["source"]
        (tile_data, palettes, palette_data) = read_png(
          str(tilemap_path.parent.joinpath(name)),
          False,
          True)
      else:
        name = root_name + "@" + str(tile_id)
        start_offset = tile_id * 16
        tile_data = root_tile_data[start_offset : (start_offset + 16)]
        palette_start_offset = root_palettes[tile_id]
        palette_data = root_palette_data[palette_start_offset : palette_start_offset + 4]

      if palette_data in unique_palettes:
        palette_idx = unique_palettes.index(palette_data)
      else:
        palette_idx = len(unique_palettes)
        unique_palettes.append(palette_data)

      tile_entry = {
        "name": name + " gid " + str(tile_gid),
        "hexdata": [hex(v).rjust(4, " ") for v in tile_data],
        "palette_idx": palette_idx
      }
      tiles_data.append(tile_entry)
      seen_tiles_id += 1
      
  map_name = args.infile.split("/")[-1].split(".")[0]
  map_data = ",".join([hex(tileset_gid_map[v]) for v in level_data])

  write_mapdata(outfile,
    bank,
    map_data,map_width,
    map_height,
    map_name,
    collision_tiles,
    collision_down_tiles)
  write_tiledata(outfile, bank, tiles_data, map_name)
  write_palette_data(outfile, bank, map_name, unique_palettes)

if __name__ == "__main__":
  main()
