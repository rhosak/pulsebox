# pulsebox
Arbitrary digital pulse sequence generator with delay-loop timing [(arXiv)](https://arxiv.org/abs/1801.02433)

R. Hošák and M. Ježek, Rev. Sci. Inst. 89, 045103 (2018). https://doi.org/10.1063/1.5019685

The software is now in the process of being cleaned up. It will be available **soon**!
In the meantime, we will share the basic concepts here.

## Connecting an external clock source
Locate the onboard quartz oscillator on your board. Remove it, along with the two capacitors on its sides. Four soldering points are left underneath the oscillator. Connect the central pin of a coaxial connector to the upper left one, and the ground of the connector to the lower left one.

![image](examples/ext_clock_connection.png)

The external clock signal should be a unipolar rectangular signal with 3.3 V amplitude and 50 % duty cycle. Its frequency should be in the 3 to 20 MHz range. 12 MHz is the default (the frequency of the onboard oscillator). This frequency is eventually multiplied by a factor of 7, which for a 12 MHz clock source leads to a 84 MHz master clock.
