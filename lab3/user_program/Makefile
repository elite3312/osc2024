SRCS = $(wildcard *.c)
OBJS = $(SRCS:.c=.o)
CFLAGS = -Wall -O2 -ffreestanding -nostdinc -nostdlib -nostartfiles
all: clean user.img

start.o: start.S
	aarch64-none-elf-gcc $(CFLAGS) -c start.S -o start.o

%.o: %.c
	aarch64-none-elf-gcc $(CFLAGS) -c $< -o $@

user.img: start.o $(OBJS)
	aarch64-none-elf-ld start.o $(OBJS) -T linker.ld -o user.elf
	aarch64-none-elf-objcopy -O binary user.elf user.img

clean:
	rm -f user.img user.elf *.o

run:
	qemu-system-aarch64 -M raspi3b -kernel user.img -d in_asm