#include "Banks/SetBank2.h"

#include "../res/src/tiles.h"
#include "../res/src/map.h"

#include "ZGBMain.h"
#include "Scroll.h"
#include "SpriteManager.h"

#include <gb/gb.h>
#include <rand.h>

UINT8 collision_tiles[] = {1, 0};
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
	SHOW_SPRITES;

	InitScrollTiles(0, &tiles);
	InitScroll(&map, collision_tiles, 0);
	SHOW_BKG;

	// waitpad(0xFF);
	seed = DIV_REG;
	// waitpadup();
	seed |= (UWORD)DIV_REG << 8;
	initarand(seed);

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
			SpriteManagerAdd(SpriteEnemy, 80 + (arand() >> 1), 16);
		}
	}
}