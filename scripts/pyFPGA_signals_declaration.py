# Script for Verilog signals declaration
#
# EXAMPLE
#
# What you copy:                          What you get:
#
# input       [2:0]   sel,                reg       [2:0]   sel;
# input       [23:0]  in0,                reg       [23:0]  in0;
# input       [23:0]  in1,                reg       [23:0]  in1;
# input       [23:0]  in2,   === \        reg       [23:0]  in2;
# input       [23:0]  in3,   =    \       reg       [23:0]  in3;
# input       [23:0]  in4,   =    /       reg       [23:0]  in4;
# input       [23:0]  in5,   === /        reg       [23:0]  in5;
# input       [23:0]  in6,                reg       [23:0]  in6;
# input       [23:0]  in7,                reg       [23:0]  in7;
# output reg  [23:0]  out                 wire      [23:0]  out;

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

                var_dir = line[0] # input, output or inout
                var_type = "wire" # wire or reg
                var_size = "" # [end:begining]
                var_name = line[-1] # name

########################## decode line construction ##########################
                if len(line) == 3:                  # for line: <dir> <type/size> <name>
                    if line[1] in ["wire", "reg"]:
                        var_type = line[1]
                    else:
                        var_size = line[1]

                elif len(line) == 4:                # for line: <dir> <type> <size> <name>
                    var_type = line[1]
                    var_size = line[2]
                
                else:                               # for line: <dir> <name>
                    pass

########################## adjust line parameters ##########################

                if var_dir.find("input") >= 0:
                    var_type = "reg"

                elif var_dir.find("output") >= 0:
                    if var_type == "reg":
                        var_type = "wire"
                    else:
                        var_type = "reg"

                # uncomment to add empty line between two type of ports
                # if var_dir != var_dir_prev:
                #     var_dir = var_dir_prev
                #     lines += "\n" 

                lines += var_type + "\t" + var_size + "\t" + var_name + "; " + comment + "\n"

    print(lines)
    pyperclip.copy(str(lines))

else:
    print("\nERROR: no data in cache\n")
    quit()