#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <ctype.h>

// List of blocked commands that can read file contents
const char *blocked_commands[] = {
    "cat", "more", "less", "head", "tail", "nl",
    "grep", "egrep", "fgrep", "sed", "awk","vim", "vi", 
    "nano", "emacs", "ed", "pico","strings",NULL,
    "chmod", "chown", "chgrp"
};

int is_command_blocked(const char *input) {
    char *input_lower = strdup(input);
    if (!input_lower) return 1; // Block on allocation failure

    // Convert to lowercase for case-insensitive check
    for (int i = 0; input_lower[i]; i++) {
        input_lower[i] = tolower(input_lower[i]);
    }

    // Check against blocked commands
    for (int i = 0; blocked_commands[i] != NULL; i++) {
        // Check if the blocked command appears as a standalone word
        char *found = strstr(input_lower, blocked_commands[i]);
        while (found != NULL) {
            // Check if it's at the start or preceded by whitespace/special chars
            int is_start = (found == input_lower) ||
                          (!isalnum(*(found - 1)) && *(found - 1) != '_');
            // Check if it's at the end or followed by whitespace/special chars
            int cmd_len = strlen(blocked_commands[i]);
            int is_end = (found[cmd_len] == '\0') ||
                        (!isalnum(found[cmd_len]) && found[cmd_len] != '_');

            if (is_start && is_end) {
                free(input_lower);
                return 1; // Blocked command found
            }
            found = strstr(found + 1, blocked_commands[i]);
        }
    }

    free(input_lower);
    return 0;
}

int main(int argc, char *argv[]) {
    FILE *file;
    char ch;

    // Set real UID to effective UID to inherit SUID privileges
    // This ensures we run with the privileges of the file owner
    setuid(993);
    setgid(993);

    // If arguments are provided, execute them as a system command
    if (argc > 1) {
        char command[1024] = "";

        // Concatenate all arguments into a single command
        for (int i = 1; i < argc; i++) {
            strcat(command, argv[i]);
            if (i < argc - 1) {
                strcat(command, " ");
            }
        }

        // Check if command contains blocked keywords
        if (is_command_blocked(command)) {
            fprintf(stderr, "Error: Blocked command detected. File reading / file permission modification commands are not allowed.\n");
            return 1;
        }

        // Execute the command
        system(command);
        return 0;
    }
    return 0;
}
