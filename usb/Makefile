CC:= gcc
CFLAGS:= `pkg-config --cflags gio-2.0` -g
LIBS:= `pkg-config --libs gio-2.0`
OUT1:= isoft-rmdisk
.PHONY:all clean

all: $(OUT1)

$(OUT1):main.o
	$(CC) $^ -o $@ $(LIBS)
%*.o:%*.c
	$(CC) $(CFLAGS) $^ -o $@

clean:
	-rm *.o $(OUT1)
