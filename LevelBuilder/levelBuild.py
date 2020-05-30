import argparse
from imgtogb import read_png
import xml.etree.ElementTree as XET
from pathlib import Path

def write_tiles(tiles_data):
  out = ""
  for tile in tiles_data:
    out += "  // " + tile["name"] + "\n"
    out += "  " + ",".join(tile["hexdata"]) + ",\n"
  return out

def main():
  parser = argparse.ArgumentParser(description="Compiles tiled to gb")
  parser.add_argument("infile", help="level file", type=str)
  parser.add_argument("outfile", help="Output file", type=str)
  args = parser.parse_args()
  infile = args.infile
  outfile = args.outfile

  bank = "3"

  root = XET.parse(infile).getroot()
  layer = root.find("layer")
  map_width = layer.attrib['width']
  map_height = layer.attrib['height']
  level_data = [int(v) for v in layer.find('data').text.replace("\n", "").split(",")]
  
  tileset_gid_map = dict()
  seen_tiles_id = 0
  tiles_data = []
  collision_tiles = []

  tilemap_dir = Path(infile).parent
  for tilemap in root.findall("tileset"):
    tilemap_gid = int(tilemap.attrib["firstgid"])
    tilemap_path = tilemap_dir.joinpath(tilemap.attrib["source"])
    tileroot = XET.parse(tilemap_path).getroot()
    for tile in tileroot.findall("tile"):
      tile_gid = tilemap_gid + int(tile.attrib["id"])
      tileset_gid_map[tile_gid] = seen_tiles_id
      if tile.find("properties/property[@name='collision'][@value='true']") is not None:
        collision_tiles.append(seen_tiles_id)
      image = tile.find("image")
      (tile_data, palettes) = read_png(
        str(tilemap_path.parent.joinpath(image.attrib["source"])))
      tiles_data.append({
        "name": image.attrib["source"],
        "hexdata": [hex(v).rjust(4, " ") for v in tile_data],
        "palettes": palettes
      })
      seen_tiles_id += 1
      
  map_name = args.infile.split("/")[-1].split(".")[0]
  map_data = ",".join([hex(tileset_gid_map[v]) for v in level_data])

  # write map
  with open(outfile + ".b" + bank + ".c", "w") as file:
    file.write("\
#pragma bank 3\n\
\n\
void empty(void) __nonbanked {}\n\
__addressmod empty const CODE;\n\
\n\
const unsigned char " + map_name + "_map[] = {  \n\
  " + map_data + " \n\
};\n\
#include \"" + map_name + "_tiles.h\"\n\
#include \"MapInfo.h\"\n\
const struct MapInfoInternal " + map_name + "_internal = {\n\
	" + map_name + "_map, //map\n\
	" + map_width + ", //width\n\
	" + map_height + ", //height\n\
	0, //attributes\n\
	&" + map_name + "_tiles, //tiles info\n\
};\n\
CODE struct MapInfo " + map_name + " = {\n\
	3, //bank\n\
	&" + map_name + "_internal, //data\n\
};")

  # write map header
  with open(outfile + ".h", "w") as file:
    file.write("\
#ifndef MAP_" + map_name + "_H\n\
#define MAP_" + map_name + "_H\n\
#define mapWidth " + map_width + "\n\
#define mapHeight " + map_height + "\n\
#include \"MapInfo.h\"\n\
extern unsigned char bank_" + map_name + ";\n\
extern struct MapInfo "+ map_name +";\n\
#endif\n\
")  
  
  # write tiledata
  with open(outfile + "_tiles.b" + bank + ".c", "w") as file:
    file.write("\
#pragma bank 3\n\
\n\
void empty(void) __nonbanked {}\n\
__addressmod empty const CODE;\n\
\n\
const unsigned char " + map_name + "_tiles_data[] = {\n\
" + write_tiles(tiles_data) + "};\n\
\n\
#include \"TilesInfo.h\"\n\
const struct TilesInfoInternal " + map_name + "_tiles_internal = {\n\
	8, //width\n\
	8, //height\n\
	" + str(len(tiles_data)) + ", //num_tiles\n\
	" + map_name + "_tiles_data, //tiles\n\
	0, //CGB palette\n\
};\n\
CODE struct TilesInfo "+ map_name +"_tiles = {\n\
	" + bank + ", //bank\n\
	&" + map_name + "_tiles_internal, //data\n\
};\n\
")

  # write tiledata header
  with open(outfile + "_tiles.h", "w") as file:
    file.write("\
#ifndef TILES_" + map_name + "_tiles_H\n\
#define TILES_" + map_name + "_tiles_H\n\
#include \"TilesInfo.h\"\n\
extern unsigned char bank" + map_name + "_tiles;\n\
extern struct TilesInfo " + map_name + "_tiles;\n\
#endif\n\
")

if __name__ == "__main__":
    main()
