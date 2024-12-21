#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>

#define BUFSIZE 800
#define FLAGSIZE 256

void vuln(char *buf){
	gets(buf);
	puts(buf);
}

int main(int argc, char **argv){
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);

	gid_t gid = getegid();
	setresgid(gid, gid, gid);

	char buf[BUFSIZE];

	printf("Ask and you shall receive! : ");
	vuln(buf);

	printf("Thanks! Executing now....");

	((void (*)())buf)();

	 return 0;
}
