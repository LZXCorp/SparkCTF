#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define TARGET_PORT 56441
#define BUFFER_SIZE 256

// Obfuscated data arrays - flag split and heavily encoded
// Original: SPARK{w04h_y0uR3_g3tt1ng_th3_h4nG_0f_R3V}
// Applied: XOR with rotating key + bit reversal + scrambling
static unsigned char d1[] = {0xce, 0xb8, 0x98, 0xd4, 0xea};
static unsigned char d2[] = {0xda, 0x2b, 0x20, 0xe7, 0x7b};
static unsigned char d3[] = {0xc8, 0x2c, 0x20, 0x47, 0x66};
static unsigned char d4[] = {0xfe, 0x3f, 0x8b, 0x64, 0x75};
static unsigned char d5[] = {0x5d, 0x08, 0x0f, 0x4e, 0xe0};
static unsigned char d6[] = {0x5d, 0xa4, 0xa1, 0x52, 0x7b};
static unsigned char d7[] = {0x7d, 0xa7, 0x9b, 0x52, 0x57};
static unsigned char d8[] = {0x54, 0x3f, 0x11, 0x64, 0x64};
static unsigned char d9[] = {0xd9};

// Obfuscation keys
static unsigned char k1[] = {0xde, 0xad, 0xbe, 0xef, 0xca};
static unsigned char k2[] = {0xfe, 0xba, 0xbe, 0x13, 0x37};

// Transform function 1 - reverse bit manipulation (decode)
void t1(unsigned char *data, int len, unsigned char *key, int klen) {
    for (int i = 0; i < len; i++) {
        // Reverse: swap nibbles first, then XOR
        data[i] = ((data[i] & 0x0F) << 4) | ((data[i] & 0xF0) >> 4);
        data[i] ^= key[i % klen];
    }
}

// Transform function 2 - additional XOR layer (decode)
void t2(unsigned char *data, int len, unsigned char *key, int klen) {
    for (int i = 0; i < len; i++) {
        // Reverse: NOT first, then XOR
        data[i] = ~data[i];
        data[i] ^= key[(len - i - 1) % klen];
    }
}

// Transform function 3 - byte rotation (decode)
void t3(unsigned char *data, int len) {
    for (int i = 0; i < len; i++) {
        // Reverse: rotate right by 3 (same as left by 5)
        data[i] = ((data[i] >> 3) | (data[i] << 5)) & 0xFF;
    }
}

// Combine and decode all segments
void p1(char *output) {
    unsigned char temp[50];
    int pos = 0;

    // Copy all segments
    memcpy(temp + pos, d1, sizeof(d1)); pos += sizeof(d1);
    memcpy(temp + pos, d2, sizeof(d2)); pos += sizeof(d2);
    memcpy(temp + pos, d3, sizeof(d3)); pos += sizeof(d3);
    memcpy(temp + pos, d4, sizeof(d4)); pos += sizeof(d4);
    memcpy(temp + pos, d5, sizeof(d5)); pos += sizeof(d5);
    memcpy(temp + pos, d6, sizeof(d6)); pos += sizeof(d6);
    memcpy(temp + pos, d7, sizeof(d7)); pos += sizeof(d7);
    memcpy(temp + pos, d8, sizeof(d8)); pos += sizeof(d8);
    memcpy(temp + pos, d9, sizeof(d9)); pos += sizeof(d9);

    // Apply reverse transformations
    t3(temp, pos);
    t2(temp, pos, k2, sizeof(k2));
    t1(temp, pos, k1, sizeof(k1));

    memcpy(output, temp, pos);
    output[pos] = '\0';
}

// Network communication handler
int n1(const char *host, int port) {
    int sock;
    struct sockaddr_in server;

    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == -1) {
        return -1;
    }

    server.sin_family = AF_INET;
    server.sin_port = htons(port);

    if (inet_pton(AF_INET, host, &server.sin_addr) <= 0) {
        close(sock);
        return -1;
    }

    if (connect(sock, (struct sockaddr *)&server, sizeof(server)) < 0) {
        close(sock);
        return -1;
    }

    return sock;
}

// Receive data handler
int r1(int sock, char *buffer, int size) {
    memset(buffer, 0, size);
    int bytes = recv(sock, buffer, size - 1, 0);
    if (bytes <= 0) {
        return -1;
    }
    buffer[bytes] = '\0';
    return bytes;
}

// Send data handler
int s1(int sock, const char *data) {
    int len = strlen(data);
    if (send(sock, data, len, 0) < 0) {
        return -1;
    }
    return 0;
}

// Main protocol handler
int m1() {
    int sock;
    char buffer[BUFFER_SIZE];
    char payload[50];

    // Establish connection
    sock = n1("127.0.0.1", TARGET_PORT);
    if (sock < 0) {
        return 0;
    }

    // Step 1: Expect "hello linrev3"
    if (r1(sock, buffer, BUFFER_SIZE) < 0) {
        close(sock);
        return 0;
    }

    if (strcmp(buffer, "hello linrev3") != 0) {
        close(sock);
        return 0;
    }

    // Step 2: Send "sendflagoverthenet?"
    if (s1(sock, "sendflagoverthenet?") < 0) {
        close(sock);
        return 0;
    }

    // Step 3: Expect "yes"
    if (r1(sock, buffer, BUFFER_SIZE) < 0) {
        close(sock);
        return 0;
    }

    if (strcmp(buffer, "yes") != 0) {
        close(sock);
        return 0;
    }

    // Step 4: Decode and send the payload
    p1(payload);
    if (s1(sock, payload) < 0) {
        close(sock);
        return 0;
    }

    close(sock);
    return 1;
}

int main() {
    if (!m1()) {
        printf("This is just outright insane. Take your time on this!\n");
        return 1;
    }

    return 0;
}
