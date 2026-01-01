/* gcc -no-pie -fno-stack-protector -o chall chall.c */
#include <stdio.h>   
#include <string.h>

void flag(int a, int b, int c) {
    if (a == 0xAAAABBBB && b == 0xCCCCDDDD && c == 0x12345678){
        FILE *file = fopen("flag.txt", "r");
        char flag[256];
        fgets(flag,256,file);
        printf("%s",flag);
        fclose(file);
    }
}

int main() {

    //ignore this
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    char find[150];
    printf("I'm missing something...Could you tell me where it is?: ");
    size_t input = read(0, find, 0x300);
    return 0;
}