# lab 1

#### cmds

```sh
cd lab1
make # build
dd if=kernel8.img of=padded.img bs=512 conv=sync # pad to 512 byte
# use pi imager to write padded.img to sd card in windows
make run # run qemu
make clean # clear files
```