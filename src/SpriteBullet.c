#include "Banks/SetBank2.h"
#include "ZGBMain.h"

#include "SpriteManager.h"
#include "SpriteBullet.h"

extern UINT8 numBullets;

UINT8 bulletTileCollision;
void Start_SpriteBullet() {
    struct BulletInfo *data = (struct BulletInfo *)THIS->custom_data;

    THIS->coll_y = 2;
	THIS->coll_h = 4;
	THIS->coll_x = 2;
	THIS->coll_w = 4;
}

void Update_SpriteBullet() {
    UINT8 i;
	struct Sprite* spr;

    struct BulletInfo *data = (struct BulletInfo *)THIS->custom_data;
    bulletTileCollision = TranslateSprite(THIS, data->speed << delta_time, 0);
    if (bulletTileCollision) {
        SpriteManagerRemove(THIS_IDX);
    }

    for(i = 0u; i != sprite_manager_updatables[0]; ++i) {
		spr = sprite_manager_sprites[sprite_manager_updatables[i + 1u]];
        if (spr->type == SpriteEnemy && CheckCollision(THIS, spr)) {
            SpriteManagerRemove(i);
            SpriteManagerRemove(THIS_IDX);
            return;
        }
    }
}

void Destroy_SpriteBullet() {
    numBullets--;
}