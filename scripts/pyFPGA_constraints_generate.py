# Script for generating constraint file for Libero and Vivado using netltst
# of signals used in the design and Altium Pin Report File generated from 
# schematic component. 
# Required is to define appropreiate files one for Pin Report File (pin_mapping_file_ori)
# second for constraints (.pdc for Libero and .xdc for Vivado)

import csv

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
                        print(type(line[1][-1]))
                        line[1] = line[1] + '\n'
                        line = line[0:2] # limit contents to pin designator and net name
                        constraints_mod = constraints_mod + ','.join(line)
    
    with open(out_file_path, 'w') as out_file:
        out_file.write(constraints_mod)

def search_pin_mapping(pin_mapping_file, search_phrase):
    matching_rows = []
    with open(pin_mapping_file, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            for field in row:
                if search_phrase in field:
                    matching_rows.append(row)
                    break

    return matching_rows

def search_constraints(in_file_path, out_file_path):
    curr_line = ""
    with open(in_file_path, 'r') as in_file, open(out_file_path, 'w') as out_file:
        lines = in_file.readlines()
        for line in lines:
            line = str(line).split(' ')
            if 'set_io' in line or 'set_property' in line:
                if '-pinname' in line or 'PACKAGE_PIN' in line:
                    out_file.write(' '.join(line))
                else:
                    pin_name = str(line[1:2])
                    pin_location = search_pin_mapping(pin_mapping_file_mod, pin_name)
                    print(pin_name + str(pin_location))
                    #TODO if pdc elif xdc
                    mod_line = ' '.join(line)[:-1] + " -pinname \n"
                    out_file.write(mod_line)
            else:
                out_file.write(' '.join(line))

pin_mapping_file_ori = 'data\pin_mapping.csv' # generated from Altium (Schematic->Component->Right click->Pin Mapping)
pin_mapping_file_mod = 'data\pin_mapping_mod.csv'
constraints_file_ori = 'data\constraints.pdc' # *.pdc for Libero and *.xdc for Vivado
constraints_file_mod = 'data\constraints_mod.pdc'

replace_characters_in_pin_mapping(pin_mapping_file_ori, pin_mapping_file_mod)
#search_constraints(constraints_file_ori, constraints_file_mod)
