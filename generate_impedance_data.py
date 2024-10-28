import numpy as np

def generate_circuit():
    return '(C1)'

def generate_parameters():
    p1=100
    p2=1e-6
    parameters=([p1, p2])
    return parameters

def generate_constant_array():
    constant_array = ([0, 0])
    return constant_array

def impedance_R(r, w):
    #definition of impedance for resistances
    return r+0j*np.zeros(len(w))

def impedance_C(c, w):
    #definition of impedance for capacitors
    return 1./(1j*w*c)

def impedance_Q(Q, n, w):
    #definition of impedance for constant phase element
    return 1./(Q*w**n*np.exp(np.pi/2*n*1j))

def get_impedance_function(element_string, impedance, initial_parameters, parameters, 
                           constant_elements):
    print('\nelement: '+element_string)
    i_element=int(element_string[1])-1
    if element_string[0]=='Z':
        impedance_element=impedance[i_element]
    elif constant_elements[i_element]:
        ptmp=initial_parameters[i_element]
        if element_string[0]=='R':
            impedance_element=lambda p, w: impedance_R(ptmp,w)
        if element_string[0]=='C':
            impedance_element=lambda p, w: impedance_C(ptmp,w)
        if element_string[0]=='Q':
            impedance_element=lambda p, w: impedance_Q(ptmp[0], ptmp[1], w)
    else:
        parameters.append(initial_parameters[i_element])
        i_parameter=len(parameters)-1
        if element_string[0]=='R':
            impedance_element=lambda p, w: impedance_R(p[i_parameter],w)
        if element_string[0]=='C':
            impedance_element=lambda p, w: impedance_C(p[i_parameter],w)
        if element_string[0]=='Q':
            impedance_element=lambda p, w: impedance_Q(p[i_parameter-1], p[i_parameter],
                                                       w)
    return impedance_element, parameters

def add(f1,f2):
    fsum = lambda parameters, x: f1(parameters,x) + f2(parameters,x)
    return fsum

def serialComb(impedance_cell):
    function_cell=lambda x, y: 0
    for i, _ in enumerate(impedance_cell):
        function_cell = add(function_cell, impedance_cell[i])
    return function_cell


class Circuit:
    def __init__(self, string, parameters, constant_elements):
        self.string = string
        self.values = parameters
        self.const = constant_elements



#circuit_string = input('Enter the equivalent circuit: ')
circuit_string = generate_circuit()
initial_parameters=generate_parameters()
constant_elements=generate_constant_array()