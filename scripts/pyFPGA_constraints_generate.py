import csv

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
                    print(line[1:2])
                    #TODO if pdc elif xdc
                    mod_line = ' '.join(line)[:-1] + " -pinname\n"
                    out_file.write(mod_line)
            else:
                out_file.write(' '.join(line))

pin_mapping_file = 'data\pin_mapping.csv' # generated from Altium (Schematic->Component->Right click->Pin Mapping)
constraints_file_ori = 'data\constraints.pdc' # *.pdc for Libero and *.xdc for Vivado
constraints_file_mod = 'data\constraints_mod.pdc'

search_constraints(constraints_file_ori, constraints_file_mod)
