#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void getflag(){
    FILE *file = fopen("flag.txt", "r");
    char flag[256];
    fgets(flag, 256, file);
    printf("%s", flag);
    fclose(file);
    exit(1);
}


void play() {
    srand(time(0)); 
    for (int i = 0; i < 10; i++) {
        int rolled = rand() % 6 + 1; 
        printf("=============================\n");
        printf("=          Round %d          =\n", i + 1);
        printf("=============================\n\n");

        int guess = 0;
        printf("Make your guess (1-6):\n");
        if (scanf("%d", &guess) != 1 || guess < 1 || guess > 6) {
            printf("Re-try with a proper guess.\n");
            exit(0);
        }

        if (guess == rolled) {
            printf("Correct!\n\n");
        } else {
            printf("Wrong guess! The number was %d\n", rolled);
            exit(0);
        }
    }
    getflag();
}

int main() {

    //ignore this
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    printf("Let's play a game shall we?\n");
    printf("If you can guess the number on the dice 10 times, I shall grant you the flag :)\n\n");

    play();

}