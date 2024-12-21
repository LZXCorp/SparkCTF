#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>

#define BUFSIZE 100
// not the actual size for the actual application :)

void sigsegv_handler(int sig){
	printf("SIG24{NOT_THE_ACTUAL_FLAG}");
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
