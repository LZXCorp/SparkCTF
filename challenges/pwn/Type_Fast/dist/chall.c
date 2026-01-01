#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <time.h>

// config
#define BUFFER_SIZE 64
#define REQUIRED_WPM 5067
#define TYPING_TEXT "LeBron James is the greatest basketball player of all time."

// le setup
void setup() {
    /* Disable buffering for immediate output */
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void print_banner() {
    puts("╔════════════════════════════════════════════╗");
    puts("║          LeTyping Test                     ║");
    puts("║    Type the sentence as fast as you can    ║");
    puts("╚════════════════════════════════════════════╝");
}

/* The function we want players to reach to get the flag */
void win() {
    FILE *fp;
    char flag[128];

    fp = fopen("flag.txt", "r");
    if (fp == NULL) {
        puts("\n[!] Flag file not found. Contact an admin.");
        return;
    }

    if (fgets(flag, sizeof(flag), fp) != NULL) {
        printf("\nFLAG: %s\n", flag);
    } else {
        puts("Error reading flag.");
    }
    fclose(fp);
}

/* The vulnerable function (intentionally simple) */
void challenge() {
    char buffer[BUFFER_SIZE];
    time_t start_time, end_time;
    double elapsed, wpm;
    int chars = strlen(TYPING_TEXT);

    printf("\nWelcome to the typing test!\n");
    printf("You must reach %d WPM to get the flag (good luck!).\n\n", REQUIRED_WPM);
    printf("Type this exact sentence and press ENTER when done:\n\n");
    printf("  \"%s\"\n\n", TYPING_TEXT);
    printf("Press ENTER to start...");
    fflush(stdout);
    getchar();

    printf("\nSTART TYPING NOW!\n> ");
    fflush(stdout);

    start_time = time(NULL);

    read(STDIN_FILENO, buffer, 256);

    end_time = time(NULL);
    elapsed = difftime(end_time, start_time);
    if (elapsed <= 0) elapsed = 0.001;

    buffer[strcspn(buffer, "\n")] = '\0';

    double words = (double)chars / 5.0;
    double minutes = elapsed / 60.0;
    wpm = minutes > 0 ? words / minutes : 0.0;

    printf("\nRESULTS:\n");
    printf(" Time: %.2f s\n", elapsed);
    printf(" Your WPM: %.2f\n", wpm);
    printf(" Required WPM: %d\n", REQUIRED_WPM);

    if (strcmp(buffer, TYPING_TEXT) == 0 && wpm >= REQUIRED_WPM) {
        puts("\nYou're insanely fast!");
        win();
    } else {
        if (strcmp(buffer, TYPING_TEXT) != 0) {
            puts("\nText mismatch. Try again.");
        } else {
            printf("\nToo slow. Try again.\n");
        }
    }

    printf("\nThanks for playing!\n");
}

// mainnnnnnnnnnz
int main() {
    setup();
    print_banner();
    challenge();
    return 0;
}

/*
to compile
  gcc ret2main.c -o challenge -fno-stack-protector -no-pie -z execstack
*/
