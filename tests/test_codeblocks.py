#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from pulsebox import codeblocks, config


class HeaderTest(unittest.TestCase):
    """Tests for the header code block
    """
    
    def test_default_header(self):
        self.assertEqual(codeblocks.header(),
                         f"/* {config.header} */",
                         "Did not produce correctly formated default header.")
    
    def test_empty_input(self):
        self.assertEqual(codeblocks.header(""), None,
                         '`header("")` should produce no header: `None`.')
    
    def test_strip_commentend(self):
        msg = "Test message */ but now it's code */*/ /*/ */* /"
        correct = "/* Test message  but now it's code  / * / */"
        self.assertEqual(codeblocks.header(msg), correct,
                         "Comment ending sequence `*/` stripped incorrectly.")


class SetupTest(unittest.TestCase):
    """Tests for the setup code block
    """
    
    def test_no_input(self):
        """Test that `codeblocks.setup()` produces setup for continuously
        running pulsebox with the default delay.
        """
        correct = "void setup() {\n" \
                  "   for (int i=1; i<=78; i++)\n" \
                  "      detachInterrupt(i);\n" \
                  "   void __disable_irq(void);\n" \
                  f"   REG_PIOC_OER = {config.all_pins_enabled};\n" \
                  f"   REG_PIOC_OWER = {config.all_pins_enabled};\n" \
                  "   while(1) {\n" \
                  "      sequence();\n" \
                  f"      delay({config.cont_mode_delay_ms});\n" \
                  "   }\n" \
                  "}\n\n" \
                  "void sequence() {"
        self.assertEqual(codeblocks.setup(), correct,
                         "The default setup code block is incorrect.")

    def test_default_cont(self):
        """Test that `codeblocks.setup(triggered=False)` behaves correctly.
        """
        correct = "void setup() {\n" \
                  "   for (int i=1; i<=78; i++)\n" \
                  "      detachInterrupt(i);\n" \
                  "   void __disable_irq(void);\n" \
                  f"   REG_PIOC_OER = {config.all_pins_enabled};\n" \
                  f"   REG_PIOC_OWER = {config.all_pins_enabled};\n" \
                  "   while(1) {\n" \
                  "      sequence();\n" \
                  f"      delay({config.cont_mode_delay_ms});\n" \
                  "   }\n" \
                  "}\n\n" \
                  "void sequence() {"
        self.assertEqual(codeblocks.setup(triggered=False), correct,
                         "The default setup code block for cont. mode" \
                         "is incorrect.")

    def test_default_trig(self):
        """Test that `codeblocks.setup(triggered=True)` behaves correctly.
        """
        correct = "void setup() {\n" \
                  "   for (int i=1; i<=78; i++)\n" \
                  "      detachInterrupt(i);\n" \
                  "   void __disable_irq(void);\n" \
                  f"   REG_PIOC_OER = {config.all_pins_enabled};\n" \
                  f"   REG_PIOC_OWER = {config.all_pins_enabled};\n" \
                  f"   attachInterrupt({config.trigger_pin}, " \
                                       "sequence, RISING);\n" \
                  "}\n\n" \
                  "void sequence() {"
        self.assertEqual(codeblocks.setup(triggered=True), correct,
                         "The default setup code block for trig. mode" \
                         "is incorrect.")

    def test_delay_point_zero_conversion(self):
        """Test that ints represented as floats like 4.0 are accepted.
        """
        correct = "void setup() {\n" \
                  "   for (int i=1; i<=78; i++)\n" \
                  "      detachInterrupt(i);\n" \
                  "   void __disable_irq(void);\n" \
                  f"   REG_PIOC_OER = {config.all_pins_enabled};\n" \
                  f"   REG_PIOC_OWER = {config.all_pins_enabled};\n" \
                  "   while(1) {\n" \
                  "      sequence();\n" \
                  "      delay(4);\n" \
                  "   }\n" \
                  "}\n\n" \
                  "void sequence() {"
        self.assertEqual(codeblocks.setup(triggered=False, parameter=4.0),
                         correct,
                         "Conversion of integer-like float 4.0 to int failed.")

    def test_delay_scientific_conversion(self):
        """Test that integers in scientific notation like 1e2 are accepted.
        """
        
        correct = "void setup() {\n" \
                  "   for (int i=1; i<=78; i++)\n" \
                  "      detachInterrupt(i);\n" \
                  "   void __disable_irq(void);\n" \
                  f"   REG_PIOC_OER = {config.all_pins_enabled};\n" \
                  f"   REG_PIOC_OWER = {config.all_pins_enabled};\n" \
                  "   while(1) {\n" \
                  "      sequence();\n" \
                  "      delay(100);\n" \
                  "   }\n" \
                  "}\n\n" \
                  "void sequence() {"
        self.assertEqual(codeblocks.setup(triggered=False, parameter=1e2),
                         correct,
                         "Conversion of integer-like float 1e2 to int failed.")

    def test_non_int_delay(self):
        with self.assertRaises(TypeError):
            codeblocks.setup(triggered=False, parameter=3.14)
        with self.assertRaises(TypeError):
            codeblocks.setup(triggered=False, parameter="four")
        with self.assertRaises(TypeError):
            codeblocks.setup(triggered=False, parameter="12e-1")
            
    def test_non_32bit_delay(self):
        with self.assertRaises(ValueError):
            codeblocks.setup(triggered=False, parameter=-1)
        with self.assertRaises(ValueError):
            codeblocks.setup(triggered=False, parameter=2**32)

    def test_non_int_trigger(self):
        with self.assertRaises(TypeError):
            codeblocks.setup(triggered=True, parameter=3.14)
        with self.assertRaises(TypeError):
            codeblocks.setup(triggered=True, parameter="four")
        with self.assertRaises(TypeError):
            codeblocks.setup(triggered=True, parameter="12e-1")

    def test_invalid_trigger_pin(self):
        with self.assertRaises(ValueError):
            codeblocks.setup(triggered=True, parameter=-1)
        with self.assertRaises(ValueError):
            codeblocks.setup(triggered=True, parameter=79)

    def test_overlapping_trigger(self):
        """See that trigger pin cannot be identical to a pulsebox pin.
        """
        for pin in config.pulsebox_pins:
            with self.assertRaises(ValueError):
                codeblocks.setup(triggered=True, parameter=pin)


class StateChangeTest(unittest.TestCase):
    """Tests for the state_change code block
    """
    
    def test_not_enough_channels(self):
        for channel_count in range(0, config.pulsebox_pincount):
            states = [0] * channel_count
            with self.assertRaises(ValueError):
                codeblocks.state_change(states)

    def test_too_many_channels(self):
        states = [0] * (config.pulsebox_pincount + 1)
        with self.assertRaises(ValueError):
            codeblocks.state_change(states)
    
    def test_all_to_zero(self):
        all_zeros = [0] * len(config.pulsebox_pins)
        correct = "   REG_PIOC_ODSR = 0b0;"
        self.assertEqual(codeblocks.state_change(all_zeros), correct,
                         "Setting all to zero yields non-zero register.")

    def test_all_to_one(self):
        all_ones = [1] * len(config.pulsebox_pins)
        correct = f"   REG_PIOC_ODSR = {config.all_pins_enabled};"
        self.assertEqual(codeblocks.state_change(all_ones), correct,
                         "Setting all to one yields incorrect result.")

    def test_all_singles(self):
        """Test that setting each channels to high individually is correct.
        """
        for channel, pin in enumerate(config.pulsebox_pins):
            states = [0] * config.pulsebox_pincount
            states[channel] = 1
            
            odsr = bin(1 << pin)
            correct = f"   REG_PIOC_ODSR = {odsr};"
            self.assertEqual(codeblocks.state_change(states), correct,
                             "Incorrect REG_PIOC_ODSR for single channel.")


class LoopTest(unittest.TestCase):
    """Tests for the loop code block
    """
    
    def test_non_int_iters(self):
        with self.assertRaises(TypeError):
            codeblocks.loop(3.14)
        with self.assertRaises(TypeError):
            codeblocks.loop("four")
        with self.assertRaises(TypeError):
            codeblocks.loop(triggered=False, parameter="12e-1")
            
    def test_non_32bit_iters(self):
        with self.assertRaises(ValueError):
            codeblocks.loop(-1)
        with self.assertRaises(ValueError):
            codeblocks.loop(2 ** 32)

    def test_zero_iters_forbidden(self):
        with self.assertRaises(ValueError):
            codeblocks.loop(0)

    def test_iters_point_zero_conversion(self):
        """Test that ints represented as floats like 4.0 are accepted.
        """
        correct = "   asm volatile (\n" \
                  '      "MOVW R1, #0x4\\n"\n' \
                  '      "MOVT R1, #0x0\\n"\n' \
                  '      "LOOP0:\\n\\t"\n' \
                  '      "NOP\\n\\t"\n' \
                  '      "SUB R1, #1\\n\\t"\n' \
                  '      "CMP R1, #0\\n\\t"\n' \
                  '      "BNE LOOP0\\n"\n' \
                  "   );"
        self.assertEqual(codeblocks.loop(4.0), correct,
                         "Conversion of integer-like float 4.0 to int failed.")

    def test_iters_scientific_conversion(self):
        """Test that integers in scientific notation like 1e2 are accepted.
        """
        correct = "   asm volatile (\n" \
                  '      "MOVW R1, #0x64\\n"\n' \
                  '      "MOVT R1, #0x0\\n"\n' \
                  '      "LOOP0:\\n\\t"\n' \
                  '      "NOP\\n\\t"\n' \
                  '      "SUB R1, #1\\n\\t"\n' \
                  '      "CMP R1, #0\\n\\t"\n' \
                  '      "BNE LOOP0\\n"\n' \
                  "   );"
        self.assertEqual(codeblocks.loop(1e2), correct,
                         "Conversion of integer-like float 1e2 to int failed.")
    
    def test_one_iter_loop(self):
        correct = "   asm volatile (\n" \
                  '      "MOVW R1, #0x1\\n"\n' \
                  '      "MOVT R1, #0x0\\n"\n' \
                  '      "LOOP0:\\n\\t"\n' \
                  '      "NOP\\n\\t"\n' \
                  '      "SUB R1, #1\\n\\t"\n' \
                  '      "CMP R1, #0\\n\\t"\n' \
                  '      "BNE LOOP0\\n"\n' \
                  "   );"
        self.assertEqual(codeblocks.loop(1), correct,
                         "One-iteration delay produces wrong code.")

    def test_full_bottom(self):
        """Check that 65535 iterations fill the bottom part of the register.
        """
        correct = "   asm volatile (\n" \
                  '      "MOVW R1, #0xffff\\n"\n' \
                  '      "MOVT R1, #0x0\\n"\n' \
                  '      "LOOP0:\\n\\t"\n' \
                  '      "NOP\\n\\t"\n' \
                  '      "SUB R1, #1\\n\\t"\n' \
                  '      "CMP R1, #0\\n\\t"\n' \
                  '      "BNE LOOP0\\n"\n' \
                  "   );"
        self.assertEqual(codeblocks.loop(65535), correct,
                         "Max-16-bit-iter loop delay produces wrong code.")

    def test_full_top(self):
        """Check that 4294901760 iterations fill the top part of the register.
        """
        correct = "   asm volatile (\n" \
                  '      "MOVW R1, #0x0\\n"\n' \
                  '      "MOVT R1, #0xffff\\n"\n' \
                  '      "LOOP0:\\n\\t"\n' \
                  '      "NOP\\n\\t"\n' \
                  '      "SUB R1, #1\\n\\t"\n' \
                  '      "CMP R1, #0\\n\\t"\n' \
                  '      "BNE LOOP0\\n"\n' \
                  "   );"
        self.assertEqual(codeblocks.loop(4294901760), correct,
                         "0xffff0000 loop delay produces wrong code.")

    def test_max_iter(self):
        """Check that 4294967295 iterations fill the register completerly.
        """
        correct = "   asm volatile (\n" \
                  '      "MOVW R1, #0xffff\\n"\n' \
                  '      "MOVT R1, #0xffff\\n"\n' \
                  '      "LOOP0:\\n\\t"\n' \
                  '      "NOP\\n\\t"\n' \
                  '      "SUB R1, #1\\n\\t"\n' \
                  '      "CMP R1, #0\\n\\t"\n' \
                  '      "BNE LOOP0\\n"\n' \
                  "   );"
        self.assertEqual(codeblocks.loop(4294967295), correct,
                         "Max-iter loop delay produces wrong code.")


class EndTest(unittest.TestCase):
    """Tests for the end code block
    """
    
    def test_end(self):
        correct = "}\n\n" \
                  "void loop() {\n" \
                  "   ;\n" \
                  "}"
        self.assertEqual(codeblocks.end(), correct,
                         "The end part of the .ino code is incorrect.")
        

if __name__ == "__main__":
    unittest.main()
