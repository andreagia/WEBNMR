export LCG_GFAL_INFOSYS=bdii-enmr.cerm.unifi.it:2170
export LCG_CATALOG_TYPE=lfc
export LFC_HOST=lfcserver.cnaf.infn.it

#lcg-cp -v --vo enmr.eu lfn:/grid/enmr.eu/JobControl/STRUM1 file:./struttureMAX.tgz
lcg-cp -v --vo enmr.eu lfn:/grid/enmr.eu/JobControl/STRUM2 file:./curve_input.tgz

tar xvfz curve_input.tgz
#tar xvfz struttureMAX.tgz

tar xvfz in.tgz

#/bin/chmod 754 descr_grid
#./descr_grid

/bin/chmod 777 distcalc
./distcalc 7 

mkdir ./results
touch ./results/results.pcs
touch ./results/results.rdc
touch ./results/results.int
touch ./results/contributes

/bin/chmod 777 maxoccenmr.64
./maxoccenmr.64

tar cvfz out.tgz results

pwd 
ls -l
 
