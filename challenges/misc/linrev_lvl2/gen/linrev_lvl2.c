#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

// Obfuscated data storage - split into multiple arrays with transformations
static const uint8_t d1[] = {0x93, 0x52, 0xfc, 0xb2, 0x1c, 0xc0, 0x89, 0xc7};
static const uint8_t d2[] = {0xc9, 0xe0, 0x53, 0x12, 0x0e, 0x64, 0x38, 0x82};
static const uint8_t d3[] = {0xf9, 0x24, 0x53, 0x14, 0x53, 0xb1, 0xf9, 0x64};
static const uint8_t d4[] = {0xc3, 0x82, 0xcc, 0x64, 0xec, 0x71, 0xbd, 0x55};

// Transformation keys scattered throughout
static const uint32_t k1 = 0xDEADBEEF;
static const uint8_t k2 = 0xAA;
static const uint8_t k3 = 0x55;
static const uint8_t k4 = 0x33;

// Anti-analysis: dummy arrays to confuse static analysis
static const char n1[] = {0x46, 0x4c, 0x41, 0x47, 0x00};
static const char n2[] = {0x70, 0x61, 0x73, 0x73, 0x77, 0x6f, 0x72, 0x64, 0x00};

// Obfuscated function to transform data
static inline uint8_t t1(uint8_t v, uint8_t k) {
    return ((v ^ k) + 0x11) & 0xFF;
}

static inline uint8_t t2(uint8_t v, uint8_t k) {
    return ((v - 0x11) ^ k) & 0xFF;
}

static inline uint8_t t3(uint8_t v) {
    return ((v << 4) | (v >> 4)) & 0xFF;
}

static inline uint8_t t4(uint8_t v) {
    return ((v >> 4) | (v << 4)) & 0xFF;
}

// Multi-stage transformation function
void p1(uint8_t* buf, size_t len) {
    for (size_t i = 0; i < len; i++) {
        buf[i] = t2(buf[i], (i & 1) ? k3 : k2);
    }
}

void p2(uint8_t* buf, size_t len) {
    for (size_t i = 0; i < len; i++) {
        buf[i] = t4(buf[i]);
    }
}

void p3(uint8_t* buf, size_t len) {
    for (size_t i = 0; i < len; i++) {
        buf[i] ^= k4;
    }
}

// Reconstruct the hidden data
void r1(uint8_t* out) {
    // Copy and transform each segment
    uint8_t temp[32];

    memcpy(temp, d1, 8);
    memcpy(temp + 8, d2, 8);
    memcpy(temp + 16, d3, 8);
    memcpy(temp + 24, d4, 8);

    // Apply reverse transformations
    p3(temp, 32);
    p2(temp, 32);
    p1(temp, 32);

    memcpy(out, temp, 32);
}

// Validation function with obfuscated name
int v1(const char* s1, const char* s2) {
    uint64_t val1 = 0, val2 = 0;

    // Parse hex values
    if (s1 && s2) {
        val1 = strtoull(s1, NULL, 16);
        val2 = strtoull(s2, NULL, 16);
    }

    // Check if both match the magic value
    return (val1 == k1 && val2 == k1);
}

// Main entry point
int main(int argc, char* argv[]) {
    // Dummy operations for anti-analysis
    volatile int x = 0;
    for (int i = 0; i < 100; i++) x += i;

    if (argc != 3) {
        printf("It's me again, but i've levelled up\n");
        return 1;
    }

    if (v1(argv[1], argv[2])) {
        uint8_t result[32] = {0};
        r1(result);
        printf("%s\n", result);
    } else {
        printf("It's me again, but i've levelled up\n");
    }

    return 0;
}
