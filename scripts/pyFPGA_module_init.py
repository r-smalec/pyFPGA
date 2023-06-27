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

    for line_original_no in range(0, len(lines_original)):
        line = lines_original[line_original_no].split()
        
        if len(line) > 0:
            if line[0].find("/") >=0: # line with a comment
                lines += ' '.join(line) + "\n"

            else:
                comment = ""
                for i in range(0, len(line)):
                    if line[i].find("//") >= 0: # comment found in a string
                        comment = ' '.join(line[i:])
                        line = line[0:i]
                        break

                line[-1] = line[-1].replace(',', '')

                var_dir = line[0]
                var_name = line[-1]

                # uncomment to add empty line between two type of ports
                # if var_dir != var_dir_prev:
                #     var_dir = var_dir_prev
                #     lines += "\n" 

                tabs = "\t" * int(  8 - int((len(var_name) + 1) / 4)    )

                if line_original_no == len(lines_original) - 1:
                    lines += "\t." + var_name + "\t" + tabs + "("+ var_name + ") " + comment + "\n"
                else:
                    lines += "\t." + var_name + "\t" + tabs + "("+ var_name + "), " + comment + "\n"

    print(lines)
    pyperclip.copy(str(lines))

else:
    print("\nERROR: no data in cache\n")
    quit()