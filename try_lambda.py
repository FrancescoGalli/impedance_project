import numpy as np
import matplotlib.pyplot as plt

def plotGraph(x_vector,y_vector):
    plt.plot(x_vector,y_vector, '-o')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Frequency(Hz)')
    plt.ylabel('Impedance(Ohm)')
    plt.show()

    
"""

function fHndl=serialComb(ZFHandleCell)
%return the equivalent impedance function of two Z elements in series. ZFHandleCell is the array of the (two) expressions, Ztmp
nF=length(ZFHandleCell);
fHndl=@(p,w)zeros(size(w));
for i=1:nF
    fh=ZFHandleCell{i};
    fHndl=@(p,w)fHndl(p,w)+fh(p,w); %serialComb
end

end

function fHndl=parallelComb(ZFHandleCell)
%return the equivalent impedance function of two Z elements in parallel. ZFHandleCell is the array of the (two) expressions, Ztmp
nF=length(ZFHandleCell);
fHndl=@(p,w)zeros(size(w));
for i=1:nF
    fh=ZFHandleCell{i};
    fHndl=@(p,w)fHndl(p,w)+1./fh(p,w); %parallelComb^(-1)
end

fHndl=@(p,w)1./fHndl(p,w); %parallelComb

end
"""



def impedance_R(r,w):
    #definition of impedance for resistances
    return r+0j*np.zeros(len(w))

def impedance_C(c,w):
    #definition of impedance for capacitors
    return 1./(1j*w*c)

def impedance_Q(Q,n,w):
    #definition of impedance for constant phase element
    return 1./(Q*w**n*np.exp(np.pi/2*n*1j))

"""
def serialComb(ZFHandleCell):
    #%return the equivalent impedance function of two Z elements in series. ZFHandleCell is the array of the (two) expressions, Ztmp
    nF=len(ZFHandleCell)
    fHndl=@(p,w)zeros(size(w))
    for i=1:nF
       fh=ZFHandleCell[i]
       fHndl=@(p,w)fHndl(p,w)+fh(p,w)
"""

def add(f1,f2):
    fsum = lambda parameters, x: f1(parameters,x) + f2(parameters,x)
    return fsum




logf=np.linspace(1,5,100)
f=10.**logf
w=f*2*np.pi
#w=np.array([1,10])

r1=100
r2=1000
c=1e-6
Q=1e-3
n=2
pr=([r1,r2,c,Q,n])

Z1 = lambda pr, w: impedance_R(r1,w)
Z2 = lambda pr, w: impedance_R(r2,w)
ZCell=([Z1,Z2])
Z3= lambda pr, w: impedance_C(c,w)
Z4=lambda pr, w: impedance_Q(Q,n,w)


#print(Z1(pr,w))
#print(Z2(pr,w))
print(Z3(pr,w))
print(Z4(pr,w))
fHndl=lambda pr, w: 0
fHndl=add(fHndl, Z1)
fHndl=add(fHndl, Z2)
#print(fHndl(pr,w))

plotGraph(w, abs(Z3(pr,w)))







#x=np.array([1,2,3])
Za = lambda x, y: x+y
Zb = lambda x, y: x*y
#div=lambda x,y: 1./Za(x,y)+1./Zb(x,y)