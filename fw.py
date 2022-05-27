# eigenstates of tight-binding finite square potential well in 1D
import sys
import os
if'../lib/' not in sys.path:
    sys.path.append('../lib/')
import numpy as np
import math
#from numpy import linalg as la
from scipy import linalg as la
#from npext import *
import npext
import cmath
import itertools as it
#from scipy.special import binom as binom
import kpath
#from chern import chern

def h(v, nsys=100, nwell=20, wbeg=None):
    """v: depth of the potential, in unit of hopping t (t=1)
    
    nsys:  system size
    nwell: potential well size
    wbeg:  beginning position of the potential well. If not given, then put potential well at center of system
    """
    hdiag = np.zeros(nsys, dtype=np.double)
    if wbeg == None:
        wbeg = (nsys-nwell)//2

    hdiag[wbeg:wbeg+nwell] = v
    res = np.diag(hdiag)
    i,j = np.indices((nsys,nsys))
    res[i==j-1] = -1
    res[i==j+1] = -1
    return res
def export_h(v, nsys=200, nwell=10, wbeg=None, fn='fw'):
    labels_eig = 'erg'
    header_eig = '#' + '\t'.join(['%d:%s'%(i+1,txt) for i,txt in enumerate(labels_eig.split())])

    labels_u = 'n x psi(x)'
    header_u = '#' + '\t'.join(['%d:%s'%(i+1,txt) for i,txt in enumerate(labels_u.split())])

    dat_eig = open(fn + '-eig.dat', 'w')
    dat_u = open(fn + '-u.dat', 'w')

    print(header_eig, dat_eig)
    print(header_u, dat_u)

    hh = h(v, nsys, nwell, wbeg)
    eig,u = la.eigh(hh)

    print('\n'.join(['%g'%ee for ee in eig]), file=dat_eig)
    for n in range(nsys):
        psi_n = u[:,n]
        for x,psi in zip(range(nsys),psi_n):
            print('%d\t%d\t%g'%(n,x,psi), file=dat_u)
        dat_u.write('\n')

    dat_eig.close()
    dat_u.close()

def export_h_boundstate(v, nsys=200, nwell=50, wbeg=None, fn='fw-eigu'):
    labels = 'n En x v(x) psi_n(x)'
    header = '#' + '\t'.join(['%d:%s'%(i+1,txt) for i,txt in enumerate(labels.split())])

    #fn = fn + '-v=%1.2f'%v
    par = open(fn + '.par', 'w')
    txt = """
    v = %g
    nsys = %d
    nwell = %d
    wbeg = '%s'
    """%(v,nsys,nwell,wbeg)
    print(txt,file=par)

    with open(fn + '.dat', 'w') as dat:
        print(header, file=dat)
        hh = h(v,nsys,nwell,wbeg)
        vx = np.diag(hh)              #potential profile
        eig,u = la.eigh(hh)
        eig = eig[eig < -2] + 2       # only keep bound states
        nbound = eig.shape[0]         # number of bound states
        par.write('nbound = %d\n'%nbound)
        for n in range(nbound):
            erg_n = eig[n]
            psi_n = u[:,n]
            psi_n *= (psi_n[nsys/2]/np.abs(psi_n[nsys/2]))   # pick a stable sign convention
            for x in range(nsys):
                print('%d\t%g\t%d\t%g\t%g'%(n,erg_n,x,vx[x],psi_n[x]), file=dat)
            dat.write('\n')

    par.close()

def scan_v(vfrom=-0.5, vto=0, dv=0.01):
    for v in np.arange(vfrom,vto,dv):
        export_h_boundstate(v, nsys=200, nwell=20, wbeg=None, fn='scan_v/fw-eigu-v=%1.2f'%v)
