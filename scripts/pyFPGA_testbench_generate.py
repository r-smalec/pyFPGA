# Script for Verilog simple testbench generation.
# You copy signals of a module to be tested and after running
# this script code is ready to paste to a proper file. All you
# need is to change default module name.
#
# IMPORTANT: change directory to ".../scripts/"
#
# EXAMPLE
#
# What you copy:                   
#
# input       [2:0]   sel,         
# input       [23:0]  in0, //inputs
# input       [23:0]  in1,         
# input       [23:0]  in2,         
# input       [23:0]  in3,         
# input       [23:0]  in4,         
# input       [23:0]  in5,         
# input       [23:0]  in6,         
# input       [23:0]  in7,         
# output reg  [23:0]  out // output

import pyperclip
import subprocess

original_copy = pyperclip.paste()
module_init_script = "pyFPGA_module_init.py"
signals_declaration_script = "pyFPGA_signals_declaration.py"

testbench_code = "`timescale 1ns / 1ps\n\n"
testbench_code += "module example_tb;\n\n"
testbench_code += "parameter PERIOD = 10;\nparameter HALF_PERIOD = PERIOD / 2;\nparameter TWICE_PERIOD = PERIOD * 2;\n\n"
try:
    subprocess.run(["python", signals_declaration_script])
except subprocess.CalledProcessError as e:
    print(f"Script error: {e}")
    pyperclip.copy("")
    quit()
testbench_code += pyperclip.paste() # save code after initializing signals

pyperclip.copy(original_copy)
try:
    subprocess.run(["python", module_init_script])
except subprocess.CalledProcessError as e:
    print(f"Script error: {e}")
    pyperclip.copy("")
    quit()

testbench_code += "\nexample UUT (\n"
testbench_code += pyperclip.paste() # save code after module initialization
testbench_code += "\n);\n\n"

testbench_code += "initial begin\n\tclk = 1'b1;\n\tforever begin\n\t\t#HALF_PERIOD clk = ~clk;\n\tend\nend\n\n"
testbench_code += "initial begin\n\trstn <= 1'b0;\n\t#TWICE_PERIOD rstn <= 1'b1;\n\n\t#100 $finish();\nend\n\n"
testbench_code += "endmodule\n"
print(testbench_code)
pyperclip.copy(testbench_code)
