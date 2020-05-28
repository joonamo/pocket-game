#include "ZGBMain.h"
#include "Banks/SetBank2.h"
#include "SpriteManager.h"
#include <rand.h>

// Shared between enemies, why not
UINT8 enemyTileCollision;
const UINT8 anim_enemyWalk[] = {3, 0, 1, 2};

extern UINT8 numEnemies;

void Start_SpriteEnemy()
{
    numEnemies++;
    THIS->coll_y = 2;
    THIS->coll_h = 6;
    THIS->coll_x = 2;
    THIS->coll_w = 4;

    SetSpriteAnim(THIS, anim_enemyWalk, 15);
    if (arand() > 0) {
        SPRITE_SET_VMIRROR(THIS);
    }
}

void walk(struct Sprite *sprite, INT8 speed)
{
    enemyTileCollision = TranslateSprite(sprite, speed << delta_time, 0);
    if (enemyTileCollision)
    {
        if (SPRITE_GET_VMIRROR(sprite))
        {
            SPRITE_UNSET_VMIRROR(sprite);
        }
        else
        {
            SPRITE_SET_VMIRROR(sprite);
        }
    }
}

void Update_SpriteEnemy()
{
    enemyTileCollision = TranslateSprite(THIS, 0, 1 << delta_time);
    if (enemyTileCollision)
    {
        if (SPRITE_GET_VMIRROR(THIS))
        {
            walk(THIS, -1);
        }
        else
        {
            walk(THIS, 1);
        }
    }
}

void Destroy_SpriteEnemy()
{
    numEnemies--;
}