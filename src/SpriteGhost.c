#include "Banks/SetBank2.h"

#include "ZGBMain.h"
#include "SpritePlayer.h"
#include <rand.h>

extern UINT8 evenFrame;

void Start_SpriteGhost()
{
}

INT16 y_diff;
INT16 rand_v;
#define WOBBLE 5
INT8 wobble = WOBBLE;
void Update_SpriteGhost()
{
  if (evenFrame) {
    return;
  }

  y_diff = THIS->y - playerPointer->y;
  
  if (playerPointer->x != THIS->x & y_diff < WOBBLE && y_diff > -WOBBLE)
  {
    if (playerPointer->x < THIS->x)
    {
      THIS->x--;
    }
    else
    {
      THIS->x++;
    }
  } else {
    if (wobble > 0) {
      THIS->x--;
    } else {
      THIS->x++;
    }
  }

  if (y_diff + wobble != 0)
  {
    if (y_diff + wobble > 0)
    {
      THIS->y--;
    }
    else
    {
      THIS->y++;
    }
  }

  wobble--;
  if (wobble == -WOBBLE)
  {
    wobble = WOBBLE * 2;
  }
}

void Destroy_SpriteGhost()
{
}