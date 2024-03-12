# Script for generating constraint file for Libero and Vivado using netltst
# of signals used in the design and Altium Pin Report File generated from 
# schematic component. 
# Required is to define appropreiate files one for Pin Report File (pin_mapping_file_ori)
# second for constraints (.pdc for Libero and .xdc for Vivado)

def replace_characters_in_pin_mapping(in_file_path, out_file_path):
    with open(in_file_path, 'r') as in_file:
        constraints = in_file.readlines()
        constraints_mod = ""
        for line in constraints:
            if any(keyword in line for keyword in ['GND', 'VDD', 'VSS', 'VPP']):
                pass
            else:
                if '\\' in line:
                    line = line.replace('\\', '')
                    line = line.split(',')
                    line[1] = ''.join(line[1:2]) + '_N\n' ## if signal is negated addd _N on the end
                    line = line[0:2]
                    constraints_mod = constraints_mod + ','.join(line)
                else:
                    line = line.split(',')
                    if len(str(line[1:2])) > 4: # 4 is for [''] which is empty string
                        line[1] = ''.join(line[1:2]) # assign to net name
                        if line[1][-1].isdigit():
                            for i in range(2, len(line[1])):
                                if line[1][-i].isdigit(): # add \[num\] if pin name ends with a number what mmns it is part of a vector
                                    pass
                                else:
                                    line[1] = line[1][:-(i-1)] + '\\[' + line[1][-(i-1):]
                                    break
                            line[1] = line[1] + '\\]\n'
                        else:
                            line[1] = line[1] + '\n'
                        line = line[0:2] # limit contents to pin designator and net name
                        constraints_mod = constraints_mod + ','.join(line)
    
    with open(out_file_path, 'w') as out_file:
        out_file.write(constraints_mod)

def search_pin_mapping(pin_mapping_file_path, pin_name):
    matching_pin = ""
    with open(pin_mapping_file_path, 'r') as in_file:
        lines = in_file.readlines()
        for line in lines:
            if pin_name in line:
                line = line.split(',')
                matching_pin = line[0]
                break

    return matching_pin

def assign_constraints(in_file_path, out_file_path, pin_mapping_file_path):
    curr_line = ""
    with open(in_file_path, 'r') as in_file, open(out_file_path, 'w') as out_file:
        lines = in_file.readlines()
        for line in lines:
            line = str(line).split(' ')
            if 'set_io' in line or 'set_property' in line:
                if '-pinname' in line or 'PACKAGE_PIN' in line:
                    out_file.write(' '.join(line))
                else:
                    pin_name = ''.join(line[1:2])
                    matching_pin = search_pin_mapping(pin_mapping_file_path, pin_name)
                    #print(pin_name)
                    #print(matching_pin)
                    #TODO if pdc elif xdc
                    if len(matching_pin) > 0: # if matching pin was exist
                        mod_line = ' '.join(line)[:-1] + " -pinname " + matching_pin + "\n"
                    else:
                        mod_line = ' '.join(line)[:-1] + "\n"
                    
                    out_file.write(mod_line)
            else:
                out_file.write(' '.join(line))

pin_mapping_file_ori = 'data\pin_mapping.csv' # generated from Altium (Schematic->Component->Right click->Pin Mapping)
pin_mapping_file_mod = 'data\pin_mapping_mod.csv'
constraints_file_ori = 'data\constraints.pdc' # *.pdc for Libero and *.xdc for Vivado
constraints_file_mod = 'data\constraints_mod.pdc'

replace_characters_in_pin_mapping(pin_mapping_file_ori, pin_mapping_file_mod)
assign_constraints(constraints_file_ori, constraints_file_mod, pin_mapping_file_mod)
