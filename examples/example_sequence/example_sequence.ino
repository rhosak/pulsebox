/* example.ino
 * 2018 Radim Hosak <radim.hosak01@upol.cz>
 */
void setup() {
   /* Disabling interrupts */
   for (int i = 1; i<=78; i++)
      detachInterrupt(i); 
   void __disable_irq(void);
   
   /* Configuring pins for output
    * We use exclusively the GPIO port C.
    * Our channel-to-pin assignment:
    * 
    * ch1: bit 1 (Arduino pin 33)
    * ch2: bit 3 (Arduino pin 35)
    * ch3: bit 5 (Arduino pin 37)
    * ch4: bit 7 (Arduino pin 39)
    * ch5: bit 9 (Arduino pin 41)
    * ch6: bit 18 (Arduino pin 45)
    * ch7: bit 16 (Arduino pin 47)
    * ch8: bit 14 (Arduino pin 49)
    * ch9: bit 12 (Arduino pin 51)
    * ch10: bit 2 (Arduino pin 34)
    * ch11: bit 4 (Arduino pin 36)
    * ch12: bit 6 (Arduino pin 38)
    * ch13: bit 8 (Arduino pin 40)
    * ch14: bit 19 (Arduino pin 44)
    * ch15: bit 17 (Arduino pin 46)
    * ch16: bit 15 (Arduino pin 48)
    * 
    */
   REG_PIOC_OER = 0b11111101001111111110;
   REG_PIOC_OWER = 0b11111101001111111110;

   /* Choose one of the modes of operation below: */
   
   /* Continuously-running mode:
    * Run the sequence in an endless while loop
    * with some fixed delay.
    */
    while (true) {
       sequence();
       delay(100);
    }

   /* Interrupt mode:
    * Run sequence after a rising edge is detected
    * on Arduino pin 52.
    * 
    * attachInterrupt(52, sequence, RISING);
    */
}

void sequence() {
   /* We write the desired output state into REG_PIOC_ODSR. */
   /* ABOUT ASM LOOPS:
    * 1. The loop iteration variable is a 32bit value, so it must
    * be moved into the register R1 in two steps.
    * First, the bottom 16 bits (hexadecimal 0x0000 -- 0xffff)
    * are moved using MOVW. Then, the top 16 bits are moved using MOVT.
    * 
    * 2. To make conditional branching inside the loop possible, each delay loop
    * needs to have a label (we choose LOOP#, where # is a unique number throughout
    * the entire .ino code).
    * 
    * 3. We have experimented with various forms of the delay loop. Removing the NOP
    * inside the loop, or replacing the 'SUB R1, #1' and 'CMP R1, #0' with just one
    * instruction 'SUBS R1, #1' might yield slightly different results, especially
    * the delay loop granularity.
    */
   REG_PIOC_ODSR = 0b10; // ch1 on
   asm volatile (
      "MOVW R1, #0x14\n"  // 20 iterations, approx 1.2 microsec delay
      "MOVT R1, #0x0\n"
      "LOOP0:\n\t"
      "NOP\n\t"
      "SUB R1, #1\n\t"
      "CMP R1, #0\n\t"
      "BNE LOOP0\n"
   );
   REG_PIOC_ODSR = 0b100000;  // ch1 off, ch3 on
   asm volatile (
      "MOVW R1, #0x32\n"  // 50 iterations, approx. 3 microsec delay
      "MOVT R1, #0x0\n"
      "LOOP1:\n\t"
      "NOP\n\t"
      "SUB R1, #1\n\t"
      "CMP R1, #0\n\t"
      "BNE LOOP1\n"
   );
   REG_PIOC_ODSR = 0b1010;  // ch3 off, ch1 and ch2 on
   asm volatile (
      "MOVW R1, #0x14\n"  // 20 iterations, approx 1.5 microsec delay
      "MOVT R1, #0x0\n"
      "LOOP2:\n\t"
      "NOP\n\t"
      "SUB R1, #1\n\t"
      "CMP R1, #0\n\t"
      "BNE LOOP2\n"
   );
   REG_PIOC_ODSR = 0b1000;  // ch1 off, ch2 still on
   asm volatile (
      "MOVW R1, #0x1e\n"  // 30 iterations, approx 2 microsec delay
      "MOVT R1, #0x0\n"
      "LOOP3:\n\t"
      "NOP\n\t"
      "SUB R1, #1\n\t"
      "CMP R1, #0\n\t"
      "BNE LOOP3\n"
   );
   REG_PIOC_ODSR = 0b1010;  // ch1 on, ch2 still on
   asm volatile (
      "MOVW R1, #0xa\n"  // 10 iterations, approx. 600 ns delay
      "MOVT R1, #0x0\n"
      "LOOP4:\n\t"
      "NOP\n\t"
      "SUB R1, #1\n\t"
      "CMP R1, #0\n\t"
      "BNE LOOP4\n"
   );
   REG_PIOC_ODSR = 0b10;  // ch2 off, ch1 still on
   asm volatile (
      "MOVW R1, #0x3c\n"  // 60 iterations, approx. 3.6 microsec delay
      "MOVT R1, #0x0\n"
      "LOOP5:\n\t"
      "NOP\n\t"
      "SUB R1, #1\n\t"
      "CMP R1, #0\n\t"
      "BNE LOOP5\n"
   );
   REG_PIOC_ODSR = 0b101010;  // ch2 and ch3 on, ch1 still on
   asm volatile (
      "MOVW R1, #0xa\n"  // 10 iterations, approx. 600 ns delay
      "MOVT R1, #0x0\n"
      "LOOP6:\n\t"
      "NOP\n\t"
      "SUB R1, #1\n\t"
      "CMP R1, #0\n\t"
      "BNE LOOP6\n"
   );
   REG_PIOC_ODSR = 0b101000;  // ch1 off, ch2 and ch3 still on
   asm volatile (
      "MOVW R1, #0xa\n"  // 10 iterations, approx. 600 ns delay
      "MOVT R1, #0x0\n"
      "LOOP7:\n\t"
      "NOP\n\t"
      "SUB R1, #1\n\t"
      "CMP R1, #0\n\t"
      "BNE LOOP7\n"
   );
   REG_PIOC_ODSR = 0b100000;  // ch2 off, ch3 still on
   asm volatile (
      "MOVW R1, #0x14\n"  // 20 iterations, approx 1.2 microsec delay
      "MOVT R1, #0x0\n"
      "LOOP8:\n\t"
      "NOP\n\t"
      "SUB R1, #1\n\t"
      "CMP R1, #0\n\t"
      "BNE LOOP8\n"
   );
   REG_PIOC_ODSR = 0b0;  // ch 3 off
   /* And now some quick pulses on ch1.
    * Each pulse approx. 24 ns
    */
   /* ABOUT ADDING NOP:
    * The pulses can be prolonged by adding the following NOP instruction:
    * asm volatile("NOP\n");
    * Unfortunately, when more NOPs are used in different places, the lengths of the pulses
    * might not be as expected and need to be verified. This is because of the inner
    * workings of the MCU, especially the instruction pipelining, that we have no
    * control over. Hopefully, we will find a more reliable 'no operation instruction
    * equivalent' to use in the future.
    */
   REG_PIOC_ODSR = 0b10;
   REG_PIOC_ODSR = 0b0;
   REG_PIOC_ODSR = 0b10;
   REG_PIOC_ODSR = 0b0;
   REG_PIOC_ODSR = 0b10;
   REG_PIOC_ODSR = 0b0;
   REG_PIOC_ODSR = 0b10;
   REG_PIOC_ODSR = 0b0;
}

void loop() {
   ;
}
