
import numpy as np

def check_brackets(circuit_string):
    try:
        if (circuit_string.count('(') != circuit_string.count(')')
             or circuit_string.count('[') != circuit_string.count(']')):
            raise Exception('Inconsistent number of open and close brackets')
        number_of_brackets = [i for i, _ in enumerate(circuit_string) if (circuit_string.startswith(')', i)
                                                                        or circuit_string.startswith(']', i)) ]
        cut_parameter=0
        try: 
            for _ in number_of_brackets:
                for i, char_i in enumerate(circuit_string):
                    if(char_i==')' or char_i==']'):
                        if char_i==')': bracket, wrong_bracket='(','['
                        if char_i==']': bracket, wrong_bracket='[','('
                        found=False
                        analyzed_string=circuit_string[:i]
                        for j, _ in enumerate(analyzed_string):
                            if (circuit_string[len(analyzed_string)-1-j]==bracket and found==False):
                                found=True
                                bracket_index=len(analyzed_string)-1-j
                                index_wrong_bracket=circuit_string[bracket_index+1:i].find(wrong_bracket)
                                if index_wrong_bracket>-0.5:
                                    raise Exception('Inconsistent '+wrong_bracket+' at '+str(index_wrong_bracket+bracket_index+1+cut_parameter))
                                circuit_string=circuit_string[:bracket_index]+circuit_string[bracket_index+1:i]+circuit_string[i+1:]
                                cut_parameter=cut_parameter+2
                                print('New string: '+circuit_string)
                                break
                        if found:
                            break
        except Exception as message_loose_bracket:
            print(message_loose_bracket) 
    except Exception as message_inconsistent_number:
        print(message_inconsistent_number)



#circuit_string = input('Enter the equivalent circuit: ')

circuit_string='(c(1c2c3))'
print('original string: ' +circuit_string)
#print(circuit_string[3]==']')
check_brackets(circuit_string)
#print(circuit_string)



"""
i_vec=(['a','b','c','d','e','f'])
for i in range(5):
    print(i_vec[i])
    for j in range(4):
        print(j)
        if i_vec[i]=='b' or i_vec[i]=='d':
            break
"""

