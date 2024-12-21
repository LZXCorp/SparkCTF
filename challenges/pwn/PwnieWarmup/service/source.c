#include <stdio.h>
#include <string.h>

void printf_flag(void) {
  printf("Well done! here is your flag: SIG24{4_s1mpl3_w4rmUp}");
  fflush(stdout);
}

void vuln(){
	char buf[20];
	printf("\nSo what's your name again?: ");
	scanf("%s",buf);
	printf("Hi %s",buf);
	fflush(stdout);
}

int main(int argc, char *argv[]) {
  setbuf(stdin,NULL);
  setbuf(stdout,NULL);
  setbuf(stderr, NULL);

  printf("Address of print_flag : %p",printf_flag);
  vuln();

  return 0;
}