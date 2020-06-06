def write_tiledata(outfile, bank, tiles_data, name):
  def write_tiles():
    out = ""
    for tile in tiles_data:
      out += "  // " + tile["name"] + "\n"
      out += "  " + ",".join(tile["hexdata"]) + ",\n"
    return out

  def write_palettes():
    return ", ".join([hex(tile["palette_idx"]) for tile in tiles_data])

   # write tiledata
  with open(outfile + "_tiles.b" + bank + ".c", "w") as file:
    file.write("\
#pragma bank " + bank + "\n\
\n\
void empty(void) __nonbanked {}\n\
__addressmod empty const CODE;\n\
\n\
const unsigned char " + name + "_tiles_data[] = {\n\
" + write_tiles() + "};\n\
\n\
const unsigned char " + name + "_tile_palettes[] = {\n\
  " + write_palettes() + "\n\
};\n\
\n\
#include \"TilesInfo.h\"\n\
const struct TilesInfoInternal " + name + "_tiles_internal = {\n\
  8, //width\n\
  8, //height\n\
  " + str(len(tiles_data)) + ", //num_tiles\n\
  " + name + "_tiles_data, //tiles\n\
  " + name + "_tile_palettes, //CGB palette\n\
};\n\
CODE struct TilesInfo " + name + "_tiles = {\n\
  " + bank + ", //bank\n\
  &" + name + "_tiles_internal, //data\n\
};\n\
")

  # write tiledata header
  with open(outfile + "_tiles.h", "w") as file:
    file.write("\
#ifndef TILES_" + name + "_tiles_H\n\
#define TILES_" + name + "_tiles_H\n\
#include \"TilesInfo.h\"\n\
extern struct TilesInfo " + name + "_tiles;\n\
#endif\n\
")

def write_mapdata(
  outfile,
  bank,
  map_data,map_width,
  map_height,
  map_name,
  collision_tiles,
  collision_down_tiles):

  def write_collision_tiles(collision_tiles):
    if len(collision_tiles) == 0:
      return "0"
    return "{" + ", ".join(str(v) for v in collision_tiles) + ", 0}"

  # write map
  with open(outfile + ".b" + bank + ".c", "w") as file:
    file.write("\
#pragma bank " + bank + "\n\
\n\
void empty(void) __nonbanked {}\n\
__addressmod empty const CODE;\n\
\n\
const unsigned char " + map_name + "_map[] = {  \n\
  " + map_data + " \n\
};\n\
#include \"" + map_name + "_tiles.h\"\n\
#include \"MapInfo.h\"\n\
#include \"types.h\"\n\
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
};\n\
CODE UINT8 " + map_name + "_collision_tiles[] = " + write_collision_tiles(collision_tiles) + ";\n\
CODE UINT8 " + map_name + "_collision_down_tiles[] = " + write_collision_tiles(collision_down_tiles) + ";\n\
\n\
")

  # write map header
  with open(outfile + ".h", "w") as file:
    file.write("\
#ifndef MAP_" + map_name + "_H\n\
#define MAP_" + map_name + "_H\n\
#define mapWidth " + map_width + "\n\
#define mapHeight " + map_height + "\n\
#include \"MapInfo.h\"\n\
#include \"types.h\"\n\
extern unsigned char bank_" + map_name + ";\n\
extern struct MapInfo " + map_name + ";\n\
extern UINT8 " + map_name + "_collision_tiles;\n\
extern UINT8 " + map_name + "_collision_down_tiles;\n\
#endif\n\
")

def write_palette_data(outfile, bank, name, palettes):
  def palette_or_zero(idx):
    try:
      return ", ".join([hex(v).rjust(6, " ") for v in palettes[idx]])
    except:
      return "0x0000, 0x0000, 0x0000, 0x0000"
  if len(palettes) > 8:
    raise ValueError("More than 8 palettes given!")

  with open(outfile + "_palette.b" + bank + ".c", "w") as file:
    file.write("\
#pragma bank " + bank + "\n\
\n\
void empty(void) __nonbanked {}\n\
__addressmod empty const CODE;\n\
\n\
#include \"types.h\"\n\
\n\
CODE UINT16 " + name + "_palette[] = {\n\
" + palette_or_zero(0) + ",\n\
" + palette_or_zero(1) + ",\n\
" + palette_or_zero(2) + ",\n\
" + palette_or_zero(3) + ",\n\
" + palette_or_zero(4) + ",\n\
" + palette_or_zero(5) + ",\n\
" + palette_or_zero(6) + ",\n\
" + palette_or_zero(7) + "\n\
};")

  # write tiledata header
  with open(outfile + "_palette.h", "w") as file:
    file.write("\
#ifndef PALETTE_" + name + "_palette_H\n\
#define PALETTE_" + name + "_palette_H\n\
#include \"types.h\"\n\
extern UINT16 " + name + "_palette;\n\
#endif\n\
")