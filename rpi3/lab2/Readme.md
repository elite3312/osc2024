# lab2

## kernel

### start.s

ARM64 assembly bootloader
- Ensures only CPU core 0 continues (other cores go into - low-power wait)
- Sets up the stack pointer
- Clears the BSS section (uninitialized data)
- Jumps to the C main function

### main.c

Main kernel entry point
- Initializes UART for serial communication
- Parses the device tree to find the initramfs location
- Implements a simple memory allocator (simple_alloc)
- Runs a command-line shell that accepts user input

### Hardware Interface

uart.c & uart.h
- Implements a simple UART driver for serial communication

### file system

shell.c & shell.h

- help - Lists available commands
- ls - Lists files in the CPIO archive
- cat - Displays file contents
- Parses CPIO (Copy In, Copy Out) archive format for the - initial RAM filesystem

initramfs.cpio
- A CPIO archive containing the initial RAM filesystem
- cpio stands for Copy In and Out, and it's a command-line tool used in Unix-like systems to create, extract, and manage archive files.

### device tree


A Flattened Device Tree Blob is a binary representation of a Device Tree, which describes the hardware layout of a system to the OS. It is static.

dtb.c & dtb.h

- Parses the flattened device tree blob (DTB) to extract - hardware information
- Finds the initramfs location specified in the device tree
- Handles big-endian to little-endian conversion for DTB data

### build

- Makefile 
  - Builds the kernel using the ARM64 cross-compiler linker.ld - Linker script that places code at address 0x80000 (standard for Raspberry Pi)
  
- config.txt
  - Raspberry Pi boot configuration:
    - Enables 64-bit mode
    - Loads the initramfs at address 0x20000000

## bootloader

The bootloader in bootloader is a two-stage boot system that allows you to load and execute different kernel images without reflashing the SD card.

The bootloader acts as an intermediary that:

- Boots first from the SD card (as bootloader.img)
- Waits for commands via UART serial connection
- Receives a new kernel over the serial connection
- Relocates itself to a different memory location
- Loads and executes the received kernel

- start.s
  - ARM64 assembly code that relocates the bootloader from 0x80000 to 0x60000
  - Sets up the stack pointer and clears the BSS section
  - Jumps to the C main function

- Memory Layout

    ```txt
    Before Relocation:
    0x60000: [empty]
    0x80000: [bootloader code]

    After Relocation:
    0x60000: [bootloader code]  ← relocated here
    0x80000: [empty]            ← ready for kernel

    After Kernel Load:
    0x60000: [bootloader code]
    0x80000: [received kernel]  ← loaded here, then executed
    ```
- Usage Workflow
- Flash bootloader to SD card as bootloader.img
- Boot Raspberry Pi - bootloader starts and waits
- Connect via serial: screen /dev/ttyUSB0 115200
- Type "boot" in the serial terminal
- Run loader script: python3 [send_loader.py](http://_vscodecontentref_/6)-f kernel8.img
- Kernel loads and executes automatically

## test

- export path
```sh
export PATH=/home/perry/cross_compiler/arm-gnu-toolchain-14.3.rel1-x86_64-aarch64-none-elf/bin:$PATH
```

### Option 1: Test Kernel Directly (Simplest)

```sh
cd lab2/kernel
make
qemu-system-aarch64 -M raspi3b -kernel kernel8.img -serial null -serial stdio -display none -initrd initramfs.cpio -dtb bcm2710-rpi-3-b-plus.dtb
```

```txt
(base) perry@NinjaCastle:~/git_repos/osc2024/lab2/kernel$ qemu-system-aarch64 -M raspi3b -kernel kernel8.img -serial null -serial stdio -display none -initrd initramfs.cpio -dtb bcm2710-rpi-3-b-plus.dtb
0x08200000
found initrd in 0x082005B0
Booted, start testing simple_alloc
Command: char* string = simple_alloc(8);
0x00080C80
1234567
0x00080C88
# ls
.
file1
file2.txt
# help
help    : print all available commands
ls      : list all files
cat     : show content of file
# cat
Filename: file1
this is file1
# 
```

### ~~Option 2: Test Bootloader + Kernel (Full Workflow)~~

#### note

- do not use this with qemu
- When QEMU redirects the second serial port (UART1) to your terminal's stdio, which is typically `/dev/pts/X`, we should not send binary data directly to it as it may interfere with the console. Thus this approach is not recommended.

1. build
```sh
cd lab2/bootloader
make
cd ../kernel  
make
```

2. run bootloader
```sh
cd lab2/bootloader
qemu-system-aarch64 -M raspi3b -kernel bootloader.img -serial null -serial stdio -display none
```
3. In another terminal, find the pts device for QEMU
```sh
# In another terminal while QEMU is running:
ls -la /proc/$(pgrep qemu)/fd/ | grep pts
```
```txt
(base) perry@NinjaCastle:~/git_repos/osc2024/lab2/kernel$ ls -la /proc/$(pgrep qemu)/fd/ | grep pts
lrwx------ 1 perry perry 64 Jul 30 20:53 0 -> /dev/pts/4
lrwx------ 1 perry perry 64 Jul 30 20:53 1 -> /dev/pts/4
```
4. In another terminal, simulate the loader script
```sh
# Type "boot" in the QEMU terminal first 
cd lab2/kernel
python3 ../bootloader/send_loader.py -s /dev/pts/4 -f kernel8.img
```

### ~~Option3:Use the TCP redirection method~~

#### note

There is something wrong with the TCP redirection method, it does not work as expected. The bootloader does not receive the kernel image correctly.

```sh
# Start QEMU with TCP serial
cd lab2/bootloader
qemu-system-aarch64 -M raspi3b -kernel bootloader.img -serial null -serial tcp::1234,server,nowait -display none

# In another terminal, connect to interact
telnet localhost 1234
# sudo apt install inetutils-telnet
```
```sh
#Send kernel via TCP (in another terminal):
cd lab2/kernel
python3 send_loader_tcp.py --host localhost -p 1234 -f kernel8.img
```

debug

```sh
ls -la kernel8.img
#(base) perry@NinjaCastle:~/git_repos/osc2024/lab2/kernel$ ls -la kernel8.#img
#-rwxr-xr-x 1 perry perry 3200 Jul 30 21:12 kernel8.img
```



## debug

```sh
#1st terminal
cd lab2/kernel
make
qemu-system-aarch64 -M raspi3b -kernel kernel8.img -serial null -serial stdio -display none -initrd initramfs.cpio -dtb bcm2710-rpi-3-b-plus.dtb -s -S
#2nd terminal
cd lab2/kernel
aarch64-none-elf-gdb kernel8.img
```

```sh
#(gdb) 
file kernel8.elf
target remote localhost:1234
break shell
print (char*)cpio_base
set $cpio = 0x8000000
x/50s (char*)cpio_base #This shows up to 50 null-terminated strings starting from cpio_base.
```