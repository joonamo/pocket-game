#include "types.h"
#include "Sprite.h"

UINT8 numBullets = 0;
UINT8 numEnemies = 0;

UINT8 evenFrame = 0;

#define XMAX 168
#define XMIN 0
#define YMAX 152
#define YMIN 0
void CheckWrapping(struct Sprite *sprite) {
  if ((INT16)sprite->x < XMIN) {
    sprite->x = XMAX;
  } else if (sprite->x > XMAX) {
    sprite->x = XMIN;
  }

  if ((INT16)sprite->y < YMIN) {
    sprite->y = YMAX;
  } else if (sprite->y > YMAX) {
    sprite->y = YMIN;
  }
}
