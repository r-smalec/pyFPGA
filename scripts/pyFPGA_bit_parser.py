# Script to generate binary/hexadecimal form of frames
# using provided frame format. For example "0aab bbb1"
# stands for frame consist of 0, 2-bit number "a", 3-bit
# number "b" and 1. Script asks for "a" and "b" in decimal
# and generates frame which is ready to paste

import pyperclip

################### CONFIGURABLE FRAME FORMAT ###################
frame_format = "0sst trrr rrrc cccc cccc cmmm mmmm wwww wwwb bbbb"
#################################################################

def count_letters(input_string):
    letter_count = {}
    
    for char in input_string:
        if char.isalpha():
            if char in letter_count:
                letter_count[char] += 1
            else:
                letter_count[char] = 1
    
    return letter_count

letters_structure = count_letters(frame_format)
letters_values = dict(letters_structure)

for letter in letters_structure:
    num = 0
    max_num = 2**letters_structure[letter] - 1
    print(letter + " (max is {max}): ".format(max = max_num))
    while True:
        while True:
            temp_num = input()
            if temp_num.isnumeric():
                temp_num = int(temp_num)
                break
            else:
                print("Input is not numeric")
        if temp_num <= max_num:
            letters_values[letter] = bin(temp_num)[2:].zfill(letters_structure[letter]) # adjust length of a value in binary representation
            break
        else:
            print("Input too big")

#print(letters_structure)   
#print(letters_values)
frame = ""
prev_char = ""
for char in frame_format:
    if char == "0":
        frame += "0"
    elif char == "1":
        frame += "1"
    elif char != prev_char and char.isalpha():
        frame += letters_values[char]
        prev_char = char
print("Bianry format: " + frame)
frame = int(frame, 2)
hex_digits = int(len(frame_format.replace(" ", "")) / 4)
frame = hex(frame)[2:].zfill(hex_digits)
print("Hex format: " + frame)
pyperclip.copy(frame)