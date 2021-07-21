# pulsebox
Arbitrary digital pulse sequence generator (_pulsebox_) with delay-loop timing, based on Arduino Due.

This repository accompanies the paper by R. Hošák and M. Ježek ([arXiv preprint](https://arxiv.org/abs/1801.02433), [published in Rev. Sci. Inst. 89, 045103 (2018)](https://doi.org/10.1063/1.5019685))

Here we wish to share two main parts of the project:
1. [The concepts](#the-concepts):
   - How to use Arduino Due as a pulse sequence generator
   - What makes up the appropriate `.ino` source file
   - How to control Arduino Due using lower-level instructions
      + How to change the state of numerous digital pins at once
      + How to produce very precise delays ranging from tens of nanoseconds to seconds and more.
2. [The software](#the-software): Python package used to
   - Configure the Arduino Due as a pulse sequence generator
   - Read a user specification of a multi-channel digital pulse sequence
   - Generate, compile, and upload the appropriate code to Arduino Due
   - Provide a graphical user interface to enable all of the above

## The concepts
An arbitrary digital pulse sequence generator, or _pulsebox_, is an electronic device with a number of digital channels. It can change the states of these channels very quickly and with great timing precision, and can thus create complex sequences of multi-channel digital patterns, or pulse sequences.

Arduino Due is a general-purpose development board. It is based on a 32-bit Atmel SAM3X8E microcontroller (ARM Cortex-M3 architecture) running at 84 MHz.

## The software
