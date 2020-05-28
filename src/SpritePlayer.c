#include "Banks/SetBank2.h"

#include "ZGBMain.h"
#include "Keys.h"
#include "SpriteManager.h"
#include "Sprite.h"
#include "SpriteBullet.h"

const UINT8 anim_idle[] = {1, 0};
const UINT8 anim_walk[] = {3, 0, 1, 2};

typedef enum {
	WALK,
	JUMP
} PLAYER_STATE;
PLAYER_STATE playerState;

INT8 accelY = 0;
UINT8 tileCollision;

extern UINT8 numBullets;
struct Sprite *playerPointer = 0;

void Start_SpritePlayer() {
	playerPointer = THIS;

	THIS->coll_y = 1;
	THIS->coll_h = 7;
	THIS->coll_x = 2;
	THIS->coll_w = 4;

	playerState = WALK;
}

void Update_SpritePlayer() {
	if (KEY_PRESSED(J_LEFT)) {
		TranslateSprite(THIS, -1 << delta_time, 0);
		SPRITE_SET_VMIRROR(THIS);
	}
	if (KEY_PRESSED(J_RIGHT)) {
		TranslateSprite(THIS, 1 << delta_time, 0);
		SPRITE_UNSET_VMIRROR(THIS);
	}
	if (keys == 0) {
		SetSpriteAnim(THIS, anim_idle, 15);
	} else {
		SetSpriteAnim(THIS, anim_walk, 15);
	}

	if (KEY_TICKED(J_B) && numBullets != 3) {
		struct Sprite* spawnedBullet = SpriteManagerAdd(SpriteBullet, THIS->x, THIS->y);
		struct BulletInfo *data = (struct BulletInfo *)spawnedBullet->custom_data;
		if (SPRITE_GET_VMIRROR(THIS)) {
			data->speed = -2;
		} else {
			data->speed = 2;
		}
		numBullets++;
	}
	
	switch (playerState)
	{
	case WALK:
		if (KEY_PRESSED(J_A) || KEY_PRESSED(J_UP)) {
			playerState = JUMP;
			accelY = -40;
		}
		break;
	}

	// Gravity
	if (accelY < 40) {
		accelY += 2 << delta_time;
	}

	tileCollision = TranslateSprite(THIS, 0, (accelY >> 4) << delta_time);
	if (tileCollision) {
		if (playerState == JUMP && accelY > 0) {
			playerState = WALK;
		}
		accelY = 0;
	}

}

void Destroy_SpritePlayer() {
	playerPointer = 0;
}