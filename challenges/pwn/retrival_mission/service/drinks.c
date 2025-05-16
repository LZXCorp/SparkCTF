#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void retrieve() {
    FILE *flag_file = fopen("flag.txt", "r");
    if (flag_file != NULL) {
        char flag[100] = {0};
        fgets(flag, sizeof(flag), flag_file);
        printf("\nCongrats! Here's your flag: %s\n", flag);
        fclose(flag_file);
    } else {
        printf("\nFor debugging purposes, please put flag.txt in the same directoy.\n");
    }
}

int vuln() {
    char drink[0x256];
    char flavour[0x4];

    printf("What kind of drink do you want? ");

    gets(drink);
    printf(drink);

    printf("\n\nWhat about the flavour?         ");

    gets(flavour);

    printf("Your drink will be prepared in a moment!");
    return 0;
}

int main() {
    // SETUP
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    
    vuln();

    return 0;
}