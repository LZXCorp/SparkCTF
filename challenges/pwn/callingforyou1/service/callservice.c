#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void useful_gadgets() {
    __asm__(
        "pop %rax\n"
        "ret\n"

        "pop %rdi\n"
        "ret\n"

        "pop %rsi\n"
        "ret\n"

        "pop %rdx\n"
        "ret\n"

        "syscall\n"
        "ret\n"

        "mov %rsi, (%rdi)\n"
        "ret\n"
        
        "xor %rdx, %rdx\n"
        "ret\n"
        
        "add %rax, %rdi\n"
        "ret"
    );
}

int main() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    printf("Calling Services\nHelp may I help you?\n1. Write feedback\n2. Call someone idk.\n3. Exit\n");
    
    int choice;
    char feedback[100];
    
    scanf("%d", &choice);
    if (choice == 1) {
        printf("Please enter your feedback: ");
        getchar();
        gets(feedback);
        printf("Thank you for your feedback: %s", feedback);
    }
    else if (choice == 2) {
        printf("Not yet implemented (forgor to get a dev to do this) \n");
    }
    else {
        printf("Goodbye.\n");
        exit(0);
    }
    return 0;
}