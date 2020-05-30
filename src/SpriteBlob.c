#include "ZGBMain.h"
#include "Banks/SetBank2.h"
#include "SpriteManager.h"
#include <rand.h>
#include "common.h"

// Shared between enemies, why not
UINT8 blobTileCollision;
const UINT8 anim_blobWalk[] = {3, 0, 1, 2};

void Start_SpriteBlob()
{
  numEnemies++;
  THIS->coll_y = 2;
  THIS->coll_h = 6;
  THIS->coll_x = 2;
  THIS->coll_w = 4;

  SetSpriteAnim(THIS, anim_blobWalk, 15);
  if (arand() > 0) {
    SPRITE_SET_VMIRROR(THIS);
  }
}

void Walk(struct Sprite *sprite, INT8 speed)
{
  blobTileCollision = TranslateSprite(sprite, speed << delta_time, 0);
  if (blobTileCollision)
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

void Update_SpriteBlob()
{
  blobTileCollision = TranslateSprite(THIS, 0, 1 << delta_time);
  if (blobTileCollision)
  {
    if (SPRITE_GET_VMIRROR(THIS))
    {
      Walk(THIS, -1);
    }
    else
    {
      Walk(THIS, 1);
    }
  }
  CheckWrapping(THIS);
}

void Destroy_SpriteBlob()
{
  numEnemies--;
}