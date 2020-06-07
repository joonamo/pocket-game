#ifndef ZGBMAIN_H
#define ZGBMAIN_H

#define STATES \
_STATE(StateGame)\
STATE_DEF_END

#define SPRITES                     \
  _SPRITE_DMG(SpritePlayer, player) \
  _SPRITE_DMG(SpriteBlob, blob_tiles)   \
  _SPRITE_DMG(SpriteBullet, bullet) \
  _SPRITE_DMG(SpriteGhost, ghost_tiles) \
SPRITE_DEF_END

#include "ZGBMain_Init.h"

#endif