# pulsebox
Arbitrary digital pulse sequence generator with delay-loop timing [(arXiv)](https://arxiv.org/abs/1801.02433)

## Output channels and trigger pins
The Arduino pins for the output channels are chosen so that they all belong to a single PIO PORT (PORTC)

![The output channels and trigger pin layout](examples/pins.png)

channel | PORTC bit | Arduino pin | channel | PORTC bit | Arduino pin | 
--------|-----------|-------------|---------|-----------|-------------|
   1    |     1     |     33      |    9    |    12     |     51      |
   2    |     3     |     35      |   10    |     2     |     34      |
   3    |     5     |     37      |   11    |     4     |     36      |
   4    |     7     |     39      |   12    |     6     |     38      |
   5    |     9     |     41      |   13    |     8     |     40      |
   6    |    18     |     45      |   14    |    19     |     44      |
   7    |    16     |     47      |   15    |    17     |     46      |
   8    |    14     |     49      |   16    |    15     |     48      |

**Trigger channel:** Arduino pin 52

## Connecting an external clock source
Locate the onboard quartz oscillator on your board. Remove it, along with the two capacitors on its sides. Four soldering points are left underneath the oscillator. Connect the central pin of a coaxial connector to the upper left one, and the ground of the connector to the lower left one.

![image](examples/ext_clock_connection.png)

The external clock signal should be a unipolar rectangular signal with 3.3 V amplitude and 50 % duty cycle. Its frequency should be in the 3 to 20 MHz range. 12 MHz is the default (the frequency of the onboard oscillator). This frequency is eventually multiplied by a factor of 7, which for a 12 MHz clock source leads to a 84 MHz master clock.