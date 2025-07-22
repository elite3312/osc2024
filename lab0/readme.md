# lab0

## install cross compiler

```sh
# wsl
sudo apt-get install make binutils gcc-aarch64-linux-gnu
```

## assembly

- a.S
  - defines a minimal infinite loop using the wfe (Wait For Event) instruction, followed by a branch back to _start.
- linker.ld
  - This line is part of a linker script, which is used by linkers like GNU ld to control how sections of a program are arranged in memory during the build process. The syntax . = 0x80000; sets the current location counter to the hexadecimal address 0x80000. The location counter determines where the next section or symbol will be placed in the output file.

  By setting . = 0x80000;, you are telling the linker that subsequent sections (such as .text, which typically contains executable code) should start at address 0x80000. This is commonly used in embedded systems or operating system kernels to ensure code is loaded at a specific memory address, which may be required by the hardware or bootloader. If this line were omitted, the linker would use its default starting address, which might not be suitable for your target environment.
```sh
aarch64-linux-gnu-gcc -c a.S # assembles the ARM64 assembly source file a.S into an object file (a.o).
aarch64-linux-gnu-ld -T linker.ld -o kernel8.elf a.o #Object file to ELF
aarch64-linux-gnu-objcopy -O binary kernel8.elf kernel8.img #This command converts the ELF executable kernel8.elf into a raw binary image kernel8.img.
```

## install QEMU

```sh
sudo apt install qemu-system
qemu-system-aarch64 --version # check
qemu-system-aarch64 -machine help|grep raspi #look for pi
```

## qemu for lab0/1

```sh
qemu-system-aarch64 -M raspi3b -kernel kernel8.img -serial null -serial stdio -display none
#first -serial null for UART0, second -serial stdio for UART1.
#display none to disable GUI

# runs QEMU to emulate a Raspberry Pi 3B and boots your kernel image
qemu-system-aarch64 -M raspi3b -kernel kernel8.img -display none -S -s
# -M raspi3b: Emulates a Raspberry Pi 3B.
# -kernel kernel8.img: Loads your kernel image.
# -display none: Disables the graphical display.
# -S: Freezes the CPU at startup (waiting for a debugger).
# -s: Starts a GDB server on TCP port 1234.
```
## gdb

```sh
sudo apt-get install gdb-multiarch #cross platform
gdb-multiarch
```
```sh
#gdb
file kernel8.elf #this allows you to inspect the elf, but you may not run it since it is arm64
target remote :1234 # this debugs the remote qemu
disassemble _start
break _start
```

## ~~write bootable image to sdb~~

- do not write to /dev/sdb in wsl! It might damage the virtual disk!
  - In WSL (Windows Subsystem for Linux), sdb usually does not exist or does not correspond to any real hardware device.
  - instead, it is probably a swap file
    
    ```txt
    Disk /dev/sdb: 186.04 MiB, 195080192 bytes, 381016 sectors
    Disk model: Virtual Disk    
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    ```
- we skip this part because we do not plan to write to a real rpi3b
```sh
# writes the contents of nycuos.img directly to the SD card device /dev/sdb
# lsblk
# dd if=nycuos.img of=/dev/sdb 
# The dd command is a Unix utility for copying and converting data at the byte level.
```

## ~~uart~~

```sh
# screen /dev/ttyUSB0 115200
# opens a serial terminal connection to the device at /dev/ttyUSB0 (usually a USB-to-serial adapter) with a baud rate of 115200. This lets you interact with your Raspberry Pi's UART output from your host machine, viewing logs or sending input over the serial connection.
```