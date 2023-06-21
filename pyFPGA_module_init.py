import pyperclip

lines_org = pyperclip.paste().split('\n')
lines_trans = ""
for line in lines_org:
    name_var = line.split(' ')[0]
    lines_trans += name_var + " <= "+ name_var + "\n"
    print(lines_trans)
pyperclip.copy(str(lines_trans))