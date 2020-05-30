#pragma bank 3

void empty(void) __nonbanked {}
__addressmod empty const CODE;

const unsigned char level1_tiles_data[] = {
  // ../asesprite/empty.png
   0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
  // ../asesprite/block.png
   0x0,0xff,0xdf,0x20,0xdf,0x20, 0x0,0xff,0xfd, 0x2,0xfd, 0x2, 0x0,0xff,0xf7, 0x8,
};

#include "TilesInfo.h"
const struct TilesInfoInternal level1_tiles_internal = {
	8, //width
	8, //height
	2, //num_tiles
	level1_tiles_data, //tiles
	0, //CGB palette
};
CODE struct TilesInfo level1_tiles = {
	3, //bank
	&level1_tiles_internal, //data
};