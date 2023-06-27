# Script for Verilog differential signals pack 
# into IBUFFDS for input and OBUFDS for output
#
# EXAMPLE
#
# What you copy:                                    What you get:
#
# input       [1:0]   diff_in_n,                    IBUFDS  diff_in0_inst (
# input       [1:0]   diff_in_p,                        .I   (diff_in_p[0]),
# input               single_ended_in,   ====\          .IB  (diff_in_n[0]),
# output              diff_out_n,        =    \         .O   (diff_in[0])
# output              diff_out_p,        =    /     );
# output              single_ended_out   ====/
#                                                   IBUFDS  diff_in1_inst (
#                                                       .I   (diff_in_p[1]),
#                                                       .IB  (diff_in_n[1]),
#                                                       .O   (diff_in[1])
#                                                   );
#
#                                                   OBUFDS  diff_out_inst (
#                                                       .I   (diff_out),
#                                                       .O   (diff_out_p),
#                                                       .OB  (diff_out_n)
#                                                   );

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

########################## check if var is differential ##########################
                if(var_name[-2:] != "_p"):
                    continue

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

########################## calculate var length ##########################
                var_size_left = -1
                var_size_right = -1
                if len(var_size) > 0:
                    for ch in var_size:
                        if ch.isdigit():
                            if var_size_left < 0:
                                var_size_left = int(ch)
                            else:
                                var_size_right = int(ch)
                
                var_length = var_size_left - var_size_right

                if var_length == 0:
                    if var_dir == "input":
                            lines += "\nIBUFDS " + var_name[:-2] + "_inst (\n\t.I\t(" + var_name + "),\n\t.IB\t(" + var_name[:-2] + "_n),\n\t.O\t(" + var_name[:-2] + ")\n);\n" 


                    elif var_dir == "output":
                            lines += "\nOBUFDS " + var_name[:-2] + "_inst (\n\t.I\t(" + var_name[:-2] + "),\n\t.O\t(" + var_name + "),\n\t.OB\t(" + var_name[:-2] + "_n)\n);\n"
                
                else:
                
                    if var_dir == "input":
                            for i in range(0, var_length + 1):
                                lines += "\nIBUFDS " + var_name[:-2] + str(i) + "_inst (\n\t.I\t(" + var_name + "[" + str(i) + "]),\n\t.IB\t(" + var_name[:-2] + "_n[" + str(i) + "]),\n\t.O\t(" + var_name[:-2] + "[" + str(i) + "])\n);\n" 


                    elif var_dir == "output":
                            for i in range(0, var_length + 1):
                                lines += "\nOBUFDS " + var_name[:-2] + str(i) + "_inst (\n\t.I\t(" + var_name[:-2] + "[" + str(i) + "]),\n\t.O\t(" + var_name + "[" + str(i) + "]),\n\t.OB\t(" + var_name[:-2] + "_n[" + str(i) + "])\n);\n"

    print(lines)
    pyperclip.copy(str(lines))

else:
    print("\nERROR: no data in cache\n")
    quit()