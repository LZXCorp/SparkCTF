CC = gcc
CFLAGS = -O2 -Wall
TARGET = linrev_lvl2

all: $(TARGET)

$(TARGET): linrev_lvl2.c
	$(CC) $(CFLAGS) -o $(TARGET) linrev_lvl2.c

clean:
	rm -f $(TARGET) encoder

.PHONY: all clean
