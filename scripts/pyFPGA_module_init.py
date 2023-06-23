# Script for Verilog modules initialization
#
# EXAMPLE
#
# What you copy:                           What you get:
#
# input       [2:0]   sel,                .sel(sel),
# input       [23:0]  in0,                .in0(in0),
# input       [23:0]  in1,                .in1(in1),
# input       [23:0]  in2,   === \        .in2(in2),
# input       [23:0]  in3,   =    \       .in3(in3),
# input       [23:0]  in4,   =    /       .in4(in4),
# input       [23:0]  in5,   === /        .in5(in5),
# input       [23:0]  in6,                .in6(in6),
# input       [23:0]  in7,                .in7(in7),
#
# output reg  [23:0]  out                 .out(out)


import pyperclip

lines_original = pyperclip.paste().split('\n')
lines = ""
if len(lines_original) > 0:
    last_dir = lines_original[0].split()[0]
else:
    print("\nERROR: no data in cache\n")
    quit()

if last_dir == "input" or last_dir == "output" or last_dir == "inout":

    for line_original in lines_original:
        line = line_original.split()
        if len(line) > 0:
            line[-1] = line[-1].replace(',', '')
            var_name = line[-1]
            dir = line[0]

            if dir != last_dir:
                dir = last_dir
                lines += "\n"

            lines += "  ." + var_name + "("+ var_name + "),\n"
    lines = lines[:-2]
    print(lines)
    pyperclip.copy(str(lines))
else:
    print("\nERROR: invalid data in cache, data should start from: input, output or inout keyword\n")
    quit()
