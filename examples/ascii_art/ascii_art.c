#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define WIDTH 50
#define HEIGHT 20

char symbols[] = { '#', '%', '&', '*', '+', '-', '.', ' ' };

void generate_image(char image[][WIDTH]) {
  srand(time(NULL)); // Seed random number generator

  for (int y = 0; y < HEIGHT; y++) {
    for (int x = 0; x < WIDTH; x++) {
      // Generate a random index within the symbols array
      int random_index = rand() % sizeof(symbols) / sizeof(symbols[0]);
      image[y][x] = symbols[random_index];
    }
  }
}

int main() {
  char image[HEIGHT][WIDTH];

  generate_image(image);

  for (int y = 0; y < HEIGHT; y++) {
    for (int x = 0; x < WIDTH; x++) {
      printf("%c", image[y][x]);
    }
    printf("\n");
  }

  return 0;
}
