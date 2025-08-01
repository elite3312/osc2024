# lab 1

## path

```sh
export PATH=/home/perry/cross_compiler/arm-gnu-toolchain-14.3.rel1-x86_64-aarch64-none-elf/bin:$PATH
```


#### debug

```sh
#Terminal 1 (Start QEMU with GDB server)
cd lab1_debug
make debug
```

```sh
#Terminal 2 (Connect GDB to QEMU)
cd lab1_debug
# Use the ARM64 GDB from your cross-compiler
/home/perry/cross_compiler/arm-gnu-toolchain-14.3.rel1-x86_64-aarch64-none-elf/bin/aarch64-none-elf-gdb kernel8.elf

# In GDB prompt:
(gdb) target remote localhost:1234
(gdb) break main
(gdb) continue
(gdb) info registers
(gdb) disassemble
(gdb) step
(gdb) next
```

```sh
# Set breakpoints
break _start
break main
break uart_init

# Examine memory
x/10x 0x80000    # examine 10 hex words at address 0x80000
x/10i $pc        # examine 10 instructions at program counter

# View registers
info registers
info registers all

# Step through code
stepi            # step one instruction
nexti            # next instruction (skip function calls)
continue         # continue execution

# Memory mapping
info mem         # show memory regions
```