import numpy as np
import matplotlib.pyplot as plt

def generate_circuit():
    return '(R1C2[R3C4])'

def generate_parameters():
    """
    p1=90
    p2=20e-6
    p3=7000
    p4=0.3e-6 
    """
    p1=228.520
    p2=34.991e-6
    p3=7000.928
    p4=0.288e-6 
    parameters=([p1, p2, p3, p4])
    return parameters

def generate_constant_array():
    constant_array = ([0, 0, 0, 0])
    return constant_array

def impedance_R(r, f):
    #definition of impedance for resistances
    return r+0j*np.zeros(len(f))

def impedance_C(c, f):
    #definition of impedance for capacitors
    #return 1./(1j*w*c)
    return 1./(1j*f*2*np.pi*c)

def impedance_Q(Q, n, f):
    #definition of impedance for constant phase element
    return 1./(Q*(f*2*np.pi)**n*np.exp(np.pi/2*n*1j))

def get_impedance_function(element_string, impedance, initial_parameters, parameters, 
                           constant_elements):
    #print('\nelement: '+element_string)
    i_element=int(element_string[1])-1
    if element_string[0]=='Z':
        impedance_element=impedance[i_element]
    elif constant_elements[i_element]:
        ptmp=initial_parameters[i_element]
        if element_string[0]=='R':
            impedance_element=lambda p, f: impedance_R(ptmp,f)
        if element_string[0]=='C':
            impedance_element=lambda p, f: impedance_C(ptmp,f)
        if element_string[0]=='Q':
            impedance_element=lambda p, f: impedance_Q(ptmp[0], ptmp[1], f)
    else:
        parameters.append(initial_parameters[i_element])
        i_parameter=len(parameters)-1
        if element_string[0]=='R':
            impedance_element=lambda p, f: impedance_R(p[i_parameter],f)
        if element_string[0]=='C':
            impedance_element=lambda p, f: impedance_C(p[i_parameter],f)
        if element_string[0]=='Q':
            impedance_element=lambda p, f: impedance_Q(p[i_parameter-1], p[i_parameter],
                                                       f)
    return impedance_element, parameters

def add(f1,f2):
    fsum = lambda parameters, x: f1(parameters,x) + f2(parameters,x)
    return fsum

def serialComb(impedance_cell):
    function_cell=lambda x, y: 0
    for i, _ in enumerate(impedance_cell):
        function_cell = add(function_cell, impedance_cell[i])
    return function_cell

def reciprocal(f):
    receprocal_f=lambda x,y:1./f(x,y)
    return receprocal_f

def parallelComb(impedance_cell):
    one_over_function_cell = lambda x, y: 0
    for impedance_element in impedance_cell:
        one_over_impedance_element = reciprocal(impedance_element)
        one_over_function_cell = add(one_over_function_cell, 
                                     one_over_impedance_element)
    function_cell = reciprocal(one_over_function_cell)
    return function_cell

def generate_impedance_function(circuit_string, initial_parameters, constant_elements):
    working=1
    index=1 #first element is just a bracket, cannot be an element
    parameters=[]
    impedance={}
    i_impedance_element=0
    while working:
        if (circuit_string[index]==')' or circuit_string[index]==']'):
            i_end=index
            if circuit_string[index]==')':
                position_of_brackets = [i for i, _ in enumerate(circuit_string[:i_end]) 
                                if circuit_string.startswith('(', i)]
            else:
                position_of_brackets = [i for i, _ in enumerate(circuit_string[:i_end]) 
                                if circuit_string.startswith('[', i)]
            i_start=position_of_brackets[-1]
            impedance_tmp=[]
            for i in range(i_start+1, i_end, 2):
                circuit_element=circuit_string[i:i+2]
                impedance_function, parameters = get_impedance_function(
                    circuit_element, impedance, initial_parameters, 
                    parameters, constant_elements)
                impedance_tmp.append(impedance_function)
                #print('parameters: '+str(parameters))
            if circuit_string[index]==')':
                impedance[i_impedance_element]=serialComb(impedance_tmp)  
            else:
                impedance[i_impedance_element]=parallelComb(impedance_tmp)
            #print_function(impedance[len(impedance)-1], parameters)
            i_impedance_element+=1
            circuit_string=circuit_string.replace(circuit_string[i_start:i_end+1], 'Z'+str(i_impedance_element))
            index=1
            #print('circuit string: '+circuit_string)
        else:
            index+=1
        if index>len(circuit_string)-1:
            working=0
    return impedance[len(impedance)-1], parameters

def print_function(function, parameters):
    logf=np.linspace(1,5,5)
    frequency=10.**logf
    #w=frequency*2*np.pi
    print('function:')
    print(function(parameters,frequency))

def plot_modulus(x_vector, y_vector):
    plt.plot(x_vector, y_vector, '-o')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Frequency(Hz)')
    plt.ylabel('Impedance(Ohm)')
    plt.show()

def plot_phase(x_vector, y_vector):
    logf=np.linspace(-1,5,100)
    plt.plot(logf, y_vector, '-o')
    #plt.xscale('log')
    plt.xlabel('Frequency(Hz)')
    plt.ylabel('Phase(deg)')
    plt.show()



class Circuit:
    def __init__(self, string, parameters, constant_elements):
        self.string = string
        self.values = parameters
        self.const = constant_elements



#circuit_string = input('Enter the equivalent circuit: ')
circuit_string = generate_circuit()
initial_parameters=generate_parameters()
constant_elements=generate_constant_array()


logf=np.linspace(-1,5,5)
frequency=10.**logf

impedance_function, parameters = generate_impedance_function(circuit_string, 
                                                             initial_parameters, 
                                                             constant_elements)
signal=impedance_function(parameters,frequency)

noise_factor=0.4
noise=noise_factor*signal*np.random.rand(len(signal))
simulated_signal = signal + noise

#plot_modulus(frequency, abs(signal))
#plot_phase(frequency, np.angle(signal)*180/np.pi)

plot_modulus(frequency, abs(simulated_signal))
plot_phase(frequency, np.angle(simulated_signal)*180/np.pi)

np.savetxt('data_impedance.txt', np.c_[frequency, simulated_signal], delimiter=',') 

