# pulsebox
Arbitrary digital pulse sequence generator (_pulsebox_) with delay-loop timing, based on Arduino Due.

This repository accompanies the paper by R. Hošák and M. Ježek ([arXiv preprint](https://arxiv.org/abs/1801.02433), [published in Rev. Sci. Inst. 89, 045103 (2018)](https://doi.org/10.1063/1.5019685)). This [bachelor's thesis](docs/BachelorsThesisRH.pdf) contains additional information that goes more in-depth on both hardware and software.

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
This board is capable of providing 26 digital (pulsebox) channels and create digital pulse sequences on them, with pulses as short as 100 ns. This is achieved by carefully using the low-level capabilities of the SAM3X8E microcontroller in conjuction with assembly language instructions.

See [Arduino pulsebox code structure](https://github.com/rhosak/pulsebox/wiki/Arduino-pulsebox-code-structure) for an overview of the code responsible for the pulsebox capabilities.

## The software
We have created a Python package which can produce the `.ino` code necessary to produce a pulse sequence according to user specification, and a GUI application to facilitate this process to the end user.

_I am currently making the code available, please be patient._ :)
