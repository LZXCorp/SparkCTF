#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>

#define BUFSIZE 128000

void sigsegv_handler(int sig){
	printf("SIG24{0v3rFl0w_B00mZ}");
	fflush(stderr);
	exit(1);
};

void vuln(){
	char buf[BUFSIZE];
	printf("You shall not pass without the key: ");
	fflush(stdout);
	scanf("%s",buf);
}

int main(int argc, char **argv){
	signal(SIGSEGV,sigsegv_handler);
	vuln();
}
