# lab3 

## Exceptions

When a CPU takes an exception, it does the following things.
* Save the current processor’s state(PSTATE) in SPSR_ELx. (x is the target Exception level)
* Save the exception return address in ELR_ELx.
* Disable its interrupt. (PSTATE.{D,A,I,F} are set to 1).
* If the exception is a synchronous exception or an SError interrupt, save the cause of that exception in ESR_ELx.
* Switch to the target Exception level and start at the corresponding vector address.

After the exception handler finishes, it issues eret to return from the exception. Then the CPU,
* Restore program counter from ELR_ELx.
* Restore PSTATE from SPSR_ELx.
* Switch to the corresponding Exception level according to SPSR_ELx.

### ARM Exception Level

- Firmware: EL3
- Default while booted: EL2
- OS: EL1
- Program: EL0

### Disable Interrupts 

>can interrupts happen during the handling of an exception?
  - Yes, interrupts can happen during exception handling, but only if their priority is higher and if masking settings permit it.

  - Exception Priority: Faults like HardFault or NMI usually have higher priority and can interrupt lower-priority exceptions or ISRs.
>so what about the masked exceptions, are they just left unhandled?
  - Not quite — masked exceptions aren’t ignored forever, but their handling is deferred rather than abandoned.

In ARM Cortex-M microcontrollers, the NVIC (Nested Vectored Interrupt Controller) tracks interrupts using a few key registers:
- Pending Register (ISPR): This holds interrupt requests that have occurred but couldn’t be serviced due to masking or priority.
- Enable Register (ISER): Indicates which interrupts are allowed to fire.
- Active Register (IABR): Flags which interrupts are currently being serviced.

### Asynchronous Exception

In the ARMv8-A architecture, especially when working with AArch64 state, these three—**IRQ**, **FIQ**, and **SError**—are types of **asynchronous exceptions**, which are essentially interrupts. Here's a breakdown:

#### ⚡ IRQ (Interrupt Request)
- **Purpose**: Standard interrupt used for general-purpose signaling from peripherals.
- **Priority**: Lower than FIQ.
- **Masking**: Controlled by the `PSTATE.I` bit. If set, IRQs are masked (ignored).
- **Typical Use**: Timer interrupts, UART, GPIO events.

---

#### 🚨 FIQ (Fast Interrupt Request)
- **Purpose**: Designed for high-priority, low-latency interrupt handling.
- **Priority**: Higher than IRQ.
- **Masking**: Controlled by the `PSTATE.F` bit.
- **Typical Use**: Time-critical tasks like real-time audio or motor control.

---

#### 🛠️ SError (System Error)
- **Purpose**: Signals serious system-level faults, often related to hardware failures or memory corruption.
- **Masking**: Controlled by the `PSTATE.A` bit.
- **Behavior**: Can be fatal or require system recovery; not typically used for routine interrupt handling.

## updates

el2 to el1 at the beginning of the start.S
el1 to el0
el0 to el1

## UART Interrupt (Peripheral)

## Timer Multiplexing

### timer
* callback function: the task to do when expired
* data: the data for callback funct (ex. message)
* expires: time of expiring

### add_timer
1. check is there spare timer by the expire time
2. allocate a timer with the expire time (current + after)
3. check is there a timer with lower expire time, if none, set interrupt

### timer_handler
1. check which timers to expire
2. callback and clear the timer by set expires to 0
3. disable core timer
4. check if there is another timer awaiting

## Task Queue
### Modification
uart interrupt: disable write interrupt to avoid a lot of writing task

### Enqueue
Place tasks into the queue during handling with priority (the smaller the higher)


### Queue
* Enqueue: allocate to a spare place and check the priorty
* Execute: Start executing with the lowest priority (FIFO), then update lowest priority and execute next

## run

User program is a loop.
```sh
export PATH=/home/perry/cross_compiler/arm-gnu-toolchain-14.3.rel1-x86_64-aarch64-none-elf/bin:$PATH
qemu-system-aarch64 -M raspi3b -kernel kernel8.img -serial null -serial stdio -display none -initrd initramfs.cpio -dtb bcm2710-rpi-3-b-plus.dtb
```