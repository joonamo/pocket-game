#pragma bank 3

void empty(void) __nonbanked {}
__addressmod empty const CODE;

#include "types.h"

CODE UINT16 level1_palette[] = {
0x7f0d,    0x0,    0x0,    0x0,
0x1115, 0x7fff,    0x0,    0x0,
0x7f0d, 0x1595,  0x44a,   0x15,
0x0000, 0x0000, 0x0000, 0x0000,
0x0000, 0x0000, 0x0000, 0x0000,
0x0000, 0x0000, 0x0000, 0x0000,
0x0000, 0x0000, 0x0000, 0x0000,
0x0000, 0x0000, 0x0000, 0x0000
};