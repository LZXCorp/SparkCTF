#include <stdio.h>
#include <stdlib.h>
#include <string.h>

__attribute__((used))
void gadget_factory_rdi() {
    asm("pop %rdi\nret");
}

__attribute__((used))
void gadget_factory_rsi() {
    asm("pop %rsi\nret");
}

__attribute__((used))
void gadget_factory_rdx() {
    asm("pop %rdx\nret");
}

void win(int arg1, int arg2, int arg3) {
    if (arg1 == 0xdeadbeef && arg2 == 0xcafebabe && arg3 == 0xc0defeed) {
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
}

int process(int r) {
    char terms[35];

    printf("THE PURPLEMAN PROJECT\nState your terms.");
    gets(terms);

    printf("Your terms will not be accepted.");
    return r;
}

int main() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    
    process(0);

    return 0;
}