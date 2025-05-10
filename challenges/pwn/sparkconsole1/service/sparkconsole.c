#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define PIN "512524"
#define MAX_CMD_LEN 100

void print_flag() {
    printf("\nCongrats! Here's your flag: SIG24{Buff3r_0v3rfl0w_1s_FuN!}\n");
}

void read_flag_file() {
    FILE *fp = fopen("flag.txt", "r");
    if (!fp) {
        printf("Error: Cannot open flag.txt\n");
        return;
    }
    char line[256];
    while (fgets(line, sizeof(line), fp)) {
        printf("%s", line);
    }
    fclose(fp);
}

void handle_cat(char *filename) {
    if (strcmp(filename, "pin.txt") == 0) {
        printf("// This file contains nothing useful\n");
        printf("// Or does it? ;)\n");
        printf("512524\n");
        return;
    }
    printf("Error: File not found\n");
}

void shell_loop() {
    char cmd[MAX_CMD_LEN];
    char arg[MAX_CMD_LEN];
    
    while (1) {
        printf("$ ");
        fgets(cmd, MAX_CMD_LEN, stdin);
        cmd[strcspn(cmd, "\n")] = 0;

        if (strcmp(cmd, "ls") == 0) {
            printf("pin.txt\n");
            continue;
        }

        if (sscanf(cmd, "cat %s", arg) == 1) {
            handle_cat(arg);
            continue;
        }

        if (sscanf(cmd, "echo %s", arg) == 1) {
            if (strstr(arg, "%n") != NULL) {
                printf("Error: Error Occured while parsing string\n");
            } else {
                printf(arg);
                printf("\n");
            }
            continue;
        }

        if (strcmp(cmd, "exit") == 0) break;

        printf("%s: command not found\n", cmd);
    }
}

int main() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    printf("Spark Console!!!\n");
    printf("Available commands: ls, cat <file>, exit\n\n");

    shell_loop();

    char buffer2[6] = "xxxxxx";
    char buffer1[32];

    printf("\nBefore you leave, please enter the PIN: ");
    gets(buffer1);

    printf("\nA: %.32s\n", buffer1);
    printf("B: %.6s\n\n", buffer2);

    if (strncmp(buffer2, PIN, 6) == 0) {
        print_flag();
    } else {
        printf("Incorrect PIN. Better luck next time!\n");
    }

    return 0;
}