from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect 
from pylons import config
import sys,os,string, math

class multi_input:
    #n_crd = ""
    ##n_top = ""
    #n_pdb_Or = ""
    #n_pdb_Am = ""
    #top = []
    #crd = []
    #pdb_Or = []
    #pdb_Am = []
    ##coor atom number in pdb amber , atom number in pdb input
    #corr = {}
    #corr1 = {}
    #err = []
    #atm_trov = 0
    #atm_Or = 0
    #atm_Am = 0
    #crd_out = {}
    #errore = []
    #atm_res = {}
    #
    #debug_log = []
    ##debug = False
    #debug = True
    
    def __init__(self, n_pdb_Or, n_pdb_Am, n_crd):
        
        def delta(num1, num2):
            if abs(num1 - num2) < 0.01:
                return True
            else:
                return False
            
        #coor atom number in pdb amber , atom number in pdb input
        self.err = []
        self.atm_trov = 0
        self.crd_out = {}
        self.errore = []
        self.atm_res = {}
        self.debug_log = []
        
        debug_log = []
        #debug = False
        self.debug = True
        self.pdb_Or = open(n_pdb_Or,"r").readlines()
        self.pdb_Am = open(n_pdb_Am,"r").readlines()
        self.crd = open(n_crd,"r").readlines()
        #self.top = open(n_top,"r").readlines()
        anu1 = 0
        anu2 =0
        self.corr = {}
        
        if self.debug:
            self.debug_log.append("##############Corrispondenza atomi######################\n")
            self.debug_log.append("numero atomi amber %d\n"%len(self.pdb_Am))
            self.debug_log.append("numero atomi inPDB %d\n"%len(self.pdb_Or))
        for i in self.pdb_Am:
            atm_trov = 0
            if 'ATOM' in i[0:6]:
                anu1 = anu1 + 1
                xf1 = float(i[30:39])
                yf1 = float(i[39:46])
                zf1 = float(i[46:54])
                anum1 = int(i[6:11])
                anu2 = 0
                for a in self.pdb_Or:
                    if 'ATOM' in a[0:6]:                
                        anu2 = anu2 + 1
                        xf2 = float(a[30:39])
                        yf2 = float(a[39:46])
                        zf2 = float(a[46:54])
                        anum2 = int(a[6:11])
                        if delta(xf1, xf2) and delta(yf1, yf2) and delta(zf1, zf2):
                            self.corr[anum1] = anum2
                            self.atm_res[anum1] = i[0:30]
                            #self.corr["%d" %anu1] = "%d" %anu2
                            if self.debug:
                                self.debug_log.append("-----------------------------------------\n")
                                self.debug_log.append(i)
                                self.debug_log.append(a)
                                
                            self.atm_trov = self.atm_trov + 1
                            atm_trov = 1
                    elif "MODEL" in a[0:6]:
                        break
                if atm_trov == 0:
                    print "atom non trovato " , i
                    
        self.atm_Or = anu2
        self.atm_Am = anu1
        ks = self.corr.keys()
        ks.sort()
        for i in ks:
            print i, "=>", self.corr[i]
        print "numero di atomi trovato in AMBER pdb %s " % anu1
        print "numero di atomi trovato in INPUT pdb %s " % anu2
        print "dimensione vettore %s " % self.atm_trov
        
        if self.debug:
            print "###################DEBUG LOG#######################"
            de_file = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "DEBUG")
            print de_file
            open(de_file,"w").writelines(self.debug_log)
        
            
    def stampa(self):
        print self.corr
        print "atm_trov"
        print self.atm_trov
        print "atm_Or"
        print self.atm_Or
        print "atm_Am"
        print self.atm_Am
    
    def stampa_crd(self, name_pdb ):
        print self.crd
        open("prova.crd","w").writelines(self.crd_out["%s" %name_pdb])
    
   
    def add(self, pdb):
        def check_stup_res(i):
            if i == "PL":
                return False
            elif i == "LL":
                return False
            elif i == "LN":
                return False
            elif i == "NL":
                return False
            elif i == "LP":
                return False
            elif i == "LP":
                return False
            elif i == "LL2":
                return False
            elif i == "LL3":
                return False
            else:
                return True
            
        #pdb = open(name_pdb,"r").readlines()
        crd_tmp = []
        crd_tmp.append(" \n")
        crd_tmp.append("%5d\n"% int(self.atm_Am))
        nu = 0
        pdb_co = {}
        crd_co = []
        pdb2leap = []
        ter_res = []
        #pdb_co.append(" ")
        crd_co.append(" ")
        #self.atm_res.append(" ")
        
        
        #for i in self.pdb_Am:
        #   if 'ATOM' in i[0:6]:
        #        anum = int(i[6:11])
        #        self.atm_res[anum] = i[0:30]
        
        print "######### PDB IN DA TAR ###########"    
        for i in pdb:
            if 'ATOM' in i[0:6] and check_stup_res(i[17:21].replace(" ","")):
                xf1 = float(i[30:39])
                yf1 = float(i[39:46])
                zf1 = float(i[46:54])
                anum = int(i[6:11])
                pdb_co[anum] = ("%8.3f%8.3f%8.3f" %(xf1, yf1, zf1))
                #crd_co.append("%12.7f%12.7f%12.7f" %(xf1, yf1, zf1))
                print i[:-1]
                #self.atm_res.append(i[0:31])
        trov_in = len(pdb_co)
        print "Numero atomi trovati in tar PDB %d" % trov_in
        trov_atm = 0
        err = 0
        
        if trov_in <  self.atm_Am or trov_in ==  self.atm_Am:
            
            atm_keys = self.atm_res.keys()
            atm_keys.sort()
            for a in atm_keys:
                try:
                    pos = self.corr[a]
                    #print a,pos
                    print "%s%s" %(self.atm_res[a],pdb_co[pos])
                    #if "OXT" in self.atm_res[a][12:16]:
                    pdb2leap.append("%s%s\n" %(self.atm_res[a],pdb_co[pos]))
                    
                except:
                    print "amber pdb and input pdb  are differents" 
                    self.errore.append("amber pdb and input pdb  are differents"  )
                    err = 1
                
                trov_atm = trov_atm + 1
            print "Numero atomi convertiti in tar PDB %d" % trov_atm
            #sys.exit()   
            #trova TER   
            for il in range(len(self.pdb_Am)):
                if "TER" in self.pdb_Am[il]:
                    #print "trovato TER"
                    #print self.pdb_Am[il]
                    #print self.pdb_Am[il-1]
                    try:
                        ter_res.append(int(self.pdb_Am[il-1][22:26]))

                    except:
                        print "error in TER search multi_input.py"
            pdb2leap_ter = []
            print "TER trovati"
            print ter_res
            
            #print pdb2leap_ter
            #inserisci TER
            
            for i in range(len(pdb2leap)):
                
                pdb2leap_ter.append(pdb2leap[i])
                try:
                    if pdb2leap[i+1][22:26] != pdb2leap[i][22:26]:
                        div = True
                    else:
                        div = False
                except:
                    div = True
                    
                for a in ter_res:
                    if a == int(pdb2leap[i][22:26]) and div:
                        pdb2leap_ter.append("TER\n")
                        
            return pdb2leap_ter
            
        #da riverdere
        if  trov_in >  self.atm_Am:
            print "################ Warning ############################"
            print "input pdb have more atoms than amber pdb"
            self.errore.append("amber pdb and input pdb %s are differents" %name_pdb )
            err = 1
        
        #if trov_in ==  self.atm_Am:       
        #    for a in range(1,self.atm_trov + 1):
        #        try:
        #            pos = int(self.corr["%d" %a])
        #            #print "-------"
        #            #print pos
        #            #print crd_co[pos]
        #            #print len(crd_co)
        #            #print "trov_in %d" % trov_in
        #            crd_tmp.append(crd_co[pos])
        #        
        #            
        #        except:
        #            print "amber pdb and input pdb are differents"
        #            self.errore.append("amber pdb and input pdb %s are differents" %name_pdb )
        #            err = 1
        #        
        #        trov_atm = trov_atm + 1
        #        if (a+1)%2:
        #            crd_tmp.append("\n")
                    
        #print crd_tmp
        #print name_pdb
        #print self.crd
        print self.errore
        if err == 0:
            self.crd_out["%s" %name_pdb] = crd_tmp
            
        os.environ["AMBER_HOME"] = "/prog/amber10"
        amber_h_exe = "/prog/amber10/exe/"
        crd_in = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "pdb_scr.crd")    
        open(pdb_in,"w").writelines(crd_crd)
        cmd = "%s/ambpdb -aatm -p prmtop < %s "%(amber_h_exe, crd_in)
        return os.popen(cmd).read()
        #print self.crd_out

#multi_input input leap, ouput leap, crd ,top           
#ll = multi_input(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
##ll.stampa()
#ll + sys.argv[1]
#ll.stampa_crd(sys.argv[1])