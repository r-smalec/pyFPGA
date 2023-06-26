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
# output              single_ended_out,  ====/
#                                                   IBUFDS  diff_in1_inst (
#                                                       .I   (diff_in_p[1]),
#                                                       .IB  (diff_in_n[1]),
#                                                       .O   (diff_in[1])
#                                                   );
#
#                                                   OBUFDS  diff_out_inst (
#                                                       .I   (diff_out_p),
#                                                       .IB  (diff_out_n),
#                                                       .O   (diff_out)
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

                var_dir = line[0]
                var_name = line[-1]

                # uncomment to add empty line between two type of ports
                # if var_dir != var_dir_prev:
                #     var_dir = var_dir_prev
                #     lines += "\n" 

                if line_original_no == len(lines_original) - 1:
                    lines += "\t." + var_name + "("+ var_name + ") " + comment + "\n"
                else:
                    lines += "\t." + var_name + "("+ var_name + "), " + comment + "\n"

    print(lines)
    pyperclip.copy(str(lines))

else:
    print("\nERROR: no data in cache\n")
    quit()