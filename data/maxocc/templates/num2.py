#!/usr/bin/env python
import numpy
import string, os


file1 = open('0.mo', 'r')
lines=0
avel=0
alfa=[]
S=[]
for line in file1:
    lines +=1
    avel +=float(line)
    alfa.append(line)
b=0
ave=avel/lines
file1.close()
for x in range(0,lines):
#    print alfa[x]
    b += (float(alfa[x])-ave)**2
SD=(b/lines)**0.5
SD3=SD*3
SD10=SD*10
S.append(ave+SD)
S.append(ave+SD3)
S.append(ave+SD10)
S.append(ave*1.1)
file6 = open('maxocc.tre', 'r')
line=file6.readline()
ls3=string.split(line)
for x in range (0,len(ls3)):
    S.append(ave*(1+float(ls3[x])/100))
print S
file6.close()
#aggiungere 20%
#aggiungere soglie utente da file [soglie]
#leggere lista pesi e numero di strutture
print '%r, average for %r lines' %(ave,lines)
#print 'standard deviation: %r, %r, %r'%(SD,SD3,SD10)

file2 = open('0.crv', 'r')
file7 = open('maxocc.wst', 'r')
file3 = open('mo.log','w')
file4 = open('mo.crv','w')
file5 = open('mo.val','w')
#v2=["0.000","0.050","0.100","0.150","0.200"]
v2=[]
nstr=int(file7.readline())
for line in file7:

    v2.append('%0.3f' %float(line))

file7.close()
print v2
xx = numpy.zeros([nstr + 1,len(v2)],float)
for line in file2:
    ls2=string.split(line)
    xx[int(ls2[0])][v2.index('%0.3f' %float(ls2[1]))]=float(ls2[2])
#    xx[int(ls2[0])][v2.index(ls2[1])]=float(ls2[2])
#print xx
wrncount=0
for x in range (1,nstr):
    valmap=numpy.ones([len(S)],float)
    f1 = numpy.zeros([len(S)],int)
    for y in range (0,len(v2)):
#        file4.write(str(xx[x][y]))
#        file4.write('  ')
        for k in range (0,len(S)):
            if xx[x][y] > S[k]:
                if  f1[k] == 0:
                    f1[k] =1
                    if xx[x][y-1]== 0:
                        valmap[k]=v2[y]
                        wrnstr='Warning: estimate for %d th treshold in structure %d is biased from missing point ' %(k,x)
                        file3.write(wrnstr)
                        file3.write('\n')
                        wrncount += 1
                    else:
                        mo=(float(v2[y])+float(v2[y-1]))/2
                        valmap[k]=mo
               
    for z in range (0,len(S)):
        file5.write(str(valmap[z]))
        file5.write('  ')
    file5.write('\n')
#    file4.write('\n')
file3.close()
for x in range (0,len(v2)):
    file4.write(v2[x])
    file4.write('  ')
    for y in range (1,nstr):
        file4.write(str(xx[y][x]))
        file4.write('  ')
    file4.write('\n')
file4.close()
file5.close()

gp = os.popen( '/usr/bin/gnuplot', 'w' )
gp.write( "set output 'mo.png'; set terminal png; \n" )
gp.write( 'set xlabel "Weight of considered conformer" \n' )
gp.write( 'set ylabel "TF" \n' )
gp.write( 'unset key \n' )
cmdp='p "mo.crv" u 1:2 w linespoints'
for i in range (2,nstr):
    kkk=i+1
    cmdp=cmdp+', "mo.crv" u 1:%s w linespoints ' %str(kkk)
gp.write(cmdp + "\n")
gp.write( "exit\n" )
gp.close()

print wrncount
print nstr*len(S)
#mylist = []
#for x in range(1,11): myfile.write(str(x)),myfile.write('\n')
#myfile.close()

