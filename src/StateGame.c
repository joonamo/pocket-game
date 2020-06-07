#include "Banks/SetBank2.h"

#include "../res/src/tiles.h"
#include "level1.h"
#include "level1_palette.h"
#include "level1spritepalette_palette.h"

#include "ZGBMain.h"
#include "Scroll.h"
#include "SpriteManager.h"

#include <gb/gb.h>
#include <rand.h>

UINT8 enemySpawnTimer = 128u;
extern UINT8 numEnemies;
extern UINT8 evenFrame;

void Start_StateGame() {
	UINT8 i;
	UINT16 seed;


	SPRITES_8x8;
	for(i = 0; i != N_SPRITE_TYPES; ++ i) {
		SpriteManagerLoad(i);
	}
	SetPalette(SPRITES_PALETTE, 0, 8, &level1spritepalette_palette, 3);
	SHOW_SPRITES;

	InitScrollTiles(0, &tiles);
	SetPalette(BG_PALETTE, 0, 8, &level1_palette, 3);
	InitScroll(&level1, &level1_collision_tiles, &level1_collision_down_tiles);
	MoveScroll(8, 8);
	SHOW_BKG;

	// waitpad(0xFF);
	seed = DIV_REG;
	// waitpadup();
	seed |= (UWORD)DIV_REG << 8;
	initarand(seed);

	SpriteManagerAdd(SpritePlayer, 80, 120);
	SpriteManagerAdd(SpriteGhost, 80, 16);
}

void Update_StateGame() {
	evenFrame = 1 - evenFrame;

	if (numEnemies < 10) {
		enemySpawnTimer--;
		if (enemySpawnTimer == 0) {
			enemySpawnTimer = 1;
			if (numEnemies < 5) {
				enemySpawnTimer = 64u;
			} else if (numEnemies < 10) {
				enemySpawnTimer = 128u;
			} else {
				enemySpawnTimer = 255u;
			}
			SpriteManagerAdd(SpriteBlob, 80 + (arand() >> 1), 16);
		}
	}
}