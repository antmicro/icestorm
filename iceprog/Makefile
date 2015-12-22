INCLUDE_PATH=$(LIBFTDI_INSTALL_PATH)/include/libftdi1

LDFLAGS=-Wl,-rpath=$(LIBFTDI_INSTALL_PATH):$(LIBUSB_INSTALL_PATH)/lib,-lftdi1,-lusb-1.0
TOPDIR  := $(shell pwd)
#TOPDIR = .
MXEGCC = /usr/local/src/mxe/usr/bin/i686-pc-mingw32-gcc


CFLAGS ?= -I$(INCLUDE_PATH) -Wall -std=c11 -L$(LIBFTDI_INSTALL_PATH)/lib -L$(LIBUSB_INSTALL_PATH)/lib
CC=arm-linux-gnueabihf-gcc
OBJS = iceprog.o

all: iceprog.o

iceprog.o: iceprog.c
	$(CC) $(CFLAGS) -o iceprog  iceprog.c $(LDFLAGS)

iceprog.exe: iceprog.c
	$(MXEGCC) -std=c99 -o iceprog.exe -Os iceprog.c -lftdi -lusb -lm

install:
	install -d $(INSTALLDIR)
	install -c $(OBJS) $(INSTALLDIR)

clean:
	rm -f *.o *~ core iceprog iceprog.exe
