extern volatile unsigned int mailbox[36];


//#define MBOX_REQUEST    0

/* channels */
// #define MBOX_CH_POWER   0
// #define MBOX_CH_FB      1
// #define MBOX_CH_VUART   2
// #define MBOX_CH_VCHIQ   3
// #define MBOX_CH_LEDS    4
// #define MBOX_CH_BTNS    5
// #define MBOX_CH_TOUCH   6
// #define MBOX_CH_COUNT   7
// #define MBOX_CH_PROP    8

/* tags */
// #define MBOX_TAG_GETSERIAL      0x10004
// #define MBOX_TAG_LAST           0

int mbox_call();
int get_board_revision();
int get_arm_memory();