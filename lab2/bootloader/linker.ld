SECTIONS
{
    . = 0x60000; /*start loading from 0x60000*/
    
    /*: {} means to combine sub-part into the section. 
    The sub-parts might be generated to .o files by compiler*/
    /* KEEP ensures the symbol will not be discarded after optimizing */
    
    .text : { KEEP(*(.text.boot)) *(.text .text.* .gnu.linkonce.t*) }
    .rodata : { *(.rodata .rodata.* .gnu.linkonce.r*) }
    PROVIDE(_data = .); /* let _data = current address */
    .data : { *(.data .data.* .gnu.linkonce.d*) }
    .bss (NOLOAD) : { /*don't require space in executable*/
        . = ALIGN(16); /*align with 16 bit for efficiency*/
        /*put all .bss, .bss. segments and other segments into .bss */
        __bss_start = .; 
        *(.bss .bss.*)
        *(COMMON)
        __bss_end = .;
    }
    _end = .;
    
    /* some unneed segments */
   /DISCARD/ : { *(.comment) *(.gnu*) *(.note*) *(.eh_frame*) }
}
__bss_size = (__bss_end - __bss_start)>>3; /* bss size for start.S */
__bootloader_size = (_end - 0x60000)>>3;