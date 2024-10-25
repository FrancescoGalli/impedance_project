def generate_circuit():
    return '(R1C1[C2Q1])'

def test_empty_string():
    """Checks that the string is not empty"""
    circuit_string = generate_circuit()
    assert (circuit_string), 'empty string'

def test_open_brakets():
    """Checks that there is an open round or square bracket as first character
       in the string"""
    circuit_string = generate_circuit()
    assert (circuit_string[0]=='(' or circuit_string[0]=='['),(
           'no initial open bracket detected')

def test_close_brakets():
    """Checks that there is a close round or square bracket as last character in
       the string"""
    circuit_string = generate_circuit()
    assert (circuit_string[-1]==')' or circuit_string[-1]==']'), (
           'no final close bracket detected')

def test_different_number_brackets():
    """Checks that there is an equal number of close and open bracket, for both
       square and round types"""
    circuit_string = generate_circuit()
    assert (circuit_string.count('(') == circuit_string.count(')')
            or circuit_string.count('[') == circuit_string.count(']')), (
                'inconsistent number of open and close brackets')

def test_consistency_brackets():
    """
    Given a string with an equal number of open and close brackets of the same type
    (round or square), checks if there is a consistency among the brackets
    """
    circuit_string = generate_circuit()
    position_of_brackets = [i for i, _ in enumerate(circuit_string) 
                            if (circuit_string.startswith(')', i) 
                                or circuit_string.startswith(']', i)) ]                                                              
    cut_parameter = 0
    for _ in position_of_brackets:
        for i, char_i in enumerate(circuit_string):
            if(char_i==')' or char_i==']'):
                if char_i==')': bracket, wrong_bracket='(', '['
                if char_i==']': bracket, wrong_bracket='[', '('
                found=False
                analyzed_string=circuit_string[:i]
                for j, _ in enumerate(analyzed_string):
                    if (circuit_string[len(analyzed_string)-1-j]==bracket 
                        and found==False):
                        found = True
                        bracket_index = len(analyzed_string)-1-j
                        index_wrong_bracket = circuit_string[
                            bracket_index+1:i].find(wrong_bracket)
                        assert index_wrong_bracket==-1, (
                            'inconsistent \'' + wrong_bracket + '\' at '
                            + str(index_wrong_bracket + bracket_index + 1 + cut_parameter)
                            + ': ' + circuit_string)
                        circuit_string = circuit_string[:bracket_index] + circuit_string[
                            bracket_index+1:i]+circuit_string[i+1:]
                        cut_parameter += 2
                        break
                if found:
                    break

def test_characters():
    """
    Checks that a string containes only valid characters:
    '(', ')', '[', ']', 'C', 'Q', 'R' and natural numbers
    """
    circuit_string = generate_circuit()
    wrong_characters=''
    wrong_characters_index=[]
    for i, char in enumerate(circuit_string):
        if (char not in {'(', ')', '[', ']', 'C', 'Q', 'R'} 
                and not char.isnumeric()):
            wrong_characters+= '\''+char+'\', '
            wrong_characters_index.append(i)
    assert not wrong_characters, (
         'Invalid character(s) ' + wrong_characters + ' at '
         + str(wrong_characters_index) + ' in ' + circuit_string
         + '. Only round and square brackets, C, Q, R and natural numbers are allowed')
        
def test_element_consistency():
    """
    Checks the element consistency of a string that containes only valid characters: 
    each element is composed by a capital letter among {'C', 'Q', 'R'} followed by a
    natural number
    """
    circuit_string = generate_circuit()
    wrong_elements=''
    wrong_element_index=[]
    for i, char in enumerate(circuit_string):
        if (char in {'C', 'Q', 'R'} and circuit_string[-1]!=char):
            if not circuit_string[i+1].isnumeric():
                wrong_elements+= '\''+char+str(circuit_string[i+1])+'\', '
                wrong_element_index.append(i)
        elif (char.isnumeric() and circuit_string[0]!=char):
            if not (circuit_string[i-1] in {'C', 'Q', 'R'}):
                wrong_elements+= '\''+str(circuit_string[i-1])+char+'\', '
                wrong_element_index.append(i-1)
    assert not wrong_elements, ('element inconsistency for '+ wrong_elements +
                                ' at ' + str(wrong_element_index) + ': ' 
                               + circuit_string + '. An element is composed by a '
                               + 'valid letter followed by a natural number')
        
def test_duplicates():
    """
    Checks that there are no duplicates inside a string that containes 
    only valid characters and has element consistency
    """
    circuit_string=generate_circuit()
    for i, char in enumerate(circuit_string):
        if (char.isnumeric() and circuit_string[0]!=char):
            precedent_char=circuit_string[i-1]
            rest_of_string=circuit_string[:i-1]+circuit_string[i+1:]
            duplicate_elements = [k+1 for k, _ in enumerate(rest_of_string) 
                                    if (rest_of_string.startswith(char, k) and 
                                    rest_of_string.startswith(precedent_char, k-1))]
            assert  not duplicate_elements, (
                            'element \''+str(circuit_string[i-1:i+1])
                            +'\' at '+str(i-1)+' has duplicate(s) at '+str(duplicate_elements)+': '+circuit_string
                            +' An element is composed by a valid character '
                            +'followed by a number')
            
def generate_parameters():
    p1=1000
    p2=1e-6
    p3=2e-6
    p4=([1.5e-6, 10.5])
    parameters=([p1,p2,p3,p4])
    return parameters

def test_type():
    """
    Checks that the only valid types as parameters are float, integer and lists
    """
    parameters=generate_parameters()
    wrong_type=''
    wrong_type_index=[]
    for i, parameter in enumerate(parameters):
        if (type(parameter)!=float and type(parameter)!=int and type(parameter)!=list):
            wrong_type+= '\''+str(parameter)+'\', '
            wrong_type_index.append(i)
    assert not wrong_type, ('type error for parameter(s) number ' + str(wrong_type_index) + ' '
                            + wrong_type + ' in ' + str(parameters) 
                            + '. Parameters can only be floats, integers or lists')

def test_values():
    """
    Checks that the float parameters are positive
    """
    parameters=generate_parameters()
    wrong_value=''
    wrong_value_index=[]
    for i, parameter in enumerate(parameters):
        if (type(parameter)==float or type(parameter)==int):
            if parameter<=0:
                wrong_value+= '\''+str(parameter)+'\', '
                wrong_value_index.append(i)
    assert not wrong_value, ('value error for parameter(s) number ' + str(wrong_value_index) + ' '
                            + wrong_value + ' in ' + str(parameters) 
                            + '. Float parameters must be positive')
        
def test_list_two_elements():
    """
    Checks that the list parameters contain exactly 2 parameters
    """
    parameters=generate_parameters()
    wrong_elements=''
    wrong_elements_index=[]
    for i, parameter in enumerate(parameters):
        if type(parameter)==list:
            if len(parameter)!=2:
                wrong_elements_index.append(i)
                wrong_elements+= '\''+str(parameter)+'\', '
    assert not wrong_elements, ('type error for parameter(s) number ' 
                                + str(wrong_elements_index) + ': \'' + wrong_elements 
                                + '\' in ' + str(parameters) 
                                + '. Lists parameters must contain exactly 2 parameters')

def test_list_type():
    """
    Checks that the list parameters (assumed to be of length 2) contain only floats or
    integers
    """
    parameters=generate_parameters()
    wrong_types=''
    wrong_types_index=[]
    for i, parameter in enumerate(parameters):
        if type(parameter)==list:
            for _, p in enumerate(parameter):
                if (type(p)!=float and type(p)!=int):
                    wrong_types+= '\''+str(p)+'\', '
                    wrong_types_index.append(i)
    assert not wrong_types, ('type error for parameter(s) '+ wrong_types  +' in parameter(s) number ' 
                                + str(wrong_types_index) + ' contained in: \'' 
                                + '\' in ' + str(parameters) 
                                + '. Lists parameters must only contain floats or integers')

def test_list_value():
    """
    Checks that the two object (float or integer) contained in the list parameters meet
    the value requirements: the first one is positive, the second one is between 0 and 1
    """
    parameters=generate_parameters()
    wrong_value=''
    wrong_value_index=''
    for i, parameter in enumerate(parameters):
        if type(parameter)==list:
            if parameter[0]<=0:
                    wrong_value+= '\''+str(parameter[0])+'\', '
                    wrong_value_index+='first of ['+str(i)+']'
            if (parameter[1]<0 or parameter[1]>1):
                    wrong_value+= '\''+str(parameter[1])+'\', '
                    wrong_value_index+='second of ['+str(i)+']'
    assert not wrong_value, ('type error for parameter(s) '+ wrong_value
                             + wrong_value_index + ' parameter(s) ' + ' contained in: \'' 
                             + str(parameters) + '. Lists parameters must contain as '
                             + 'first parameter a positive float and as second parameter '
                             + 'a float between 0 and 1')

def elements():
    """
    Return the list of elements ('C', 'Q' or 'R' ) of a string. Used for testing
    """
    circuit_string = generate_circuit()
    elements=[]
    for char in circuit_string:
        if char in {'C', 'Q', 'R'}:
            elements.append(char)
    return elements

def test_parameter_length():
    """
    Checks that the list of elements and the list of parameters have the same size
    """
    elements_array=elements()
    parameters=generate_parameters()
    assert len(elements_array)==len(parameters), (
        'parameters list size and element count must be the same. Parameters size: '
        + str(len(parameters)) + ', element count: ' + str(len(elements_array)))

def test_parameters_match():
    """
    Checks that there is a consistent correspondance between the elements and the 
    parameters: C and R must have a float as parameter, Q a list
    """
    elements_array=elements()
    parameters=generate_parameters()
    wrong_match=''
    wrong_match_index=[]
    for i, element in enumerate(elements_array):
        if element in {'C', 'R'}:
            if (type(parameters[i])!=float and type(parameters[i])!=int):
                wrong_match += '\'[' + str(element) + ',' + str(parameters[i]) + ']\', '
                wrong_match_index.append(i)
        else:
            if (type(parameters[i])!=list):
                wrong_match += '\'[' + str(element) + ',' + str(parameters[i]) + ']\', '
                wrong_match_index.append(i)
    print(wrong_match, wrong_match_index)
    assert not wrong_match, ('bad match for '+ wrong_match + ' in ' + str(wrong_match_index)
                             + ': elements \'' + str(elements_array) + ' with parameters '
                             + str(parameters) + '. \'R\' and \'C\' elements must have '
                             + 'a float as parameter, \'Q\' must have a list')





class Circuit:
    def __init__(self, string, parameters, p_const):
        self.string = string
        self.values = parameters
        self.p_const = p_const



#circuit_string = input('Enter the equivalent circuit: ')

#test_open_brakets()
#test_empty_string()
#test_different_number_brackets()
#test_consistency_brackets()
#test_characters()
#test_element_consistency()
#test_duplicates()

#test_type()
#test_list_two_elements()
#test_list_type()
#test_values()
#test_list_value()
#test_parameter_length()
#test_parameters_match()

