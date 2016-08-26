import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from webenmr.lib.base import BaseController, render
import numpy as n
from math import pi
import random
import mimetypes
import os, sys, shutil
from pylons import config
from webenmr.lib import RTFDoc
import tarfile

from scipy.integrate import romberg 
from scipy.integrate import quad 
from scipy.optimize import brentq
from scipy.integrate import trapz 




log = logging.getLogger(__name__)


def c(rd,cl0,A,k2):
    result= (cl0/2.)/n.cosh(A/2-k2*(rd)**2/2)*(n.exp(k2*(rd)**2/2-A/2))
    return result
    
def cpyra(h,r1,hcc,b1,cl0,A,k2):
    result= (r1*(hcc-h+b1)/hcc)**2*(cl0/2.)/n.cosh(A/2-k2*(h)**2/2)*(n.exp(k2*(h)**2/2-A/2))
    return result

def pyra(h,r1,hcc,b1):
    result= (r1*(hcc-h+b1)/hcc)**2
    return result

def funct(A,r1,r2,r3, hcc, theor, bc0,cl0,k2,b1,b2,b3,b4):
    ca = (pi*(r1**2*romberg(c,bc0,b1,args=(cl0,A,k2))+romberg(cpyra,b1,b2,args=(r1,hcc,b1,cl0,A,k2))+r2**2*(romberg(c,b2,b3,args=(cl0,A,k2)))+r3**2*(romberg(c,b3,b4,args=(cl0,A,k2))))-theor)*100./theor
    return ca

def Aforplot1(r, r1, r2,r3,m0,rs0,rp0,wr0,Rb,T0,bc0, cl0, hcc, theor, b1,b2,b3,b4):
    k2=(m0*(1-rs0/rp0)*wr0**2)/(2*Rb*T0)
    pex=1400

    xb = 1418.+k2*bc0**2
    xa = -1418.+k2*b4**2
#	be=be0
#	rs=rs0
#	rp=rp0
#	theor=Vdev*c0
#	print funct(xa,r1,bc0,cl0,k2,b1,b2,b3,b4)
#	print funct(xb,r1,bc0,cl0,k2,b1,b2,b3,b4)
    res=brentq(funct,xa,xb,args=(r1,r2,r3,hcc, theor, bc0,cl0,k2,b1,b2,b3,b4))
#	print res
    A=res

    #print wr0
    s = cl0/(1+n.exp(A-k2*r**2))
    #fig=plt.figure()
    #ax=fig.add_subplot(111)
    #ax.plot(r,s)
    #plt.show()
    #exit()
    return s

def cc2(rd,cl0,A,k2,k10):
    pippo = (cl0/2.)/n.cosh(A/2-k2*(rd)**2/2)*(n.exp(k2*(rd)**2/2-A/2))
    if pippo>cl0*k10:
        result = pippo
    else:
        result = 0.0 
    return result
    
def Aforplot2(r1, r2, r3, cl0, hcc, theor, m0,rs0,rp0,Rb,T0,bc0,b1,b2,b3,b4,mr,k10):

    A3=[]
    for ni,pp in enumerate(mr):
        k2=(m0*(1-rs0/rp0)*pp**2)/(2*Rb*T0)
        xb = 1418.+k2*(bc0)**2
        xa = -1418.+k2*(b4)**2
        res=brentq(funct,xa,xb,args=(r1,r2,r3,hcc, theor, bc0,cl0,k2,b1,b2,b3,b4))
        A3.append(res)
    u=[]
    for ni,pp in enumerate(mr):
        A = A3[ni]
        k2=(m0*(1-rs0/rp0)*pp**2)/(2*Rb*T0)
        u.append(pi*r3**2*(quad(cc2,b3,b4,args=(cl0,A,k2,k10))[0])/theor)
#def cc2(rd,cl0,A,k2):

    for ni,i in enumerate(u):
        if i<0.0:
            u[ni]=0.0
    return u

class SednmrController(BaseController):
    
    maxFreq = {}
    maxFreq['Agilent'] = {
        "7.9502": 5500,
        "5.969": 7000,
        "4.4958": 9000,
        "3.429": 12000,
        "4.3942": 7000,
        "2.4638": 18000,
        "3.2258": 10000,
        "2.032": 25000,
        "2.6162": 15000,
        "1.5748": 30000,
        "1.143": 40000,
        "0.625": 60000
    }
    
    maxFreq['Bruker'] = {
        "5.6": 7000,
        "3.0": 15000,
        "2.6": 24000,
        "1.7": 35000,
        "1.5": 42000,
        "0.9": 67000
    }
    
    maxFreq['JEOL'] = {
        "6.4": 8000,
        "2.6": 19000,
        "2.2": 24000,
        "1.7": 35000,
        "0.5": 80000,
        "0.35": 110000
    }
    
    maxFreq['Doty'] = {
            "2.2": 28000,
            "2.90": 18000,
            "3.2990": 12000,
            "2.9": 24000,
            "3.299": 11000,
            "3.5990": 18000,
            "3.599": 13000,
            "4.10950": 16000,
            "4.1095": 9000,
            "5.410": 12000,
            "5.41": 8000,
            "6.0170": 11000,
            "6.017": 7000
    }
    
    
    def __before__(self):
        """
        This __before__ method calls the parent method, and then sets up the
        tabs on the page.
        """
        c.page_base = u'WeNMR'

        c.page_title = u'SedNMR'

    
        
    def index(self):
        # Return a rendered template
        return render('/sedNMR.mako')
    
    def initPlots(self):
        b0 = 1.3
        be0 = b0/1000.
        r = n.arange(0.0, b0, 0.001)
        nr0 = 12000.
        wr0 = nr0*(2*pi)
        rs0 = 0.99
        rp0 = 1.23
        c0 = 30.
        cl0 = 700.
        m0 = 100.
        Rb = 8.31
        T0 = 274.
        k10 = 0.86
        k2=(m0*(1-rs0/rp0)*wr0**2)/(2*Rb*T0) 
        A = (n.exp((k2*be0**2)*(1-c0/cl0))-1)/(1-n.exp(-k2*(c0/cl0)*be0**2)) 
        s = cl0/(1+A*n.exp(-k2*(r/1000.)**2))
        #plot2
        mr = n.arange(100.0, 70000.0, 100.0)
        k3=(m0*(1-rs0/rp0)*(2*pi*mr)**2)/(2*Rb*T0)
        A3 = (n.exp((k3*be0**2)*(1-c0/cl0))-1)/(1-n.exp(-k3*(c0/cl0)*be0**2)) 
        u = (cl0/(k3*c0*be0**2))*n.log((n.exp(k3*be0**2)+A3)/(n.exp(-n.log((1-k10)/(k10*A3)))+A3))
        plot11 = []
        for i,c in enumerate(s):
            plot11.append(str(r[i])+", "+str(c))
        
        plot1 = ";".join(x for x in plot11)
        
        
        plot22 = []
        for i2,c2 in enumerate(u):
            plot22.append(str(mr[i2])+", "+str(c2))
            
        plot2 = ";".join(y for y in plot22)
        
        return plot1 +"::" + plot2
            
    def updateRotor(self):
       
        k10 = float(request.GET.get("tr"))
        T0 = float(request.GET.get("t"))
        m0 = float(request.GET.get("pmw"))
        c0 = float(request.GET.get("ic"))
        cl0 = float(request.GET.get("lc"))
        rp0 = float(request.GET.get("pd"))
        rs0 = float(request.GET.get("sd"))
        nr0 = float(request.GET.get("mf"))
        b0 = float(request.GET.get("rr"))/2
        
        rtype = request.GET.get("rt")
        
        
        be0 = b0/1000.
        r = n.arange(0.0, b0, 0.001)
        
        wr0 = nr0*(2*pi)
        
        Rb = 8.31

        k2=(m0*(1-rs0/rp0)*wr0**2)/(2*Rb*T0)
        A = (n.exp((k2*be0**2)*(1-c0/cl0))-1)/(1-n.exp(-k2*(c0/cl0)*be0**2)) 
        s = cl0/(1+A*n.exp(-k2*(r/1000.)**2))
        #plot2
        mfreq = self.maxFreq[rtype]
        mr = n.arange(100.0, self.maxFreq[rtype][str(request.GET.get("rr"))], 100.0)

        k3=(m0*(1-rs0/rp0)*(2*pi*mr)**2)/(2*Rb*T0)
        A3 = (n.exp((k3*be0**2)*(1-c0/cl0))-1)/(1-n.exp(-k3*(c0/cl0)*be0**2)) 
        u = (cl0/(k3*c0*be0**2))*n.log((n.exp(k3*be0**2)+A3)/(n.exp(-n.log((1-k10)/(k10*A3)))+A3))
        
        plot11 = []
        for i,c in enumerate(s):
            plot11.append(str(r[i])+", "+str(c))
        
        plot1 = ";".join(x for x in plot11)
        
        
        plot22 = []
        for i,c in enumerate(u):
            plot22.append(str(mr[i])+", "+str(c))
            
        plot2 = ";".join(y for y in plot22)

        return plot1 +"::" + plot2
    
    def updateDevice(self):
        tolerance=1E-300
        tol2=1e-3
        k10 = float(request.GET.get("tr"))
        T0 = float(request.GET.get("t"))
        m0 = float(request.GET.get("pmw"))
        c0 = float(request.GET.get("ic"))
        cl0 = float(request.GET.get("lc"))
        rp0 = float(request.GET.get("pd"))
        rs0 = float(request.GET.get("sd"))
        wr0 = float(request.GET.get("cs"))/60.
        #wr0 = nr0*(2*pi)
        #b0 = float(request.GET.get("rr"))/2
        #b0 = 152.
        #be0 = b0/1000.
        
        cr0 = 653.
        Rb = 8.31

        htot=float(request.GET.get("htot"))/100.
        b0 = float(request.GET.get("hmax"))
        be0 = b0/100.
        #hf0=0.018
        h3 = float(request.GET.get("h3"))/100.
        r3 = float(request.GET.get("r3"))/100.
        h2 = float(request.GET.get("h2"))/100.
        r2 = float(request.GET.get("r2"))/100.
        hfun = float(request.GET.get("hfun"))/100. 
        h1 = float(request.GET.get("h1"))/100.
        r1 = float(request.GET.get("r1"))/100.
        htc = hfun-h2-h1
        hcc = htc/(1.-r2/r1)
        bc0 = be0-htot
        b1 = bc0+h1
        b2 = b1+htc
        b3 = b2+h2
        b4 = b3+h3
        
        Vdev=pi*(r1**2*(b1-bc0)+romberg(pyra,b1,b2,args=(r1,hcc,b1))+r2**2*(b3-b2)+r3**2*(b4-b3))
        r = n.arange(bc0, b4, 0.001)
        mr = n.arange(30, 2000, 10)
        be=be0
        rs=rs0
        rp=rp0
        theor=Vdev*c0
        A=0
        k2=0
        ss=Aforplot1(r, r1, r2,r3,m0,rs0,rp0,wr0,Rb,T0,bc0,cl0, hcc, theor, b1,b2,b3,b4)
        uu=Aforplot2(r1, r2, r3, cl0, hcc, theor, m0,rs0,rp0,Rb,T0,bc0,b1,b2,b3,b4,mr,k10)

        plot11 = []
        for i,c in enumerate(ss):
            plot11.append(str(r[i]*100)+", "+str(c))
        
        plot1 = ";".join(x for x in plot11)
        
        
        plot22 = []
        for i,c in enumerate(uu):
            plot22.append(str(mr[i]*60)+", "+str(c))
            
        plot2 = ";".join(y for y in plot22)
        
        
        return plot1 +"::" + plot2
    
    
    def genDataDevice(self, k10, T0, m0, c0, cl0, rp0, rs0, wr0, htot, hmax, hfun, h3, h2, h1, r3, r2, r1):
        tolerance=1E-300
        tol2=1e-3
        k10 = float(k10)
        T0 = float(T0)
        m0 = float(m0)
        c0 = float(c0)
        cl0 = float(cl0)
        rp0 = float(rp0)
        rs0 = float(rs0)
        wr0 = float(wr0)/60.
        #wr0 = nr0*(2*pi)
        #b0 = float(request.GET.get("rr"))/2
        #b0 = 152.
        #be0 = b0/1000.
        
        cr0 = 653.
        Rb = 8.31

        htot=float(htot)/100.
        b0 = float(hmax)
        be0 = b0/100.
        #hf0=0.018
        h3 = float(h3)/100.
        r3 = float(r3)/100.
        h2 = float(h2)/100.
        r2 = float(r2)/100.
        hfun = float(hfun)/100. 
        h1 = float(h1)/100.
        r1 = float(r1)/100.
        htc = hfun-h2-h1
        hcc = htc/(1.-r2/r1)
        bc0 = be0-htot
        b1 = bc0+h1
        b2 = b1+htc
        b3 = b2+h2
        b4 = b3+h3
        
        Vdev=pi*(r1**2*(b1-bc0)+romberg(pyra,b1,b2,args=(r1,hcc,b1))+r2**2*(b3-b2)+r3**2*(b4-b3))
        r = n.arange(bc0, b4, 0.001)
        mr = n.arange(30, 2000, 10)
        be=be0
        rs=rs0
        rp=rp0
        theor=Vdev*c0
        A=0
        k2=0
        ss=Aforplot1(r, r1, r2,r3,m0,rs0,rp0,wr0,Rb,T0,bc0,cl0, hcc, theor, b1,b2,b3,b4)
        uu=Aforplot2(r1, r2, r3, cl0, hcc, theor, m0,rs0,rp0,Rb,T0,bc0,b1,b2,b3,b4,mr,k10)
        return ss, r, uu, mr
    
    def genDataRotor(self, k10, T0, m0, c0, cl0, rp0, rs0, nr0, b0, rt):
        #maxFreq = {
        #    "7.9502": 5500,
        #    "5.969": 7000,
        #    "4.4958": 9000,
        #    "3.429": 12000,
        #    "4.3942": 7000,
        #    "2.4638": 18000,
        #    "3.2258": 10000,
        #    "2.032": 25000,
        #    "2.6162": 15000,
        #    "1.5748": 30000,
        #    "1.143": 40000,
        #    "0.625": 60000,
        #    "5.6": 7000,
        #    "3.0": 15000,
        #    "2.6": 24000,
        #    "1.7": 35000,
        #    "1.5": 42000,
        #    "0.9": 67000
        #}
        
        k10 = float(k10)
        T0 = float(T0)
        m0 = float(m0)
        c0 = float(c0)
        cl0 = float(cl0)
        rp0 = float(rp0)
        rs0 = float(rs0)
        nr0 = float(nr0)
        b0 = float(b0)/2
        
        
        be0 = b0/1000.
        r = n.arange(0.0, b0, 0.001)
        
        wr0 = nr0*(2*pi)
        
        Rb = 8.31

        k2=(m0*(1-rs0/rp0)*wr0**2)/(2*Rb*T0)
        A = (n.exp((k2*be0**2)*(1-c0/cl0))-1)/(1-n.exp(-k2*(c0/cl0)*be0**2)) 
        s = cl0/(1+A*n.exp(-k2*(r/1000.)**2))
        #plot2
        mr = n.arange(100.0, self.maxFreq[rt][str(b0*2)], 100.0)

        k3=(m0*(1-rs0/rp0)*(2*pi*mr)**2)/(2*Rb*T0)
        A3 = (n.exp((k3*be0**2)*(1-c0/cl0))-1)/(1-n.exp(-k3*(c0/cl0)*be0**2)) 
        u = (cl0/(k3*c0*be0**2))*n.log((n.exp(k3*be0**2)+A3)/(n.exp(-n.log((1-k10)/(k10*A3)))+A3))
        
        return s, r, u, mr
    
    def prepare_download(self):
        devrot = str(request.POST.get("devrot"))
        if devrot == 'rotor':
            info = {
                'devrot': devrot,
                'threshold': str(request.POST.get("tr")),
                'temperature': str(request.POST.get("t")),
                'protmw': str(request.POST.get("pmw")),
                'initconc': str(request.POST.get("ic")),
                'limitconc': str(request.POST.get("lc")),
                'protdens': str(request.POST.get("pd")),
                'solvdens': str(request.POST.get("sd")),
                'masfreq': str(request.POST.get("mf")),
                'rotradius': str(request.POST.get("rr"))
            }
        else:
            info = {
                'devrot': devrot,
                'threshold': str(request.POST.get("tr")),
                'temperature': str(request.POST.get("t")),
                'protmw': str(request.POST.get("pmw")),
                'initconc': str(request.POST.get("ic")),
                'limitconc': str(request.POST.get("lc")),
                'protdens': str(request.POST.get("pd")),
                'solvdens': str(request.POST.get("sd")),
                'censpeed': str(request.POST.get("cs")),
                'htot': str(request.POST.get("htot")),
                'hmax': str(request.POST.get("hmax")),
                'hfun': str(request.POST.get("hfun")),
                'h3': str(request.POST.get("h3")),
                'r3': str(request.POST.get("r3")),
                'h2': str(request.POST.get("h2")),
                'r2': str(request.POST.get("r2")),
                'h1': str(request.POST.get("h1")),
                'r1': str(request.POST.get("r1"))
            }
        new_rnd_dir = str(random.randint(100000000, 999999999))
        new_path = os.path.join(config['app_conf']['sednmr_data'], new_rnd_dir)
        if not os.path.exists (new_path):
            os.makedirs(new_path)
        else:
            if os.path.exists(os.path.join(new_path, "sednmrDataTable.rtf")):
                os.remove(os.path.join(new_path, "sednmrDataTable.rtf"))
                os.remove(os.path.join(new_path, "sednmrRawPlotData.txt"))
                os.remove(os.path.join(new_path, "sednmrData.tar"))
        doc = RTFDoc.buildDOC(info)
        dataTablepath = new_path
        RTFDoc.saveToFile(doc, "sednmrDataTable.rtf", dataTablepath)
        
        filename = os.path.join(new_path,'sednmrDataTable.rtf')
        filenameRD = os.path.join(new_path,'sednmrRawPlotData.txt')
        handleRD = open(filenameRD, 'w')
        
        if devrot == 'rotor':
            [s, r, u, mr] = self.genDataRotor(request.POST.get("tr"), request.POST.get("t"), request.POST.get("pmw"), request.POST.get("ic"), request.POST.get("lc"), request.POST.get("pd"), request.POST.get("sd"), request.POST.get("mf"), request.POST.get("rr"), request.POST.get("rt"))
        else:
            [s, r, u, mr] = self.genDataDevice(request.POST.get("tr"), request.POST.get("t"), request.POST.get("pmw"), request.POST.get("ic"), request.POST.get("lc"), request.POST.get("pd"), request.POST.get("sd"), request.POST.get("cs"), request.POST.get("htot"), request.POST.get("hmax"), request.POST.get("hfun"), request.POST.get("h3"), request.POST.get("h2"), request.POST.get("h1"), request.POST.get("r3"), request.POST.get("r2"), request.POST.get("r1"))
        
        for i,c in enumerate(s):
            if str(c) != 'nan' and str(c) != 'inf':
                handleRD.write(str(r[i])+" "+str(c)+"\n")
        
        handleRD.write("\n")
        
        for i,c in enumerate(u):
            if str(c) != 'nan' and str(c) != 'inf':
                handleRD.write(str(mr[i])+" "+str(c)+"\n")
        
        handleRD.close()
        
        sedTarFile = tarfile.open(os.path.join(new_path, "sednmrData.tar"), 'w')
        sedTarFile.add(filename, arcname="sednmrDataTable.rtf", recursive=False)
        sedTarFile.add(filenameRD, arcname="sednmrRawPlotData.txt", recursive=False)
        sedTarFile.close()
        
        #permanent_file = open(os.path.join(session['DIR_CACHE_SEDNMR'], "sednmrData.tar"), 'rb')
        #data = permanent_file.read()
        #permanent_file.close()
        #[ty, enc] = mimetypes.guess_type(filename)
        #if not ty:
        #    ty = "text/plain"
        #response.content_type = ty
        #response.headers['Content-Lenght'] = len(data)
        #response.headers['Pragma'] = 'public'
        #response.headers['Cache-Control'] = 'max-age=0'
        #response.headers['Content-Disposition'] = 'attachment; filename="sedNMRdata.tar"'
        return new_rnd_dir
    
    def download(self):
        path = request.GET.get("path")
        permanent_file = open(os.path.join(config['app_conf']['sednmr_data'], path, "sednmrData.tar"), 'rb')
        data = permanent_file.read()
        permanent_file.close()
        [ty, enc] = mimetypes.guess_type(os.path.join(config['app_conf']['sednmr_data'], path, "sednmrData.tar"))
        if not ty:
            ty = "text/plain"
        response.content_type = ty
        response.headers['Content-Lenght'] = len(data)
        response.headers['Pragma'] = 'public'
        response.headers['Cache-Control'] = 'max-age=0'
        response.headers['Content-Disposition'] = 'attachment; filename="sedNMRdata.tar"' 
        return data
    
    def helpinfo(self):
        field = request.POST.get('field')
        print field
        info = open(os.path.join(config['app_conf']['properties'], "sednmr-info.properties"))
        l = 'n/a'
        for line in info:
            if field in line:
                l = line.split('=')[1]
                break
        return l