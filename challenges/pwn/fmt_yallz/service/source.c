#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[]) {
  char* flag = "SIG24{f0rm4t_54hw1nGz}";

  int f1 = 0xdeadf001;
  int f2 = 0xb33fb1b0;
  char buf[2000];
  printf("The input wars have begun. Type something and it will be displayed: \n");
  fflush(stdout);
  gets(buf);
  printf(buf);

  return 0;
}
