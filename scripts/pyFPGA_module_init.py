# Script for Verilog modules initialization
#
# EXAMPLE
#
# What you copy:                                    What you get:
#
# input       [2:0]   sel,                          .sel(sel),
# input       [23:0]  in0, //inputs                 .in0(in0), // inputs
# input       [23:0]  in1,                          .in1(in1),
# input       [23:0]  in2,             === \        .in2(in2),
# input       [23:0]  in3,             =    \       .in3(in3),
# input       [23:0]  in4,             =    /       .in4(in4),
# input       [23:0]  in5,             === /        .in5(in5),
# input       [23:0]  in6,                          .in6(in6),
# input       [23:0]  in7,                          .in7(in7),
# output reg  [23:0]  out // output                 .out(out) // output


import pyperclip

lines_original = pyperclip.paste().split('\n')
lines = ""
if len(lines_original) > 0:
    last_dir = lines_original[0].split()[0]
else:
    print("\nERROR: no data in cache\n")
    quit()

if last_dir in ["input", "output", "inout"]:

    for line_original_no in range(0, len(lines_original)):
        line = lines_original[line_original_no].split()
        
        if len(line) > 0:
            comment = ""
            for i in range(0, len(line)):
                if line[i].find("//") >= 0: # comment found in a string
                    comment = ' '.join(line[i:])
                    line = line[0:i]
                    break

            line[-1] = line[-1].replace(',', '')
            var_name = line[-1]
            dir = line[0]
            # uncomment to add empty line between two type of ports
            # if dir != last_dir:
            #     dir = last_dir
            #     lines += "\n" 

            if dir in ["input", "output", "inout"]:

                if line_original_no == len(lines_original) - 1:
                    lines += "\t." + var_name + "("+ var_name + ") " + comment + "\n"
                else:
                    lines += "\t." + var_name + "("+ var_name + "), " + comment + "\n"

            else:
                lines += "\n" + ''.join(line) + "\n"

    print(lines)
    pyperclip.copy(str(lines))
else:
    print("\nERROR: invalid data in cache, data should start from: input, output or inout keyword\n")
    quit()
