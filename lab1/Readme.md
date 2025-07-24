# lab 1

## install compiler

```sh
wget https://developer.arm.com/-/media/Files/downloads/gnu/14.3.rel1/binrel/arm-gnu-toolchain-14.3.rel1-x86_64-aarch64-none-elf.tar.xz
tar -xf arm-gnu-toolchain-14.3.rel1-x86_64-aarch64-none-elf.tar.xz
export PATH=$PWD/arm-gnu-toolchain-12.3.rel1-x86_64-aarch64-none-elf/bin:$PATH
export PATH=/home/perry/cross_compiler/arm-gnu-toolchain-14.3.rel1-x86_64-aarch64-none-elf/bin:$PATH
```

## Arm Assembly

```arm
mrs //move to register from state register (for processer)
cbz //compare and branch if zero
ldr //load register
str //store
cbnz //compare and branch if not zero
bl //branch with link
```

### start.s

This is ARM64 (AArch64) assembly code for a bare-metal or OS kernel entry point. Here’s what it does:

1. CPU Core Selection:

    Reads the CPU ID (mpidr_el1).
    If not core 0, enters an infinite low-power wait (wfe loop).
    Only core 0 continues.
2. Stack Initialization:

    Sets the stack pointer (sp) just before the code at _start.
3. BSS Clearing:

    Clears the .bss section (uninitialized data) by zeroing memory from __bss_start for __bss_size words.
4. Jump to C Code:

    Calls the main function (presumably in C).
    If main returns, halts the core in a wfe loop.

## linker

Links the object files into one executable(``kernel8.img`` in this case), relocates text, data in several object files.
* Load kernel to 0x80000
* Present data at correct memort address and set program counter

## Mini UART (Universal Asynchronous Receiver/Transmitter)

### MMIO (Memory-Mapped IO)

Map hardware on device into a memory address for IO.

The memory-mapped I/O (MMIO) base address is set using the macro MMIO_BASE, which is typically defined in a header file (gpio.h). In your code, all UART register pointers (like AUX_MU_IO) are defined as offsets from MMIO_BASE

### uart.c

- pointers

    ```c
    #define AUX_ENABLE      ((volatile unsigned int*)(MMIO_BASE+0x00215004))
    ```

- Simple Shell
    
    Save the received character into buffer and compare with the command when recieved '\n'.

### Mailbox

### run

#### makefile

A Makefile is a text file used by the make build automation tool to define how to compile and link programs

- SRCS = $(wildcard *.c): Finds all .c source files in the directory.
- OBJS = $(SRCS:.c=.o): Converts the list of .c files to .o object files.
- The line start.o: start.S declares that start.o depends on start.S, meaning that if start.S changes, start.o should be rebuilt.
- Targets:

    - all: clean kernel8.img: The default target. Runs clean first, then builds kernel8.img.
    - start.o: start.S: Compiles the assembly file start.S to start.o using the ARM64 cross-compiler.
    - %.o: %.c: Compiles each .c file to a .o object file.
    - kernel8.img: start.o $(OBJS): Links all object files into kernel8.elf using the linker script, then converts it to a raw binary image kernel8.img.
      - The target kernel8.img depends on start.o and all object files listed in $(OBJS), ensuring that any changes to these files will trigger a rebuild.
    - clean: Removes build artifacts (kernel8.img, kernel8.elf, and all .o files).
    - run: Runs the kernel image in QEMU, emulating a Raspberry Pi 3B and showing ARM instructions.
- run
  - qemu-system-aarch64 -M raspi3b -kernel kernel8.img -d in_asm
    -qemu-system-aarch64: Runs QEMU in AArch64 (ARM 64-bit) mode.
    -M raspi3b: Emulates a Raspberry Pi 3 Model B.
    -kernel kernel8.img: Loads your kernel image as the boot kernel.
    -d in_asm: Enables QEMU's instruction tracing (shows executed assembly).
  - qemu-system-aarch64 -M raspi3b -kernel kernel8.img -serial null -serial stdio -display none
    -serial null: Disables UART0.
    -serial stdio: Redirects UART1 to your terminal (standard input/output).
    -display none: Disables the graphical display.

#### cmds

```sh
cd lab1
make # build
make run # run qemu
make clean # clear files
```