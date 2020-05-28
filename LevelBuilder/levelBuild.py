import json
import argparse

def main():
  parser = argparse.ArgumentParser(description="Compiles tiled to gb")
  parser.add_argument("infile", help="level file", type=str)
  parser.add_argument("outfile", help="Output file", type=str)
  args = parser.parse_args()

  bank = "3"

  with open(args.infile, "r") as file:
    level_data = json.load(file)

  map_name = args.infile.split("/")[-1].split(".")[0]
  map_data = ", ".join([hex(v - 1) for v in level_data["layers"][0]["data"]])
  map_width = str(level_data["layers"][0]["width"])
  map_height = str(level_data["layers"][0]["height"])

  with open(args.outfile + ".b" + bank + ".c", "w") as file:
    file.write("\
#pragma bank 3\n\
\n\
void empty(void) __nonbanked {}\n\
__addressmod empty const CODE;\n\
\n\
const unsigned char " + map_name + "_map[] = {  \n\
  " + map_data + " \n\
};\n\
#include \"tiles.h\"\n\
#include \"MapInfo.h\"\n\
const struct MapInfoInternal " + map_name + "_internal = {\n\
	" + map_name + "_map, //map\n\
	" + map_width + ", //width\n\
	" + map_height + ", //height\n\
	0, //attributes\n\
	&tiles, //tiles info\n\
};\n\
CODE struct MapInfo " + map_name + " = {\n\
	3, //bank\n\
	&" + map_name + "_internal, //data\n\
};")

  with open(args.outfile + ".h", "w") as file:
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

if __name__ == "__main__":
    main()
